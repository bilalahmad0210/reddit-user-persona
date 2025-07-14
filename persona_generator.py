import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
import google.generativeai as genai

# Load .env and configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

TOKEN_LIMIT = 30000  # Adjust based on Gemini's token limit (~32K for 1.5 Flash)

def load_prompt_template():
    with open("prompts/lucas_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def load_user_data(username):
    path = Path("output") / f"{username}_raw.json"
    return json.loads(path.read_text(encoding="utf-8"))

def estimate_token_length(text):
    return int(len(text) / 4)  # Roughly 4 characters per token

def call_gemini_api(prompt: str) -> str | None:
    try:
        logging.info("Sending prompt to Gemini (models/gemini-1.5-flash)...")
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error("Gemini API failed:\n%s", e, exc_info=True)
        return None

def chunk_data(prompt_template, posts, comments, chunk_size=15000):
    chunks = []
    current_data = {"posts": [], "comments": []}

    for post in tqdm(posts, desc="Chunking posts"):
        current_data["posts"].append(post)
        draft_prompt = prompt_template + "\n" + json.dumps(current_data, indent=2)
        if estimate_token_length(draft_prompt) > chunk_size:
            current_data["posts"].pop()
            chunks.append(json.dumps(current_data, indent=2))
            current_data = {"posts": [post], "comments": []}

    for comment in tqdm(comments, desc="Chunking comments"):
        current_data["comments"].append(comment)
        draft_prompt = prompt_template + "\n" + json.dumps(current_data, indent=2)
        if estimate_token_length(draft_prompt) > chunk_size:
            current_data["comments"].pop()
            chunks.append(json.dumps(current_data, indent=2))
            current_data = {"posts": [], "comments": [comment]}

    if current_data["posts"] or current_data["comments"]:
        chunks.append(json.dumps(current_data, indent=2))

    return chunks

def generate_persona(username: str):
    prompt_template = load_prompt_template().replace("<username>", username)
    user_data = load_user_data(username)

    posts = user_data.get("posts", [])
    comments = user_data.get("comments", [])

    logging.info("Preparing prompt chunks for Gemini...")

    chunks = chunk_data(prompt_template, posts, comments, chunk_size=TOKEN_LIMIT)

    full_output = ""
    for i, chunk in enumerate(tqdm(chunks, desc="Generating persona chunks")):
        full_prompt = prompt_template + "\n" + chunk
        result = call_gemini_api(full_prompt)
        if result:
            full_output += f"\n\n---\n### Chunk {i+1}\n\n" + result
        else:
            full_output += f"\n\n---\n### Chunk {i+1}\n\n Gemini failed on this chunk."

    if not full_output.strip():
        logging.warning("No response from Gemini.")
        return

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"persona_{username}.txt").write_text(full_output, encoding="utf-8")
    logging.info(" Persona saved to output/persona_%s.{md,txt}", username)

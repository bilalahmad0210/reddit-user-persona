# 🧠 Reddit User Persona Generator 

An intelligent, LLM-powered tool that scrapes a Reddit user's public posts and comments, then generates a psychologically grounded **User Persona Profile** using Google Gemini (or OpenAI GPT-4). It includes **citations from posts**, **motivations**, **personality traits**, and more. This project is part of the AI Engineering Internship evaluation at **Amlgo Labs**.

---

## 🔧 Project Architecture & Flow

```
Reddit User URL → Reddit Scraper (PRAW+Pushshift)
                         ↓
       Extract Posts + Comments (JSON)
                         ↓
      Prompt Construction with Persona Template
                         ↓
          🤠 Gemini / GPT-4 API Call
                         ↓
    📄 Persona Output (.txt / .md with Citations)
```

- `main.py`: Entry point for scraping + persona generation.
- `reddit_scraper.py`: Uses PRAW and Pushshift to collect Reddit activity.
- `persona_generator.py`: Sends chunked user data to Gemini / OpenAI for persona analysis.
- `prompts/lucas_prompt.txt`: Custom crafted prompt template.

---

## 📁 Folder Structure

```
reddit-user-persona/
├── main.py
├── reddit_scraper.py
├── persona_generator.py
├── prompts/
│   └── lucas_prompt.txt
├── output/
│   ├── kojied_raw.json
│   ├── persona_kojied.md
│   └── persona_kojied.txt
├── .env
├── requirements.txt
└── README.md
```

---

## ✨ Key Features

- ✅ Full Reddit scraping via PRAW + Pushshift
- ✅ Uses **all posts/comments** with **auto chunking**
- ✅ Generates detailed persona with:
  - Age, profession, motivations, habits
  - MBTI-style personality traits
  - Quotes and citations from real posts
- ✅ Works with **Gemini 1.5 Flash** or **OpenAI GPT-4**
- ✅ Includes **progress bars**, chunked inference, and clean outputs

---

## ▶️ How to Run Locally

### 1. Clone & Setup Environment

```bash
git clone https://github.com/your-username/reddit-user-persona.git
cd reddit-user-persona
python -m venv env
env\Scripts\activate  # or source env/bin/activate on Linux/macOS
pip install -r requirements.txt
```

### 2. Setup API Keys

Create a `.env` file like this:

```
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key  # optional fallback
```

### 3. Generate Persona

```bash
python main.py kojied
```

Output files will be saved in:
```
output/persona_kojied.txt
output/persona_kojied.md
```

---

## 🧠 Prompt Design

| Component           | Design Style       | Purpose                                |
|--------------------|--------------------|----------------------------------------|
| Prompt Type         | Zero-shot + Few-shot | Steer model into role of analyst      |
| Format              | JSON w/ real quotes | Aid LLM grounding + citation linking  |
| Tone                | Professional        | Useful for business / brand use cases |

---

## 🌐 Sample Output Snippet

```markdown
# Reddit Persona: u/kojied

**Age**: 25-35  
**Occupation**: iOS Developer (spatial computing)  
**Traits**: Practical • Analytical • Curious  

### Motivations
- Comfort: "I was at the wrong party."  
- Tech Curiosity: "Building in visionOS."

### Personality
- Introvert: 4/10  
- Thinking: High (strategic posts on visas and gaming)
```

---

## 🌐 Deployment-Ready Enhancements

| Feature                 | Status  |
|-------------------------|---------|
| Modular scripts         | ✅ Done |
| Prompt injection        | ✅ Done |
| Token overflow handling | ✅ Done (via chunking) |
| Markdown formatting     | ✅ Done |
| API fallback support    | ✅ Optional (OpenAI or Gemini) |

---

## 🚀 Future Ideas

- Web UI via Gradio or Streamlit
- Persona clustering from multiple users
- Sentiment timelines & subreddit graphs

---

## 🙋‍♂️ Author

Developed by **Bilal Ahmad** 

Reach out: [LinkedIn](https://linkedin.com/in/bilalahmad0210)  
GitHub: [@bilalahmad0210](https://github.com/bilalahmad0210)

---

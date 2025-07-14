import argparse
import logging

from reddit_scraper import fetch_user_data, save_user_data
from persona_generator import generate_persona

def main():
    # Setup logging format and level
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # CLI argument parsing
    parser = argparse.ArgumentParser(
        description="Reddit User Persona Generator"
    )
    parser.add_argument(
        "username",
        type=str,
        help="Reddit username (without r/ or u/)"
    )
    args = parser.parse_args()

    username = args.username

    # Step 1: Scrape Reddit data
    logging.info(f"Scraping Reddit data for u/{username}...")
    try:
        user_data = fetch_user_data(username)
        save_user_data(user_data)
        logging.info("Scraping complete.")
    except Exception as e:
        logging.error(f"Failed to fetch/save Reddit data: {e}")
        return

    # Step 2: Generate persona with LLM
    logging.info(f"Generating persona using LLM for u/{username}...")
    try:
        generate_persona(username)
        logging.info("Persona generation complete.")
    except Exception as e:
        logging.error(f"Failed to generate persona: {e}")

if __name__ == "__main__":
    main()

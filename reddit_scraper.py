import json
import os
import logging
from pathlib import Path

import praw


def load_reddit_config(path="config/reddit_config.json"):
    with open(path, "r") as f:
        return json.load(f)

def init_reddit_client():
    cfg = load_reddit_config()
    return praw.Reddit(
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        user_agent=cfg["user_agent"]
    )

def fetch_user_data(username, post_limit=100, comment_limit=100):
    reddit = init_reddit_client()
    user = reddit.redditor(username)

    posts = []
    comments = []

    try:
        logging.info(f"Fetching posts for u/{username}")
        for post in user.submissions.new(limit=post_limit):
            posts.append({
                "title": post.title,
                "selftext": post.selftext,
                "subreddit": str(post.subreddit),
                "created_utc": post.created_utc,
                "score": post.score,
                "url": post.url
            })
    except Exception as e:
        logging.error(f"Error fetching posts: {e}")

    try:
        logging.info(f"Fetching comments for u/{username}")
        for comment in user.comments.new(limit=comment_limit):
            comments.append({
                "body": comment.body,
                "subreddit": str(comment.subreddit),
                "created_utc": comment.created_utc,
                "score": comment.score,
                "link_permalink": f"https://www.reddit.com{comment.permalink}"
            })
    except Exception as e:
        logging.error(f"Error fetching comments: {e}")

    return {
        "username": username,
        "posts": posts,
        "comments": comments
    }

def save_user_data(data, out_dir="output"):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{data['username']}_raw.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved user data to {path}")

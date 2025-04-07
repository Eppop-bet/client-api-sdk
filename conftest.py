from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

missing = []
if not API_URL:
    missing.append("API_URL")
if not TEST_EMAIL:
    missing.append("TEST_EMAIL")
if not TEST_PASSWORD:
    missing.append("TEST_PASSWORD")

if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

"""One-time setup: saves your Gemini API key to .env"""
from pathlib import Path

key = input("Paste your Gemini API key here and press Enter: ").strip()
if key:
    env_path = Path(__file__).resolve().parent / ".env"
    env_path.write_text(f"GEMINI_API_KEY={key}\n")
    print(f"Saved to {env_path}")
    print("You can now run: python quickstart.py")
else:
    print("No key entered. Try again.")

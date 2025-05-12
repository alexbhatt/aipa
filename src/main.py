import os
from dotenv import load_dotenv

# Load .env only if running locally
if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv()

# Read environment variables
jira_api_key = os.getenv("JIRA_API_KEY")
jira_email = os.getenv("JIRA_EMAIL")
jira_url = os.getenv("JIRA_URL")

print("Running Jira Tool...")
print(f"URL: {jira_url}")
# Replace the print statements with actual API logic

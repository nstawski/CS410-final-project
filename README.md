## GitHub PR Review Bot

This is the final project for UIUC CS410 Text Information Systems class of Fall 2023. The idea is to enable catching simple typos and style errors in the PRs using ChatGPT.

This project is designed to be ran on localhost, but I might convert it to the webhook in the future.

Steps to run:

1. Create a virtual environment:

```
python -m venv github_pr_bot_venv
```

To activate:
```
source github_pr_bot_venv/bin/activate
```
2. Install Dependencies

```
pip install -r requirements.txt
```

3. Set up GitHub Access token
To be to use this application and connect to GitHub from your localhost, you need to setup a GitHub access token using this url: https://github.com/settings/personal-access-tokens/new

and make sure you grant access to the PR actions (important!)

4. Set up OpenAI API key
Go to https://platform.openai.com/api-keys to setup the key

5. Run the Script

```
python github_bot.py GITHUB_ACCESS_TOKEN OPENAI_API_KEY username/repository
```

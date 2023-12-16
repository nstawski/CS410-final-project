## GitHub PR Review Bot

This is the final project for UIUC CS410 Text Information Systems class of Fall 2023. The idea is to enable catching simple typos and style errors in the PRs using ChatGPT.

This project is designed to be ran on localhost, but I might convert it to the webhook in the future.

[Progress Report](https://github.com/nstawski/CS410-final-project/blob/main/Nina_Stawski_Final_Project_Progress_Report_updated.docx)
[Final Project report](https://github.com/nstawski/CS410-final-project/blob/main/Nina_Stawski_Final_Project_Report.pdf)
[Project Video](https://www.youtube.com/watch?v=IpcNBNLbRoo)

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

Go into the `github_bot` folder 

```
cd github_bot
```

Now run:

```
pip install -r requirements.txt
```

3. Set up GitHub Access token

To be able to use this application and connect to GitHub from your localhost, you need to setup a GitHub access token using this url: https://github.com/settings/personal-access-tokens/new

and make sure you grant this token access to the PR actions (important!)

4. Set up OpenAI API key

To be able to query OpenAI API, you need to have an account with https://platform.openai.com - this is the same account as for accessing the ChatGPT itself, but the billing is different.

By default, you get the $18 in credit for using the API, but you will be able to use gpt-4 endpoints only if you paid an additional $1 or more. I am using the `gpt-3.5-turbo` model that should be available for the free accounts, but you will definitely get better results if using `gpt-4`. There are other models that you can try: https://platform.openai.com/docs/models

If you want to change the model, there is a variable in `github_bot.py` named `MODEL` which you need to change. It is located at the top of the file right after the imports.

After you've logged in, go to https://platform.openai.com/api-keys to setup the API key and then provide it to this script as a parameter.

5. Run the Script

The script takes the following positional parameters:

`GITHUB_ACCESS_TOKEN` - replace it with your GitHub access token

`OPENAI_API_KEY` - replace it with your OpenAI API key

`username/repository` - replace it with the specific repository that you want to use for the testing


For the illustrative purposes, I created the repo and a pull request: https://github.com/nstawski/github-pr-bot-test/pull/1 . Bear in mind that the user from which the response is created is the one that owns the github token, so I would not recommend using any public repository for this.

Run the script as follows:

```
python github_bot.py GITHUB_ACCESS_TOKEN OPENAI_API_KEY username/repository
```

The script will automatically retry if it encounters issues with OpenAI response and its subsequent parsing. In some cases, if there is an issue with posting the comments on GitHub, it might exit with an error and you may need to start again. In this case, please try again.
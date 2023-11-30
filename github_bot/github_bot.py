from argparse import ArgumentParser
from github import Github
import requests
import openai

def get_last_pr_diff(settings, pr):
    # couldn't fetch the pr diff with the Github package for some reqson, using requests instead
    print(pr)
    api_url = f'https://api.github.com/repos/{settings.github_repo}/pulls/{pr.number}'
    headers = {'Authorization': f'token {settings.github_token}', 'Accept': 'application/vnd.github.diff'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        print ('response.text', response.text)
        return response.text
    else:
        print(f'Error fetching diff: {response.status_code}, {response.text}')
        return None
    
def analyze_pr_diff(settings, pr_diff):
    # send the diff to ChatGPT API and get the feedback

    openai.api_key = settings.openai_api_key

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  
            prompt=f'Please analyze the following GitHub diff and provide comments: {pr_diff}',
            )

        print ("respp", response)
        feedback = response.choices[0].text.strip() if response.choices else ""
        return feedback

    except openai.error.OpenAIError as error:
        print(f"Error in OpenAI API call: {error}")
        return []

def poll_prs(settings):
    # set up
    github_client = Github(settings.github_token)
    repo = github_client.get_repo(settings.github_repo)

    print('Checking the repo for open pull requests...')
    open_pull_requests = repo.get_pulls(state='open', sort='created')

    for pr in open_pull_requests:
        print('Pull request number', pr.number)
        print('Pull request title', pr.title)
        print('Working on the diff...')

        pr_diff = get_last_pr_diff(settings, pr)

        pr_comments = analyze_pr_diff(settings, pr_diff)

if __name__ == "__main__":
    project_description='''
        This script is using the ChatGPT and GitHub API
        to add automated comments on a pull request,
        catch simple style errors and suggest improvements.
        Usage:
    '''
    arguments = {
        "github_token": "GitHub Personal Access Token",
        "openai_api_key": "OpenAI API Key",
        "github_repo": "GitHub username/repository name (use slash, no spaces)",
    }

    parser = ArgumentParser(project_description)
    
    for (key, value) in arguments.items():
        parser.add_argument(key, help=value)
        
    settings = parser.parse_args()
    poll_prs(settings)
from argparse import ArgumentParser
# from github import Github

def get_last_pr_diff(repo, pr):
    # fetch the last commit
    commit = repo.get_commit(pr.head.sha)
    print('commit', commit)

def poll_prs(settings):
    # set up
    github_client = Github(settings.github_personal_token)
    repo = github_client.get_repo(settings.github_repo)

    print('Checking the repo for open pull requests...')
    open_pull_requests = repo.get_pulls(state='open', sort='created')

    for pr in open_pull_requests:
        print('Pull request number', pr.number)
        print('Pull request title', pr.title)
        print('Working on the diff...')
        get_last_pr_diff(repo, pr)


if __name__ == "__main__":
    project_description='''
        This script is using the ChatGPT and GitHub API
        to add automated comments on a pull request,
        catch simple style errors and suggest improvements.
        Usage:
    '''
    arguments = {
        "github_personal_token": "GitHub Personal Access Token",
        "openai_api_key": "OpenAI API Key",
        "github_repo": "GitHub username/repository name (use slash, no spaces)",
    }
    parser = ArgumentParser(project_description)
    for key, value in arguments:
        parser.add_argument(key, help=value)
        
    settings = parser.parse_args()
    poll_prs(settings)
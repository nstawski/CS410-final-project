import ast
from argparse import ArgumentParser
from github import Github
import requests
import openai

MODEL = "gpt-3.5-turbo-instruct"
def generate_prompt(pr_diff):
    return f'''
        As an experienced Python software engineer, please analyze the provided GitHub diff, which is written in Python. Your task is to provide structured comments detailing potential improvements in the pull request. For each comment:

        1. Suggest a specific improvement. This could be related to wording, spelling corrections, coding style, or a script enhancement.
        2. Include the improvement suggestion with relevant code, formatted in backticks for GitHub code snippet display.
        3. If the suggestion is about a code change or an inquiry for modification, illustrate it with valid Python code that matches the style and context of the original code.
        4. Format your response as a Python list of tuples. Each tuple should contain:
        - File path as a string
        - Line number as an integer
        - Comment as a string (correctly formatted and escaped)
        - Relevant diff hunk section as a string (accurately corresponding to the specific place the comment is related to)

        Ensure that your response starts with '[' and ends with ']', containing only the list of tuples. Each element in the tuple should be correctly formatted for Python, and all brackets in your response should be properly closed. The diff hunk section should specifically match the location of the suggested change.

        Here is the diff:
        {pr_diff}

        Please provide your structured comments as a list in this format:
        [("file_path.py", 10, "`suggested_code_change`", "@@ -8,12 +8,15 @@ diff hunk"), ...]

        '''

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
            model=MODEL,  
            prompt=generate_prompt(pr_diff),
            max_tokens=2000
        )

        print ('respp', response)
        feedback = response.choices[0].text.strip() if response.choices else ''

        # format and parse the feedback
        try:
            if feedback.strip().startswith("("): #check if the response starts with a tuple
                formatted_feedback = f'[{feedback.strip()}]' #convert a single tuple to the list of tuples
            else:
                formatted_feedback = feedback.strip()

            # replace backslash-escaped quotes with regular quotes
            cleaned_feedback = formatted_feedback.replace("\\\"", "\"")

            print('cleaned feedba', cleaned_feedback)

            try:
                # Evaluate the cleaned string as a Python object
                comments_to_add = ast.literal_eval(cleaned_feedback)
                return comments_to_add
            except Exception as e:
                print(f"Error evaluating the string: {e}")
                return None
            
        except (ValueError, SyntaxError) as error:
            print(f'Error in formatting the response: {error}')
            return []

    except openai.error.OpenAIError as error:
        print(f'Error in OpenAI API call: {error}')
        return []

def add_comments_on_pull_request(pr, repo, pr_comments):
    # Fetch the commit object using its SHA
    commit = repo.get_commit(pr.head.sha)

    for file_path, position, comment, diff_hunk in pr_comments:
        pr.create_review_comment(comment, commit, file_path, position)

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

        print(pr_comments)

        add_comments_on_pull_request(pr, repo, pr_comments)

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
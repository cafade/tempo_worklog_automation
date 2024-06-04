# Tempo worklog REST API wrapper

### Set environment vars

1. Create the .env file based on .env.example
2. Identify your org base Jira URL, ie. https://**foo**.atlassian.net
3. Follow the documentation instructions to generate a new Jira API token for your own
   account: [https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/) - [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
4. Generate a tempo OAuth token from this link (with Periods scope -> Manage worklogs and View worklogs, or with full permissions if you like): [https://foo.atlassian.net/plugins/servlet/ac/io.tempo.jira/tempo-app#!/configuration/api-integration](https://foo.atlassian.net/plugins/servlet/ac/io.tempo.jira/tempo-app#!/configuration/api-integration)
5. Put the above and your own personal data in the corresponding .env file variables

### Run with Docker and Docker compose

Build it:

`docker build -t tempo_worklog_automation:0.1.0 -f Dockerfile .`

Then with Docker run:

`# docker run --env-file .env --restart no --name tempo_worklog_automation -v '<PROJECT_PATH>/tempo_worklog_automation/data':/app/data -it tempo_worklog_automation:0.1.0 --file-path /app/data/<CSV_FILE_NAME>.csv`

With Docker compose simply create the csv file on the /data path and update the `command` parameter with your CSV_FILE_NAME:

`# docker compose -f docker-compose.yml up`

### Setup and run with [Poetry](https://python-poetry.org/)

Create new virtualenv inside project directory if needed:

`python -m venv '.venv'`

Install poetry if needed:

`pip install poetry==1.7.1`

Enable virtualenv with poetry:

`poetry shell`

Install packages dependencies:

`poetry install`

Run script from within project root directory with:

`./main.py --file-path <PATH_TO_CSV_FILE>`

### Setup and run with requirements.txt

Create new virtualenv inside project directory if needed:

`python -m venv '.venv'`

Enable virtualenv:

`source .venv/bin/activate`

Install packages dependencies:

`pip install -r requirements.txt`

Or install packages with dev dependencies:

`pip install -r requirements.dev.txt`

Run script from within project root directory with:

`./main.py --file-path <PATH_TO_CSV_FILE>`

### Run tests locally

From root of the project run:

`pytest --cov=tempo_worklog_automation --cov-report term-missing:skip-covered .`

### Misc

Tempo API docs: [https://apidocs.tempo.io](https://apidocs.tempo.io)

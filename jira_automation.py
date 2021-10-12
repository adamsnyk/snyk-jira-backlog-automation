import requests
import json
import pprint

headers = { "Authorization": "Token AUTH_TOKEN" }

# Request Data
page = 1
per_page = 1000
start_date = '2021-08-01'
end_date = '2021-08-30'
url = 'https://snyk.io/api/v1/reporting/issues/?page={}&perPage={}&sortBy=issueTitle&order=asc&groupBy=issue&from={}&to={}'.format(
    page,
    per_page,
    start_date,
    end_date
)

# Request Body
ORG_ID = 'ORG_ID_TOKEN'
data = {
    "filters": {
        "orgs": [ORG_ID],
        "types": [
            "vuln",
            "license",
            "configuration"
        ],
        "severities": [
            "critical",
            "high",
            "medium",
            "low"
        ],
    }
}

# Get Issue Data
response = requests.post(
    url=url,
    headers=headers,
    json=data
)


for result in json.loads(response.content)["results"]:
    for project in result['projects']:
        project_id = project['id']

        jira_url = 'https://snyk.io/api/v1/org/{}/project/{}/issue/{}/jira-issue'.format(
            ORG_ID,
            project_id,
            result['issue']['id']
        )

        data = {
            "fields": {
                "project": {"id": "10000"},
                "issuetype":{"name":"Bug"},
                "summary": result['issue']['title'],
                "description": """More about the vuln here: {}\nProject: {}\nSource: {}\nURL: {}""".format(
                    result['issue']['url'],
                    project['name'],
                    project['source'],
                    project['url']
                )
            }
        }

        print('')
        print(jira_url)
        pprint.pprint(data)
        # requests.post(
        #     url=jira_url,
        #     headers=headers,
        #     json=data
        # )
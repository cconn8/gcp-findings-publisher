#!/usr/bin/env python3
import base64
import json
import requests
from google.cloud import securitycenter_v1
from jira import JIRA

email = "DEPRECATED"
api_token = "DEPRECATED" # Hardcoded creds should be avoided at all cost - use Google Secret Manager instead

PREFIX = "https://console.cloud.google.com/security/command-center/findings"

def get_finding_detail_page_link(finding_name):
    """Constructs a direct link to the finding detail page."""
    org_id = finding_name.split("/")[1]
    return f"{PREFIX}?organizationId={org_id}&resourceId={finding_name}"

def get_asset(parent, resource_name):
    """Retrieves the asset corresponding to `resource_name` from SCC."""
    client = securitycenter_v1.SecurityCenterClient()
    resp = client.list_assets(
        securitycenter_v1.ListAssetsRequest(
            parent=parent,
            filter=f'securityCenterProperties.resourceName="{resource_name}"',
        )
    )
    page = next(resp.pages)
    if page.total_size == 0:
        return None

    asset = page.list_assets_results[0].asset
    return json.loads(securitycenter_v1.Asset.to_json(asset))

def get_jira_project(project):
    return PROJECT_MAPPING[project]

def search_issues(jira, JQL):
    issues = jira.search_issues(JQL)  # returns list of of issues that match the JQL query  
    return response

def create_jira_issue(jira, issue_dict):
    issue = jira.create_issue(jira, issue_dict)
    return issue

def ticket_exists(JQL):
    ticket = search_issues(JQL)
    return 

# Jira tickets will be titled "{SEVERITY} Vulnerability - {Finding}""
def format_finding(event, context):
    """Send finding to JIRA in the form of a ticket"""    #Need a search function to check the resource name in current projects!
    pubsub_message = base64.b64decode(event['data']).decode("utf-8")
    message_json = json.loads(pubsub_message)
    finding = message_json['finding']
    finding_metadata = message_json['resource']
    finding_advisory = finding['sourceProperties']

    description = finding['description']
    severity = finding['severity']
    category = finding['category']
    created = finding['createTime']
    project = finding_metadata['projectDisplayName']
    link = get_finding_detail_page_link(finding['name'])
    recommendation = finding_advisory['Recommendation']

    jira = JIRA(server="https://DEPRECATED", basic_auth=(email, api_token))
    if jira:
        print(jira)
        jira_sync(jira, description, severity, category, created, project, link, recommendation)
    else: 
        print('Failed to connect jira client!')

    return


def jira_sync(jira, description, severity, category, created, project, link, recommendation):

    print("Syncing jira...")
    jira_project = get_jira_project(project)   # get jira project name
    print("Project " + jira_project)
    jira_summary = "[VULN] {}".format(category)   # title used in the summary field of Jira ticket
    jira_description = """
                        Category: {}\n
                        Severity: {}\n
                        Recommendation: {}\n""".format(category, severity, description)
                        

    jira_comment = "[{}] New vulnerability detected in project ({}) - Link to finding ({})".format(created, project, link) 

    jql = "project = \'{}\' AND summary ~ \'{}\' order by created desc".format(jira_project, jira_summary)   # search project tickets
    
    issue_fields={
            'project': {'key': jira_project},
            'summary': jira_summary,
            'description': jira_description,
            'issuetype': {'name': 'Task'}
    }

    new_issue = jira.create_issue(fields=issue_fields)
    print('New vulnerability, JIRA issue created ({})'.format(new_issue))

    new_comment = jira.add_comment(new_issue, jira_comment)
    print("New comment added, JIRA comment ({})".format(new_comment))
    
    
    return new_issue
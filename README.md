## Overview 
* Automate the reporting of GCP Security Center Critical and High Findings to speed up remediation
* The app should detect changes in the Security Command center and create tickets for the appropriate teams in JIRA

### High Level Plan
1. Generate JIRA API key for the cloud function to create, update tickets in JIRA
2. Configure the security command center to publish Critical and High findings to Cloud Pub/Sub (when findings are created or updated)
3. Deploy a cloud function that subscribes to the Pub/Sub findings topic and trigger a "jira" clound function to Create/Update tickets when notifications are received



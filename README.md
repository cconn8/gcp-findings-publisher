## Overview 
* Automate the reporting of GCP Security Center Critical and High Findings to speed up remediation
* The app should detect changes in the Security Command center and create tickets for the appropriate teams in JIRA

### High Level Plan
1. Generate JIRA API key for the cloud function to create, update tickets in JIRA
2. Configure the security command center to publish Critical and High findings to Cloud Pub/Sub (when findings are created or updated)
3. Deploy a cloud function that subscribes to the Pub/Sub findings topic and trigger a "jira" clound function to Create/Update tickets when notifications are received


#### Update logs
- The cloud function entry point "format_finding" parses the finding response to extract data of value
- Based on the data, it generates tickets in the required JIRA project (PROJECT MAPPING dict is deprecated)
- Tickets are created per finding


#### To-Do
- Group tickets by finding (ie. vulnerability)
- Implement a jira search function to check for previously created tickets and add the new vulns to that 

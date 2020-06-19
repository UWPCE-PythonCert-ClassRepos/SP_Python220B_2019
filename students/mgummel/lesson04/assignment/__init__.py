mysql -u root -p --database=jiradb --host=jira76uat.cdj1vcotsd72.us-west-2.rds.amazonaws.com --port=3306 --batch
  -e "select jiraissue.ID,jiraissue.pkey,jiraissue.issuetype
     from jiraissue JOIN project on jiraissue.PROJECT = project.ID
     where project.pname = 'Operations Service Management'
     and jiraissue.REPORTER ='sa_change-api'
     and issuetype=51
     and resolutiondate <= '2016-12-31 23:59';"
  | sed 's/\t/","/g;s/^/"/;s/$/"/;s/\n//g' > test.csv
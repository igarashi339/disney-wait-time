function kick() {
  const scriptProperties = PropertiesService.getScriptProperties();
  const TOKEN = scriptProperties.getProperty('WAIT_TIME_SCRAPING_TOKEN')
  const headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": "token " + TOKEN
  }
  const options = {
    "method": "post",
    "payload": "{ \"ref\": \"main\" }",
    "headers": headers
  }
  const dispatch_id = "8874774"
  const requestUrl = 'https://api.github.com/repos/igarashi339/disney-wait-time/actions/workflows/' + dispatch_id + '/dispatches'
  UrlFetchApp.fetch(requestUrl, options)
}
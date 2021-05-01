function myFunction() {
    var response = UrlFetchApp.fetch('https://www.tokyodisneyresort.jp/tds/realtime/attraction/')
    var content = response.getContentText()
    console.log(content)
}
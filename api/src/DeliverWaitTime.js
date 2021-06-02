function doGet(e) {
    if (e.parameter.mode == "latest") {
        return getLatestWaitTime()
    } else {
      return ContentService.createTextOutput("error: parameter is invalid.");
    }
}

/**
 * 現時点での最新の待ち時間情報を取得して返す。
 */
function getLatestWaitTime() {
    const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
    const sheetName = "wait_time"
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)
    
    // スプレッドシートから情報を取得する
    const colNum = 30
    const key = sheet.getRange(1, 1, 1, colNum).getValues()[0]
    const data = sheet.getRange(sheet.getLastRow() - 1, 1, 1, colNum).getValues()[0]
    var waitTimeDict = {}
    for (let i = 0; i < colNum; ++i) {
      waitTimeDict[key[i]] = data[i]
    }
    
    // 時間を日本の標準時になおす
    const fixedTime = Utilities.formatDate(new Date(waitTimeDict['timestamp']), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm');
    waitTimeDict['timestamp'] = fixedTime

    var output = ContentService.createTextOutput()
    output.setMimeType(ContentService.MimeType.JSON)
    output.setContent(JSON.stringify(waitTimeDict))

    return output
}
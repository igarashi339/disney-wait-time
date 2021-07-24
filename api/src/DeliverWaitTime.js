function doGet() {
  const latestWaitTimeDict = getLatestWaitTime()
  const meanWaitTimeDict = getMeanWaitTime()
  let allInfoDict = {}
  for (let key in meanWaitTimeDict) {
    allInfoDict[key] = latestWaitTimeDict[key] + "," + meanWaitTimeDict[key]
  }

  var output = ContentService.createTextOutput()
  output.setMimeType(ContentService.MimeType.JSON)
  output.setContent(JSON.stringify(allInfoDict))
  return output
}

/**
 * 現時点での最新の待ち時間情報をスプレッドシートから取得する。
 */
function getLatestWaitTime() {
    const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
    const sheetName = "wait_time"
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)
    
    // スプレッドシートから情報を取得する
    const colNum = 30
    const key = sheet.getRange(1, 1, 1, colNum).getValues()[0]
    const data = sheet.getRange(sheet.getLastRow(), 1, 1, colNum).getValues()[0]
    var waitTimeDict = {}
    for (let i = 0; i < colNum; ++i) {
      waitTimeDict[key[i]] = data[i]
    }
    
    // 時間を日本の標準時になおす
    const fixedTime = Utilities.formatDate(new Date(waitTimeDict['timestamp']), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm');
    waitTimeDict['timestamp'] = fixedTime

    return waitTimeDict
}

/**
 * 現時点での平均待ち時間をスプレッドシートから取得する。
 */
function getMeanWaitTime() {
  const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
  const sheetName = "mean_wait_time"
  var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)

  // スプレッドシートから情報を取得する
  const colNum = 29
  const key = sheet.getRange(1, 1, 1, colNum).getValues()[0]
  const data = sheet.getRange(sheet.getLastRow(), 1, 1, colNum).getValues()[0]
  let meanWaitTimeDict = {}
  for (let i = 0; i < colNum; ++i) {
    meanWaitTimeDict[key[i]] = data[i]
  }

  return meanWaitTimeDict
}
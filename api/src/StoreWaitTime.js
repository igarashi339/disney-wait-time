function doPost(e) {
    const params = JSON.parse(e.postData.getDataAsString());
    if (isInvalid(params)) {
      return
    }
    const keySortedList = makeKeySortedList(params)
    const currentTime  = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy/MM/dd HH:mm');
    const writeTargetList = [ currentTime ].concat(keySortedList)
    writeToSpreadSheet(writeTargetList)
}

/**
 * dictの中身がすべて「停止中,-1」の場合trueを返す
 */
function isInvalid(dict) {
  for (var key in dict) {
    if (dict[key] != "停止中,-1") {
      return false
    }
  }
  return true
}

/**
 * dictを受け取り、key順でソートしたvalueのリストを返す
 */
function makeKeySortedList(dict) {
  var keyList = []
  for (var key in dict) {
    keyList.push(key)
  }
  keyList.sort()
  var valueList = []
  for (var key of keyList) {
    valueList.push(dict[key])
  }
  return valueList
}

/**
 * arrayの内容をスプレッドシートの末尾に追加する
 */
function writeToSpreadSheet(array) {
    const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
    const sheetName = "wait_time"
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)
    sheet.appendRow(array)
}
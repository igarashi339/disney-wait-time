function CalcAndWriteMeanWaitTime() {
    const dataMatrix = GetSourceWaitTimes()
    const meanList = CalcMeanWaitTime(dataMatrix)
    WriteToSheet(meanList)
}

/**
 * 過去7日分の生の待ち時間情報を取得する。
 */
function GetSourceWaitTimes() {
    const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
    const sheetName = "wait_time"
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)
    const rowPerDay = 90 // 1日あたりのスクレイピング回数
    const rowNum = 7 * rowPerDay
    const lastRow = sheet.getLastRow()
    const colNum = 29
    let data = sheet.getRange(lastRow - rowNum, 2, rowNum, colNum).getValues()
    for (let i = 0; i < colNum; ++i) {
        for (let j = 0; j < rowNum; ++j) {
            data[j][i] = data[j][i].split(',')[2]
        }
    }
    return data
}

/**
 * 生の待ち時間情報をもとに、各アトラクションの平均待ち時間を計算する。
 * @param {*} dataMatrix 生の待ち時間情報の行列
 */
function CalcMeanWaitTime(dataMatrix) {
    const rowNum = 7 * 90
    const colNum = 29

    let sumList = Array(colNum).fill(0)
    let denominatorList = Array(colNum).fill(0)
    let meanList = Array(colNum).fill(-1)
    for (let i = 0; i < colNum; ++i) {
        for (let j = 0; j < rowNum; ++j) {
            waitTime = dataMatrix[j][i]
            if (waitTime != "-1" && waitTime != "0") {
                sumList[i] += Number(waitTime)
                denominatorList[i] += 1
            } 
        }
    }
    for (let i = 0; i < colNum; ++i) {
        if (denominatorList[i] == 0) {
            continue
        }
        meanList[i] = Math.floor(sumList[i] / denominatorList[i])
    }
    return meanList
}

/**
 * 計算した平均待ち時間情報をスプレッドシートに出力する。
 * @param {*} meanList 
 */
function WriteToSheet(meanList) {
    const sheetId = "1GvymAJ57Il1dSbPGVeGv4PDwi6ymDs_MHfHDbosQFpc"
    const sheetName = "mean_wait_time"
    var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName)
    sheet.appendRow(meanList)
}
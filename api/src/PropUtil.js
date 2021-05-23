/**
 * GASの環境変数を設定する。
 * key, valueの値をGASのコードエディタ上で編集して利用すること。
 */
function setVal() {
    const key = "KEY"
    const value = "VAL"
    PropertiesService.getScriptProperties().setProperty(key, value);
    Logger.log(PropertiesService.getScriptProperties().getProperty(key));
}
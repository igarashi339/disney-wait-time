// const puppeteer = require('puppeteer');
import { puppeteer } from './importable.js';

function fetchWaitTimeData() {
    // const url_key = "DISNEY_SEA_WAIT_TIME"
    // const url = PropertiesService.getScriptProperties().getProperty(url_key)
    const url = "https://disneyreal.asumirai.info/realtime/disneysea-wait-today.html"
    
    const testItems = async page => {
        const items = await page.$$("div.realtime")
        for (const item of items) {
            const attractions = await item.$$("li")
            console.log(attractions.length)
        }
    }

    (async () => {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url)
        await testItems(page)
        await browser.close();
    })();
}

fetchWaitTimeData()
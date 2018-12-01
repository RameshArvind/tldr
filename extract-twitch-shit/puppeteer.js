const puppeteer = require("puppeteer");

async function getTimeStamps(urls = [], getClipEnd = _ => Promise.resolve(_)) {
  const browser = await puppeteer.launch();
  console.log("Puppeteer launched");
  const times = await Promise.all(
    urls.map(async ({ url, id, video_id }) => {
      let page = await browser.newPage();
      await page.goto(url);
      await page.waitForSelector("a.tw-interactive.tw-button");
      let time = await page.evaluate(() => {
        const link = document.querySelector("a.tw-interactive.tw-button");
        let url = new URL(link.href).searchParams.get("t");
        let instant = 0;
        let arr;
        if (url.includes("h")) {
          arr = url.split("h");
          instant += parseInt(arr[0]) * 3600;
          url = arr[1];
        }
        if (url.includes("m")) {
          arr = url.split("m");
          instant += parseInt(arr[0]) * 60;
          url = arr[1];
        }
        if (url.includes("s")) {
          arr = url.split("s");
          instant += parseInt(arr[0]);
        }
        return instant;
      });
      let endTime = await getClipEnd(id);
      return { video_id, clips: [time, Math.round(time + endTime)] };
    })
  );

  await browser.close();
  console.log(`Generated timestamps for clips`);
  return times;
}

module.exports = getTimeStamps;

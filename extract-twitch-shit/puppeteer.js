const puppeteer = require("puppeteer");

const fetchTiming = async (urls = []) => {
  const browser = await puppeteer.launch()

  const times = (await Promise.all(urls.map(async url => {
    let page = await browser.newPage()
    await page.goto(url);
    await page.waitForSelector('a.tw-interactive.tw-button');
    await page.waitForSelector('[aria-valuemax]');
    let time = await page.evaluate(() => {
      const link = document.querySelector('a.tw-interactive.tw-button')
      let url = new URL(link.href).searchParams.get("t");
      let instant=0,arr;
      if(url.includes('h')){
        arr = url.split('h');
        instant += parseInt(arr[0])*3600;
        url = arr[1];
      }
      if(url.includes('m')){
        arr = url.split('m');
        instant += parseInt(arr[0])*60;
        url = arr[1];
      }
      if(url.includes('s')){
        arr = url.split('s');
        instant += parseInt(arr[0])
      }
      return instant;
    });
    return time;
  }))).reduce((acc, time) => {
    return [...acc, time];
  }, []);


  await browser.close();
  return times;
}

fetchTiming(['https://clips.twitch.tv/FaintWildSoymilkLitty', 'https://clips.twitch.tv/DreamyRoundKeyboardArgieB8']).then(time => {
  console.log(time);
});

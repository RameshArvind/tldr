let fetch = require("node-fetch");
module.exports = (req, res) => {
  res.end();
  let myLocation = `http://localhost${req.url}`;
  let vod = new URL(myLocation).searchParams.get("vod");
  // Call twitch
  // Call puppeteer
  // Return values back
};

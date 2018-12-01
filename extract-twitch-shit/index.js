let fetch = require("node-fetch");
let cors = require("micro-cors")();
let pullChats = require("./pull-chat");
let getTimeStamps = require("./puppeteer");
let fs = require("fs");
require("dotenv").config();

let helixHost = "https://api.twitch.tv/helix/";
let krakenHost = "https://api.twitch.tv/kraken/";

// (vod, chat, timestamps)

let clipSchema = {
  id: "BitterGrossStingrayTheThing",
  url: "https://clips.twitch.tv/BitterGrossStingrayTheThing",
  video_id: "",
  game_id: "32399",
  title: "LIVE: [EN] NA'VI vs Team Dignitas - Semifinals - EPICENTER: Moscow",
  view_count: 587551,
  created_at: "2016-10-23T13:53:25Z",
  thumbnail_url:
    "https://clips-media-assets2.twitch.tv/23480386448-offset-24980-preview-480x272.jpg"
};

dataset = [
  {
    vodid: 111111,
    chatlog: "tldr/lolchat.txt",
    clips: [[1, 10], [30, 40]],
    duration: 60 * 60 * 10
  },
  {
    vodid: 22222,
    chatlog: "tldr/cschat.txt",
    clips: [[30, 50], [65, 75]],
    duration: 60 * 60 * 1
  }
];

let fetchOptions = {
  headers: {
    "Client-ID": process.env.CLIENT_ID
  }
};

async function getClipEnd(clipSlug) {
  console.log(clipSlug);
  let myResponse = await fetch(`${krakenHost}clips/${clipSlug}`, {
    headers: {
      ...fetchOptions.headers,
      Accept: "application/vnd.twitchtv.v5+json"
    }
  });
  let clipInfo = await myResponse.json();
  return +clipInfo.duration;
}

function updateDataset(videosMap, cursor) {
  let datasetPath = path.join(__dirname, "dataset.json");
  let dataset;
  if (fs.existsSync(datasetPath)) {
    dataset = JSON.parse(fs.readFileSync(datasetPath, { encoding: "utf8" }));
  } else {
    dataset = {
      data: []
    };
  }
  dataset.data = dataset.data.concat(Object.values(videosMap));
  if (cursor) dataset.cursor = cursor;
  fs.writeFileSync(datasetPath, JSON.stringify(dataset), {
    encoding: "utf8"
  });
}

async function getDuration(vodid) {
  let myResponse = await fetch(`${krakenHost}videos/${vodid}`, {
    headers: {
      ...fetchOptions.headers,
      Accept: "application/vnd.twitchtv.v5+json"
    }
  });
  let clipInfo = await myResponse.json();
  return clipInfo.length;
}

module.exports = async function getDataSet(gameId, mCursor) {
  let videosMap = {};
  // Call twitch
  let getClips = `${helixHost}clips?game_id=${gameId}`;
  if (mCursor) {
    getClips = `${getClips}&first=10&after=${mCursor}`;
  }
  let getClipsCall = await fetch(getClips, fetchOptions);
  let {
    data: clips,
    pagination: { cursor }
  } = await getClipsCall.json();

  let validClips = clips.filter(
    _ =>
      _.video_id !== "" &&
      ![
        "160824571",
        "160021913",
        "160292158",
        "222906582",
        "117227658",
        "230597320"
      ].includes(_.video_id)
  );
  console.log(`Clips to be processed ${validClips.length}`);
  let _ = await Promise.all(
    validClips.map(_ =>
      pullChats(_.video_id, process.env.CLIENT_ID, getDuration)
    )
  );
  _.forEach(v => {
    videosMap[v.vodid] = {
      ...v,
      clips: []
    };
  });
  let timestamps = await getTimeStamps(validClips, getClipEnd);
  timestamps.forEach(_ => {
    videosMap[_.video_id] = {
      ...videosMap[_.video_id],
      clips: [...videosMap[_.video_id].clips, _.clips]
    };
  });
  updateDataset(videosMap, cursor);
  console.log(cursor);
  process.exit(1);
};

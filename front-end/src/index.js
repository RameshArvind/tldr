// let videoId = "171190663"; // CS:GO
// let videoId = "103229429"; // DOTA
let videoId = new URL(window.location).searchParams.get("videoId");
function formatTime(seconds) {
  let hourFragment = "0";
  let minuteFragment = "0";
  let secondFragment = "0";
  let minutes = Math.floor(seconds / 60);
  seconds = seconds % 60;
  let hours = Math.floor(minutes / 60);
  minutes = minutes % 60;
  hourFragment = hours > 9 ? hours : "0" + hours;
  minuteFragment = minutes > 9 ? minutes : "0" + minutes;
  secondFragment = seconds > 9 ? seconds : "0" + seconds;
  return `${hourFragment}:${minuteFragment}:${secondFragment}`;
}

let highlightsContainer = document.getElementById("highlights");
let currentHighlight;
let player;
function createHighlight([start, end]) {
  let div = document.createElement("div");
  let btn = document.createElement("button");
  btn.innerText = `${formatTime(start)} - ${formatTime(end)}`;
  btn.addEventListener("click", e => {
    if (currentHighlight) {
      clearInterval(currentHighlight);
    }
    player.seek(start);
    if (player.isPaused()) {
      player.play();
    }
    currentHighlight = setInterval(() => {
      let myTime = player.getCurrentTime();
      if (Math.abs(myTime) >= end) {
        player.pause();
        clearInterval(currentHighlight);
      }
    }, 1000);
  });
  div.appendChild(btn);
  return div;
}

let options = {
  video: videoId
};

function getHighlights(params) {
  fetch(`http://10.99.0.210:5000/highlights/${videoId}`, {
    mode: "cors"
  })
    .then(_ => _.json())
    .then(({ data: highlights }) => {
      highlightsContainer.append(
        ...highlights.sort((a, b) => a[0] - b[0]).map(createHighlight)
      );
      player = new Twitch.Player("app", options);
    });
}

getHighlights();

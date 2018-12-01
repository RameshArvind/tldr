let twitchChat = require("twitch-chatlog");
let fs = require("fs");
let path = require("path");
let formatMessage = require("./format-chat");
let fileOptions = {
  encoding: "utf8"
};
module.exports = async function getChat(vodId, clientId, getDuration) {
  let chatlog = path.join(
    "tldr",
    "extract-twitch-shit",
    "chats",
    `${vodId}.chat`
  );
  let chatFile = path.join(__dirname, "chats", `${vodId}.chat`);
  let duration = await getDuration(vodId);
  if (fs.existsSync(chatFile)) {
    return {
      chatlog,
      duration,
      vodid: vodId
    };
  }
  console.log(`Retrieving chat logs for ${vodId}`);
  let chats = await twitchChat.getChatlog({ clientId, vodId });
  let chat = chats.map(formatMessage).join("\n");
  fs.writeFileSync(chatFile, chat, fileOptions);
  console.log(`Created chat log for ${vodId}`);
  return { chatlog, duration, vodid: vodId };
};

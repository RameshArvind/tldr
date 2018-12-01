function formatUsername(msg) {
  const username = msg.commenter.display_name || msg.commenter.name;
  if (msg.message.is_action) {
    return `** ${username}`;
  }
  return `<${username}>`;
}

const timestampFormatter = new Intl.DateTimeFormat("en-US", {
  year: "2-digit",
  month: "numeric",
  day: "numeric",
  hour12: true,
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit"
});
module.exports = function formatMessage(msg) {
  let timestamp = `[${timestampFormatter.format(new Date(msg.created_at))}]`;
  let username = formatUsername(msg);
  let { body: message } = msg.message;

  return [timestamp, username, message].join(" ");
};

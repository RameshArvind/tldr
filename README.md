# tldr

Google Colab Notebook for the model - https://colab.research.google.com/drive/1iQHwjHrK8cGC-a_SWah5eOdIkBXcrf4e

## Running the Front-end code
  
```sh
cd front-end/
npm install
npm start
```

## Scraping for chat history

```js
let getChats = require("./extract-twitch-shit");
let gameId = ...;
getChats(gameId).then(chats => {
    ...
})
```

## To compile hightlights

```sh
python highlight_classification_model_new.py
```

## To start the flask serve

```sh
python app.py
```

# project2-mb865
Webpage served on `/` that allows user to log in with a username. Once logged in a tic-tac-toe board is shown and can be played depending on the type of user you log in as.

## Installation Guide
```
# clone repo
$ git clone https://github.com/NJIT-CS490-SP21/project2-mb865.git

# install requirements and npm packages
$ npm install`
$ pip install -r requirements.txt

Run echo "DANGEROUSLY_DISABLE_HOST_CHECK=true" > .env.development.local in the project directory

# run the server in one terminal
$ python app.py

# run the front end in another
$ npm run start

```

## Technologies Used
### Flask
Flask is a python framework that is used here to serve the main webpage for the application. After importing the library in `app.py`, the instance is created as `app`. The route decorator is then used to determine what happens when the `/` endpoint is called upon the server.

### React
React is a JS front end frame work that is used to render dynamic components of html.

### Socket Io
Socket Io is a web socket library used to update different sessions with the current state of the game and users

### Miscellaneous
* `https://fonts.google.com/` is used to select a font family.
* `https://uigradients.com/` is used to obtain the css code for the gradient background.

## Discoveries
### a. What are at least 3 technical issues you encountered with your project? How did you fix them?
* Sometimes my sockets were just not emitting and I solved the problem by not attempting to emit two socket events from one socket listener in the app.py
* My socket events were instantiated twice and I noticed this because my sockets would emit two connect and disconnect events when a new tab opened the web page. I fixxed this by getting rid of the extra instantiation of socketio in my board componnet and passed the one from my App.js component as a props
* I couldn't keep track of which socket belonged to which user in order to just emit socket events to specific users. I fixed this by using request.sid to obtain the id of the socket and placed it in a list next to the associated username.
### b. What are known problems, if any, with your project?
* The code overall feels messy and I would like to do some refactoring with it.
### c. What would you do to improve your project in the future?
* Improve the code so it is easier to follow
* Improve the styling


## Deploy to Heroku
*Don't do the Heroku step for assignments, you only need to deploy for Project 2*
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`

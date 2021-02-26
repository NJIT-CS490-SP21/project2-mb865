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
### b. What are known problems, if any, with your project?
### c. What would you do to improve your project in the future?


## Deploy to Heroku
*Don't do the Heroku step for assignments, you only need to deploy for Project 2*
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`

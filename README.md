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

# run the app
python app.py

```

## Technologies Used
### Flask
Flask is a python framework that is used here to serve the main webpage for the application. After importing the library in `app.py`, the instance is created as `app`. The route decorator is then used to determine what happens when the `/` endpoint is called upon the server.

### Spotipy
Spotipy is a python library that allows you to create a spotipy instance. This instance lets you interact with the Spotify API easily when provided with the right credentials. In my project I use it to obtain the top 10 tracks from each artist on my list of artists. This list of tracks is then parsed for the required information for my webpage.

### Heroku
Heroku is a free deployment server service that allows me to display my webpage on the global internet @ `https://project1-mb865.herokuapp.com/`.

### Miscellaneous
* `https://getbootstrap.com/docs/4.0/getting-started/introduction/` is used for easy styling.
* `https://fonts.google.com/` is used to select a font family.
* `https://uigradients.com/` is used to obtain the css code for the gradient background.

## Discoveries
### a. What are at least 3 technical issues you encountered with your project? How did you fix them?
* An issue that kept coming up was the fact the sometimes the requests would respond with null or empty arrays. Too avoid errors in the app, I would have to perform null or length checks on the responses.
* I was having trouble with deploying the app at first. Heroku didnt understand what kind of code I was trying to deploy and I fixed it by using a correct Procfile
* I was trying to dynamically display 10 songs from a randomly chosen artist and was having trouble keeping consistant margins on the loop'd tracks with bootstraps grid design. I fixed it by looping only 3 at a time and having an outer loop to change the range to loop from to get the other 7 tracks out evenly.
### b. What are known problems, if any, with your project?
* One known problem I can think of is that sometimes a preview is not given for an artists track. This causes the player to not work, I wish it would display an error message so the user can understand whats going on.
### c. What would you do to improve your project in the future?
* I would add a search function among the lists of artists I have selected. This would cut down the randomness of the requests and give the user more control over the application.


## Deploy to Heroku
*Don't do the Heroku step for assignments, you only need to deploy for Project 2*
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`

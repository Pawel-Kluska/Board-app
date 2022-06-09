# Board-app

This project was created for the Script Languages university course. The goal was to create an advanced application using Python. 
I created Bord-app, apllication similar to popular social media sites, where everyone can make their own posts and comments. 
You can run this application clicking on the following link

http://172.104.228.250/

## Technology

- Python
- Flask
- HTML
- CSS
- Bootstrap

## Screenshots
### Home page
![Alt text](/scrennshots/scr1.JPG?raw=true "Home")
### Registration page
![Alt text](/scrennshots/scr2.JPG?raw=true "Registration")
### Account 
![Alt text](/scrennshots/scr3.JPG?raw=true "Account")

## Functionalities
- Create user
- Update user (user data and password)
- Create/Update/Delete Post
- Create Comment under Post
- Give Like/Dislike on Post
- Password recovery by email
- Set user profile image
- Sort posts
- Filter posts by user
- Posts pagination

## Deployment 🚀

Get the repository using git clone:
```bash
git clone https://github.com/Pawel-Kluska/Board-app.git <repo>
```
Then install Python virtual enviroment
```bash
cd <repo>
```
```bash
pip install virtualenv 
```
(if you don't already have virtualenv installed)
```
```bash
virtualenv venv to create your new environment
```
(called 'venv' here)
```bash
source venv/bin/activate (to enter the virtual environment)
pip install -r requirements.txt
```
The app will be available under [localhost:5000](http://localhost:5000/).

This app is also deployed on Linux server http://172.104.228.250/ (unfortunately on linux there is a problem with sending emails but I'm working on it)




# TeamSoftwareProject - Group 8

## Final Release Documentation

## About the Project:

This GitHub repo began as a Team Software Project in the third year CS3305 Module of the Computer Science Degree course (2020/21 term) at the [School of Computer Science and Information Technology (CSIT)](https://www.ucc.ie/en/compsci/) at [University College Cork (UCC)](https://www.ucc.ie/en/), Ireland.  The lecturer was [Dr. Jason Quinlan](https://www.ucc.ie/en/misl/people/jquinlan/).

This typing trainer was developed as a means to practice touch typing, receiving feedback with every attempt and a way to collate your practice data over and extended period of time. Using Markov Chains, we generate text that closely mirrors real life applications. It was developed as a flask web app, and using JavaScript as the front end for the gameplay. The beta release only uses text generated from Mary Shelley's Frankenstein, but the final release will have a variety of sources to pull from to generate the practice sets.

## Running the Project:

### From Your Local Machine:

*Note: Python 3.9 may be necessary to run locally however older versions have worked for some. pip3 will be necessary.*

1. If you wish to run the beta offline and directly from your machine, then you will need to download the development branch as a zip file
or use the command `git clone  https://github.com/Raffi-Baldassini/TeamSoftwareProject.git`

2. Install the dependencies using `pip install -r requirements.txt`

3. In the Source directory, use the command `flask run` to start the server and then go to the [locally hosted IP address](http://127.0.0.1:5000/).

### From Hosted Version:

1. Navigate to [this](http://typing-trainer.pb97.container.netsoc.cloud:16555/) website.

## Usage:

Once on the site, whether locally hosted or not, you'll have the option to sign-in, sign-up, or play as a guest.
All pages on the site have a toggle button for theme-switching in the bottom right corner.
If you sign-in, you will be redirected to your profile where you will be able to view your current statistics, and view historical records for yourself and people you follow using the form on the page.
On the practice page you will see the generated text for you to practice on.
The game is played using your keyboard to match the text displayed in the grey box.
You can use the 'backspace' and 'enter' keys to reset the current textset and generate a new one.
Game-specific stats are updated every 100ms and displayed between the virtual keyboard and generated text.
Any changes to your overall statistics will be reflected in your profile.

## Code Conventions:
We employed the Google Python style guidelines while writing our code

## Contributors:

* Shane Fitzgerald Knott

* Cormac Coleman

* Niamh Healey

* Pavel Belitskiy

* Raffaele Baldassini

## Special Thanks:
Much of the code that we initially based our keyboard implementation on was written by Gregory Schier, as can be seen [here](https://codepen.io/gschier/pen/VKgyaY)

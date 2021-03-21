# Overview

## Guide to Submission
The directory tree below includes only files deemed relevant to this submission for simplicity.
```
    │
    │Overview.md
    │	
    ├───FinalDocumentation
    │       lessons_learned.pdf
    │       ProjectBrief.pdf
    │
    └───TeamSoftwareProject
        │   README.md
        │   requirements.txt
        │
        ├───Documents
        │   │
        │   ├───Minutes
        │   │
        │   └───ProjectBrief
        │
        └───Source
            │   app.py
            │   db_interaction.py
            │   friendsChart.py
            │   gamePage.py
            │   gutenbergScraper.py
            │   MarkovGenerator.py
            │   RandomCharacterMarkovChains.py
            │   RandomWordMarkovGenerator.py
            │   user_management.py
            │   __init__.py
            │
            ├───static
            │   │   base.css
            │   │   normalize.css
            │   │   practice.js
            │   │   profile.js
            │   │   scripts.js
            │   │   signup.css
            │   │
            │   └───assets
            │           space_devs.gif
            │
            ├───template
            │       index.html
            │       login.html
            │       practice.html
            │       profile.html
            │       signup.html
            │
            └──TextGeneration
               ├───FrequencyDictionaries
               │
               └───Texts
```
## Final Documentation
Contains the final versions of the Project Brief and Lessons Learned from the group
## TeamSoftwareProject
In the base directory the project's README and requirements list can be found.  The README will explain the installation/running of the project along with more meta-info.
## Documents
Older versions of documents, information regarding the project's database, and the minutes for our meetings can be found here.
## Source
The source files for Typing Trainer
The Flask application is set-up and ran through app.py. All requests to the website go through here.
Database interaction can be found in db_interaction.py
Markov-related code can be found in the \*Markov\*.py files
Text scraping performed using gutenbergScraper.py
Generation of charts for followed user's on profile page in friendsChart.py
## static
CSS files that are used to style the site's pages.
JS files that control much of the user interaction on the front, game/practice, and profile page.
### assets
GIF presented on visiting the site on a screen with a size yet unsupported.
## template
This HTML files that flask will render to are stored here. The names indicate their usage.
## TextGeneration
The texts that have been used for the project so far are in the Texts folder, and the frequency dictionaries for the texts are stored in FrequencyDictionaries in JSON format
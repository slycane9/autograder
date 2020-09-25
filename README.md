# Autograder Steup Instructions
This guide will detail how to set up your github repo for the autograder.  You will need to invite me (@slycane9) to your github repo for the grader to work properly.

Here is a link to the google sheets file where you can put your github repo and your name:
https://docs.google.com/spreadsheets/d/1Z6nc8QDHd4FtZNdhCr0m63m6mj_1eHoAM14bajcj480/edit?usp=sharing

## Github Webhooks
**Do not do this step at the moment.  I will message on slack when I have everyone's grader set up, then do this step.**

For the autograder to detect your git push, go to your github repo's settings>webhooks page and add a webhook.

Set the url to https://smee.io/beguEj0YpuDKLg5x, and make sure the content type is application/json.  At the bottom make sure to check the button saying "Send me everything".

## Jenkinsfile
The final step of your setup will be adding a Jenkinsfile to your repos root directory.  Copy the file contained in this repo for lab 1 and make sure it is named "Jenkinsfile" in your repo.

Edit your file so that your email address you want your results to be sent to are in the sections labeled "put your email address here".

**For the grader to work, your newsapp directory (the one that contains your manage.py file) should be accesible from your repo's root directory (Just like my Jenkinsfiles directory is accesible in this repos root directory)**

## Submitting your Lab
The grader will not run unless you have a file named "submit.txt" in your repo's root directory.  The content of this file does not matter it just needs to exist.

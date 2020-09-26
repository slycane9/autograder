# Autograder Steup Instructions
This guide will detail how to set up your github repo for the autograder.  You will need to invite me (@slycane9) to your github repo for the grader to work properly.

Here is a link to the google sheets file where you should put your github repo and your name:
https://docs.google.com/spreadsheets/d/1Z6nc8QDHd4FtZNdhCr0m63m6mj_1eHoAM14bajcj480/edit?usp=sharing

## Github Webhooks
**There have been bugs where webhooks created before I setup your pipeline have not worked, to be safe wait until your google sheets entry has been marked complete before creating your webhook.  I will mark how far I've gotten in the sheet so you can see if your pipeline is setup.**

For the autograder to detect your git push, go to your github repo's settings>webhooks page and add a webhook.

Set the url to https://smee.io/beguEj0YpuDKLg5x, and make sure the content type is application/json.  At the bottom make sure to check the button saying "Send me everything".

## Jenkinsfile
The next step of your setup will be adding a Jenkinsfile to your repos root directory.  Copy the file contained in this repo for lab 1 and make sure it is named "Jenkinsfile" and is located in the root directory of your repo.

Edit your file's contents so that the email address you want your results to be sent to are in the sections labeled "put your email address here".

**For the grader to work, your newsapp directory (the one that contains your manage.py file) should be accesible from your repo's root directory (Just like my Jenkinsfiles directory is accesible in this repos root directory)**

## Submitting your Lab
Finally, the grader will not run unless you have a file named "submit.txt" in your repo's root directory.  The content of this file does not matter it just needs to exist.

## Extra Notes
If you include the given testing script (test1.py) in your repo files, it will be run if my pipeline can't find it in the newsapp, newsapp/newsapp, or newsapp/newslister directory.  If you don't want it to get run and potentially fail your build, don't include it anywhere else but those locations.

Fortunately once this is all setup for lab1, you wont have to do anything for any other labs except swap to the correct Jenkinsfile (that I will provide as the labs come out).

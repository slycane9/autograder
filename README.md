# Autograder Steup Instructions
This guide will detail how to set up your github repo for the autograder.  You will need to invite me (@slycane9) to your github repo for the grader to work properly.

Here is a link to the google sheets file where you should put your github repo and your name:
https://docs.google.com/spreadsheets/d/1Z6nc8QDHd4FtZNdhCr0m63m6mj_1eHoAM14bajcj480/edit?usp=sharing

## Github Webhooks
**Your github webhook will not work if I haven't manually run your pipeline while your git repo had a Jenkinsfile in it.  If you are not getting results from your git push, message me to run your pipeline after you make sure you have the Jenkinsfile in your repo.**

For the autograder to detect your git push, go to your github repo's settings>webhooks page and add a webhook.

Set the url to https://smee.io/beguEj0YpuDKLg5x, and make sure the content type is application/json.  At the bottom make sure to check the button saying "Send me everything".

## Jenkinsfile and Repo Configurations
The next step of your setup will be adding a Jenkinsfile to your repos root directory.  Copy the file contained in this repo for lab 1 and make sure it is named "Jenkinsfile" and is located in the root directory of your repo.

Jenkinsfile Modifications:

Make sure to edit your jenkinsfile's contents so that the email address you want your results to be sent to are in the sections labeled "put your email address here".

Add any python modules your program needs in the testing phase of the file, for example below the line "pipenv run pip install cryptography" I would add "pipenv run pip install pandas" if my code needed pandas to run.

**For the grader to work, your newsapp directory (the one that contains your manage.py file) should be accesible from your repo's root directory (Just like my Jenkinsfiles directory is accesible in this repos root directory)**

**If you include any test*.py files, django will run them along with the official test files I drop in your repo.  If you don't want your build to fail make sure when the pipeline runs your test file that your code passes them.  The best way to organize this is to have "tests.py" in your "newslister" folder contain your local tests since my script replaces that file with the official testing file.**

## Submitting your Lab
Finally, the grader will not run unless you have a file named "submit.txt" in your repo's root directory.  The content of this file does not matter it just needs to exist.

## Extra Notes

Fortunately once this is all setup for lab1, you wont have to do anything for any other labs except swap to the correct Jenkinsfile (that I will provide as the labs come out).

## Common Bugs

Extra test.py file in repo that causes two test suites to be run (22 tests) and fail the nru test.  Make sure your local test file is in newslister/tests.py

Python 3.8 required in pipfile, change it to 3.6

Make sure you have the most current Jenkinsfile in your repo with submit.txt, and make sure you it named exactly "Jenkinsfile" without the lab 1 appended to the name.

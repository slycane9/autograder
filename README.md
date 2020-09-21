# Autograder Steup Instructions
This guide will detail how to set up your github repo for the autograder.  You will not need to invite me to your github repo for the grader to work properly.

## What I Need
I need the following message from you, please send it to my (Serdjan Rolovic) canvas email.

ssh private key: abcd123

git repo: git@github.com:username/repo.git

name: John Smith

## How to generate the ssh private key
Go to any linux terminal and run
```
ssh-keygen
```
This will generate you two files, id_rsa and id_rsa.pub, send me the private key (id_rsa) in your message to me.

Then go to your github repo and access settings>deploykeys.  Add a key and put in the id_rsa.pub contents as key value.

**When you send me your private key please include the entire contents (including the header and footer)**

## Github Webhooks
For the autograder to detect your git push, go to your github repo's settings>webhooks page and add a webhook.

Set the url to https://smee.io/beguEj0YpuDKLg5x, and make sure the content type is application/json.  At the bottom make sure to check the button saying "Send me everything".

## JenkinsFile
The final step of your setup will be adding a JenkinsFile to your repos root directory.  Copy the file contained in this repo for lab 1 and make sure it is named "JenkinsFile" in your repo.

Edit your file so that your email address you want your results to be sent to are in the sections labeled "put your email address here".

**For the grader to work, your newsapp directory (the one that contains your manage.py file) should be accesible from your repo's root directory (Just like my JenkinsFiles directory is accesible in this repos root directory)**

## Submitting your Lab
The grader will not run unless you have a file named "submit.txt" in your repo's root directory.  The content of this file does not matter it just needs to exist.

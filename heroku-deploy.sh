#!/bin/bash


if [ $# -eq 0 ]; then 
    echo -e "[!] commit message missing"
    echo -e "Usage: $0 \"your message\""
    exit
fi

commit_message=$1

git add .
git commit -S -am "${commit_message}"
git push heroku master

echo -e "[*] Don't forget to add repo to heroku using: heroku git:remote -a <app-name>"

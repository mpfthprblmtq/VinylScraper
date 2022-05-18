clear
rm -r deploy.zip
pip install --target ./package praw
pip install --target ./package tweepy
cd package
zip -r ../deploy.zip .
cd ..
zip -g deploy.zip lambda_function.py
zip -g deploy.zip __users/*
zip -g deploy.zip _objects/*
zip -g deploy.zip _services/*
zip -g deploy.zip _utils/*
zip -g deploy.zip app_info.json
rm -r package

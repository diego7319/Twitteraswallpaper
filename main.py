import mechanicalsoup
import os
from requests import Session
import requests
import time
from re import sub as cleanlines
import ctypes

from PIL import Image, ImageDraw, ImageFont
import ClassObjects as ClassObjects

TWITTER_HOME = "https://mobile.twitter.com/home"

if __name__ == "__main__":
    conf_file = ClassObjects.config_file()
    # Create a browser object
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
    # request Twitter login page
    if not conf_file.check_conf_file():
        print("Creating a twitter session, user and password will not be stored.")
        username_twitter = input("Enter your username: \n")
        password_twitter = input("Enter your password: \n")
        created_conf_file = conf_file.create_cookie_twitter(username_twitter,password_twitter)
        if created_conf_file:
            print("cookie created successfully")
        else:
            print("Error while creating the cookie")

    browser.session.cookies = conf_file.get_cookie_twitter()
    browser.open(TWITTER_HOME)
    browser.follow_link("/")
    page = browser.get_current_page()
    page.find_all('table', class_='tweet')
    tweets_in_list=[]
    tweets_in_table = page.find_all('table', class_='tweet')[0:6]
    #adding a tweet object to a list
    w = ClassObjects.WallpaperEngine()
    #For first run
    dummy_tweet  = ClassObjects.Tweet("","","","","","","")
    #save objects tweet
    tweets_in_list=[]
    tweets_in_list.append(dummy_tweet)
    while True:
        browser.open(TWITTER_HOME)
        browser.follow_link("/")
        browser.get_current_page()
        page = browser.get_current_page()
        page.find_all('table', class_='tweet')
        tweets_in_table = page.find_all('table', class_='tweet')[0:6]

        #First tweet for the next step
        #validate if there's any new tweet (compare tweetid)
        first_tweet_id = (((tweets_in_table[0].get('href')).split("/"))[3]).split("?p=v")[0]
        print((first_tweet_id) +"---"+ tweets_in_list[0].get_tweetid())
        if first_tweet_id.strip() != tweets_in_list[0].get_tweetid().strip():
            tweets_in_list = []
            for single_tweet in tweets_in_table:
            #is it a retweet?
                is_retweet = ""
                tweet_text = "Empty"
                tweet_user_image_http = "Empty"
                tweet_user_fullname = "Empty"
                tweet_user_account = "Empty"
                tweet_id = "Empty"
                if len(single_tweet.find_all('tr', class_='tweet-content'))> 0:
                    is_retweet = single_tweet.find('span', class_="context").text+"\n"
                tweet_user_fullname = single_tweet.find('img', alt=True)["alt"]
                tweet_user_image_http = single_tweet.find('img', alt=True)["src"]
                tweet_user_account = single_tweet.find('div', class_='username').text
                #clean double or triple \n from the tweet text body
                tweet_text = cleanlines(r'\n\s*\n', '\n',(single_tweet.find("div", class_='dir-ltr').text))
                tweet_id = (((single_tweet.get('href')).split("/"))[3]).split("?p=v")[0]
                tweet_obj = ClassObjects.Tweet(tweet_user_fullname.strip(),tweet_user_account.strip(),
                                  tweet_text.strip(),"image-body",tweet_user_image_http,
                                  is_retweet.strip(), tweet_id)
                tweets_in_list.append(tweet_obj)
            #print (len(tweets_in_list))
            w.add_tweets_toImg(tweets_in_list)
            w.setWallpaper(str(os.getcwd()+"/file.png"))
        time.sleep(3)
        #w.setWallpaper("test.png")
        #ctypes.windll.user32.SystemParametersInfoW(20,0,os.getcwd()+"/test.png",3)

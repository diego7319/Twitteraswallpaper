import mechanicalsoup
import requests,os
import time
from re import sub as cleanlines
import ctypes
from PIL import Image, ImageDraw, ImageFont
import Twitteraswallpaper.ClassObjects as ClassObjects
import shutil
import copy
import Twitteraswallpaper.utils
TWITTER_HOME = "https://mobile.twitter.com/home"


def fix_string_toScreen(paragraph):
    position_break = 35
    if len(paragraph) < position_break:
        return paragraph
    num = [pos for pos, char in enumerate(paragraph) if char == " "]
    if len(num) == 1:
        paragraph.replace(" ","\n",0)
        return paragraph
    status = True
    while status:
        position = [x for x in num if x<=position_break]
        #print (str(x) +" --"+str(x))
        paragraph = paragraph[:position[-1]]+ "\n" +paragraph[(position[-1]+1):]
        return paragraph


if __name__ == "__main__":
    #detect {-}
    connection_handler = ClassObjects.Connection_handler()
    # Create a browser object
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
    # request Twitter login page
    if not connection_handler.check_conf_file():
        print("Creating a twitter session, user and password will not be stored.")
        username_twitter = input("Enter your username: \n")
        password_twitter = input("Enter your password: \n")
        connection_newcookie = connection_handler.create_cookie_twitter(username_twitter,password_twitter)
        if connection_newcookie:
            print("cookie created successfully")
        else:
            print("Error while creating the cookie")

    browser.session.cookies = connection_handler.get_cookie_twitter()
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
    #transfer WallpaperEngine
    d=os.getenv('APPDATA')+"//Microsoft//Windows//Themes//TranscodedWallpaper"
    shutil.copy(d,"test.png")
    image = Image.open("test.png").convert('RGB')
    while True:
        browser.open(TWITTER_HOME)
        browser.follow_link("/")
        browser.get_current_page()
        page = browser.get_current_page()
        page.find_all('table', class_='tweet')
        tweets_in_table = page.find_all('table', class_='tweet')[0:8]

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
            ht=w.add_tweets_toImg(tweets_in_list, copy.deepcopy(image))
            w.setWallpaper(str(os.getcwd()+"/background.png"))
        time.sleep(3)

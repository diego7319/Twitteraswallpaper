import mechanicalsoup
import json
import os
from requests import Session
import requests
import time
from re import sub as cleanlines
import ctypes
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

LOGIN_PAGE = "https://mobile.twitter.com/login"
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)'
}

class config_file():
    def __init__(self):
        self._file_path = "conf.json"

    def check_conf_file(self):
        import os
        if os.path.exists(self._file_path) and os.path.getsize(self._file_path) > 40:
            return True
        else:
            return False

    def save_cookie_twitter(self,Browser):
        cookie_dict = Browser.session.cookies.get_dict()
        with open(self._file_path, 'w') as conffile:
            json.dump(cookie_dict, conffile)
        if self.check_conf_file():
            return True
        else:
            raise Exception("Error while saving file")

    def create_cookie_twitter(self, username, password):
        headers = {
            """User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)"""
        }
        URL_TWITTER_LOGIN= "https://twitter.com/sessions"
        data = {"session[username_or_email]": username,
                "session[password]": password,
                "scribe_log": "",
                "redirect_after_login": "/",
                "remember_me": "1"}
        browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
        browser.open(URL_TWITTER_LOGIN)
        browser.select_form('form[action="https://twitter.com/sessions"]')
        browser["session[username_or_email]"] = username
        browser["session[password]"] = password
        response = browser.submit_selected()
        # get current page output
        response_after_login = browser.get_current_page()
        browser.follow_link("/")
        if self.save_cookie_twitter(browser):
            return True
        else:
            return False


    def get_cookie_twitter(self):
        if self.check_conf_file():
            from requests.utils import cookiejar_from_dict
            cookiefileloaded = ""
            from requests.utils import cookiejar_from_dict
            cookiefileloaded = json.load( open(self._file_path))
            return cookiejar_from_dict(cookiefileloaded)
        else:
            return False

class Tweet:
    def __init__(self,nameAccount,accountusername,text_body,image_body,profile_image,retweet_status,tweet_id):
        self.nameAccount = nameAccount
        self.accountusername = accountusername
        self.text_body = text_body
        self.image_body = image_body
        self.profile_image = profile_image
        self.retweet_status = retweet_status
        self.tweet_id = tweet_id
    def get_tweetid(self):
        return self.tweet_id


class WallpaperEngine:
    #hardcoded for windwows
    def setWallpaper(self,path):
        ctypes.windll.user32.SystemParametersInfoW(20,0,path,3)
    def add_tweets_toImg(self,list_tweets):
        entireTweets=""
        for element in list_tweets:
            if element.retweet_status:
                entireTweets = entireTweets + element.retweet_status+"\n"
            entireTweets = entireTweets+"\n"+ element.accountusername + "----->"+element.nameAccount+"\n"
            entireTweets = entireTweets + element.text_body+"\n"
            entireTweets = entireTweets + "\n"+("*"*150) + "\n"
        file = BytesIO()
        #imagen de fondo
        image = Image.new('RGBA', size=(1920, 1080), color=(0, 0, 0))
        fnt = ImageFont.truetype('Symbola_hint.ttf', 20)
        txt = Image.new('RGBA', image.size, (255,255,255,255))
        d = ImageDraw.Draw(txt)
        #txt = Image.new('RGBA', base.size, (255,255,255,0))
        # draw text, half opacity
        d.text((900,10), entireTweets, font=fnt, fill=(0,0,0,0))
        # draw text, full opacity
        out = Image.alpha_composite(image, txt)
        out.save("file.png")
        #image.save("test",'png')
        #file.name = 'test.png'
        #file.seek(0)


if __name__ == "__main__":
    conf_file = config_file()
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
    browser.open("https://mobile.twitter.com/home")
    browser.follow_link("/")
    page = browser.get_current_page()
    browser.get_current_page()
    #browser.launch_browser()
    #[x.extract() for x in page.findAll('script')]
    page.find_all('table', class_='tweet')
    tweets_in_list=[]
    tweets_in_table = page.find_all('table', class_='tweet')[0:6]
    #adding a tweet object to a list
    w = WallpaperEngine()
    dummy_tweet  =Tweet("","","","","","","")
    #save objects tweet
    tweets_in_list=[]
    tweets_in_list.append(dummy_tweet)
    while True:

        #browser.launch_browser()
        #[x.extract() for x in page.findAll('script')]
        #page.find_all('table', class_='tweet')
        browser.open("https://mobile.twitter.com/home")
        browser.follow_link("/")
        #browser.refresh()
        browser.get_current_page()
        #browser.launch_browser()
        #[x.extract() for x in page.findAll('script')]
        page = browser.get_current_page()
        #browser.launch_browser()
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
                #print(tweet_id)
                tweet_user_fullname = single_tweet.find('img', alt=True)["alt"]
                tweet_user_image_http = single_tweet.find('img', alt=True)["src"]
                tweet_user_account = single_tweet.find('div', class_='username').text
                #clean double or triple \n from the tweet text body
                tweet_text = cleanlines(r'\n\s*\n', '\n',(single_tweet.find("div", class_='dir-ltr').text))
                tweet_id = (((single_tweet.get('href')).split("/"))[3]).split("?p=v")[0]
                tweet_obj = Tweet(tweet_user_fullname.strip(),tweet_user_account.strip(),
                                  tweet_text.strip(),"image-body",tweet_user_image_http,
                                  is_retweet.strip(), tweet_id)
                tweets_in_list.append(tweet_obj)
            print (len(tweets_in_list))
            w.add_tweets_toImg(tweets_in_list)
            w.setWallpaper(str(os.getcwd()+"/file.png"))
        time.sleep(3)
        #w.setWallpaper("test.png")
        #ctypes.windll.user32.SystemParametersInfoW(20,0,os.getcwd()+"/test.png",3)

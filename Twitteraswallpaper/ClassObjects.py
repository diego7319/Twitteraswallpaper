import mechanicalsoup
import json
import os
#from requests import Session
import requests
import ctypes
from PIL import Image, ImageDraw, ImageFont
import textwrap

class Connection_handler():
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
        try:
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
        except:
            return "Error while creating session cookie, check internet connection."

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
"""
    #adds jumplines to adjust tweets to the screen (currently hardcoded for fullhd)
    def fix_string_toScreen(self, charBreak):
        #charBreak is the chart's position where a jumpline will be added
        paragraph = self.text_body
        charBreak = 35
        if len(paragraph) < charBreak:
            return paragraph
        num = [pos for pos, char in enumerate(paragraph) if char == " "]
        if len(num) == 1:
            paragraph.replace(" ","\n",0)
            return paragraph
        status = True
        while status:
            position = [x for x in num if x <= charBreak]
            #print (str(x) +" --"+str(x))
            paragraph = paragraph[:position[-1]]+ "\n" +paragraph[(position[-1]+1):]
            return paragraph
"""

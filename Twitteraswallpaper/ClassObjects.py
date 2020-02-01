import mechanicalsoup
import json
import os
from requests.utils import cookiejar_from_dict
#from requests import Session


class Connection_handler():
    def __init__(self):
        self._file_path = "conf.json"

    def check_conf_file(self):
        import os
        if os.path.exists(self._file_path) and os.path.getsize(self._file_path) > 40:
            return True
        else:
            return False

    def save_cookie_twitter(self,browser):
        cookie_dict = browser.session.cookies.get_dict()
        with open(self._file_path, 'w') as conffile:
            json.dump(cookie_dict, conffile)
        if self.check_conf_file():
            return True
        else:
            raise Exception("Error while saving file")

    def create_cookie_twitter(self, username, password,browser):
        headers = {
            """User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)"""
        }
        URL_TWITTER_LOGIN= "https://twitter.com/sessions"
        data = {"session[username_or_email]": username,
                "session[password]": password,
                "scribe_log": "",
                "redirect_after_login": "/",
                "remember_me": "1"}
        try:
            browser.open(URL_TWITTER_LOGIN)
            browser.select_form('form[action="https://twitter.com/sessions"]')
            browser["session[username_or_email]"] = username
            browser["session[password]"] = password
            response = browser.submit_selected()
            # get current page output
            response_after_login = browser.get_current_page()
            #print(browser.launch_browser())
            if browser.get_url() == "https://twitter.com/":
                browser.follow_link("/")
                if self.save_cookie_twitter(browser):
                    return True
                else:
                    raise Exception("Error while saving the cookie. Check directory/files permissions.")
            else:
                return False
        except:
            raise Exception("Error while creating session , check internet connection.")

    def get_cookie_twitter(self):
        try:
            if self.check_conf_file():
                cookiefileloaded = json.load(open(self._file_path))
                return cookiejar_from_dict(cookiefileloaded)
        except:
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

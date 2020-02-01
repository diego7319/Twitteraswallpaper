import platform, os, shutil, copy
import ctypes
from PIL import Image, ImageDraw, ImageFont
import textwrap
from re import sub as cleanlines
from Twitteraswallpaper import ClassObjects

class windows_util():
    def __init__(self):
        pass
    #gets the current wallpaper and saves it to avoid modifying the original.
    def get_baseWallpaper(self):
        try:
            d = os.getenv('APPDATA')+"//Microsoft//Windows//Themes//TranscodedWallpaper"
            shutil.copy(d,"baseWallpaper.png")
        except:
            return "Error while getting the original wallpaper"
    #returns a copy of the original image to be writed
    def get_image_object(self):
        image = Image.open("baseWallpaper.png").convert('RGB')
        return copy.deepcopy(image)

    def set_wallpaper(self, filename):
        ctypes.windll.user32.SystemParametersInfoW(20,0,filename,3)

#example
class gnome():
    def get_baseWallpaper():
        pass
    def set_wallpaper():
        pass


def get_system_util():
    if platform.system()== 'Windows':
        new_system = windows_util()
        return new_system
    elif platform.system() == 'linux':
        raise Exception("Linux is not supportet yet.")
    else:
        raise Exception("Operating System not recognized.")

class Twitter_scraper():
    def __init__(self, browser, list_tweets):
        self.browser = browser
        self.TWITTER_HOME = "https://mobile.twitter.com/home"
        self.list_tweets = list_tweets
        self.new_tweets_status = True

    def get_tweetsObj_list(self,current_list):
        self.browser.open(self.TWITTER_HOME)
        self.browser.follow_link("/")
        self.browser.get_current_page()
        page = self.browser.get_current_page()
        #getting tweets from the browser
        page.find_all('table', class_='tweet')
        tweets_in_table = page.find_all('table', class_='tweet')[0:8]
        #validate if there's any new tweet (compare tweetid)
        first_tweet_id = (((tweets_in_table[0].get('href')).split("/"))[3]).split("?p=v")[0]
        #print((first_tweet_id) +"---"+ tweets_in_list[0].get_tweetid())
        if first_tweet_id.strip() != self.list_tweets[0].get_tweetid().strip():
            new_tweets_in_list = []
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

                tweet_obj = ClassObjects.Tweet(tweet_user_fullname.strip(),
                                               tweet_user_account.strip(),
                                               tweet_text.strip(),
                                               "image-body",
                                               tweet_user_image_http,
                                               is_retweet.strip(),
                                               tweet_id)
                new_tweets_in_list.append(tweet_obj)
            self.list_tweets = new_tweets_in_list
            self.new_tweets_status = True
        else:
            #False if there are not new tweets
            self.new_tweets_status = False


class WallpaperEngine():
    def __init__(self, system_util):
        self.system_util = system_util
    #hardcoded for windwows
    def custom_size_body(self, textbody, maxlen):
        textbody = textbody
        #break line after x letters, in case is mostly caps, it will use more space
        if (sum(1 for x in textbody if x.isupper()) / len(textbody))*100>40:
            #0.73 of the total len if percetange of upper case is over 40%
            return textwrap.fill(textbody,int(maxlen*0.73))
        else:
            return textwrap.fill(textbody,maxlen)
    def setWallpaper(self,path):
        ctypes.windll.user32.SystemParametersInfoW(20,0,path,3)
    def add_parag_toImg(self,list_tweets,img,position):
        entireTweets=""
        for element in list_tweets:
            if element.retweet_status:
                entireTweets = entireTweets + element.retweet_status+"\n"
            entireTweets = entireTweets+"\n"+ element.accountusername + u" \u2192 "+element.nameAccount+"\n"
            entireTweets = entireTweets + self.custom_size_body(element.text_body,70)+"\n"
            entireTweets = entireTweets + "\n"+("*"*71) + "\n"
        fnt = ImageFont.truetype('Symbola_hint.ttf', 21)
        draw_image = ImageDraw.Draw(img)
        draw_image.text(position, entireTweets, font=fnt,fill='white')
        img.save("newwallpaper.png")

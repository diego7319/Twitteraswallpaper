import platform, os, shutil
import ctypes

class windows_util():
    def get_baseWallpaper():
        #gets the current wallpaper and saves it to avoid modifying the original.
        try:
            d = os.getenv('APPDATA')+"//Microsoft//Windows//Themes//TranscodedWallpaper"
            shutil.copy(d,"originalbackground.png")
        except:
            return "Error while getting the original wallpaper"
    #returns a copy of the original image to be writed
    def get_image_object(self):
        return image
    def set_wallpaper(self,filename):
        ctypes.windll.user32.SystemParametersInfoW(20,0,filename,3)

class gnome():
    def get_baseWallpaper():
        pass
    def set_wallpaper():
        pass


def get_system_util(self):
    if platform.system()== 'windows':
        return windows_util()
    elif platform.system() == 'linux':
        raise Exception("Linux is not supportet yet.")
    else:
        raise Exception("Operating System not recognized.")


class WallpaperEngine(system_util):
    def __init__(self):
        self.system_util = system_util
    #hardcoded for windwows
    def custom_size_body(self, textbody, maxlen):
        textbody = textbody
        #break line after x letters, in case is mostly caps, it will use more space
        if (sum(1 for x in textbody if x.isupper()) / len(textbody))*100>40:
            #0.8 of the total len if percetange of upper case is over 40%
            return textwrap.fill(textbody,int(maxlen*0.73))
        else:
            return textwrap.fill(textbody,maxlen)
    def setWallpaper(self,path):
        ctypes.windll.user32.SystemParametersInfoW(20,0,path,3)
    def add_parag_toImg(self,list_tweets,img_path,position):
        entireTweets=""
        for element in list_tweets:
            if element.retweet_status:
                entireTweets = entireTweets + element.retweet_status+"\n"
            entireTweets = entireTweets+"\n"+ element.accountusername + u" \u2192 "+element.nameAccount+"\n"
            entireTweets = entireTweets + self.custom_size_body(element.text_body,70)+"\n"
            entireTweets = entireTweets + "\n"+("*"*71) + "\n"
        fnt = ImageFont.truetype('Symbola_hint.ttf', 22)
        d = ImageDraw.Draw(img_path)
        d.text((1200,30), entireTweets, font=fnt,fill='white')
        d.text((1200,30), entireTweets, font=fnt,fill='white')
        # draw text, full opacity
        #out = Image.alpha_composite(image, d)
        #img_path.save("background.png")
        return d

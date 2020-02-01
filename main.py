import mechanicalsoup
import os, time, sys
from getpass import getpass
import Twitteraswallpaper.ClassObjects as ClassObjects
import Twitteraswallpaper.utils as utils


if __name__ == "__main__":
    #Manages the connection with twitter to sign in or  log in withs cookies
    connection_handler = ClassObjects.Connection_handler()
    # Create a browser object that will be passed to other functions
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})
    # number of logins
    tries = 0; session_created = False
    # if conf file doesnt exists (first time user)
    while (not connection_handler.check_conf_file()) and (not session_created):
        print("Creating a twitter session, user and password will not be stored.")
        tries = tries + 1
        print("\nTry " + str(tries) + " of  3")
        username_twitter = input("Enter your username: \n")
        password_twitter = getpass("Enter your password: ")
        connection_newcookie = connection_handler.create_cookie_twitter(username_twitter,password_twitter,browser)
        if connection_newcookie:
            print("Session created successfully.")
        else:
            if tries == 3:
                print("Number of tries exceded. Closing program ...")
                sys.exit(0)
            print("\nError while creating the session, try again.")

    #Variables for first run
    tweets_in_list=[]
    wallpaper_engine = utils.WallpaperEngine(utils.get_system_util())
    dummy_tweet  = ClassObjects.Tweet("","","","","","","")
    tweets_in_list.append(dummy_tweet)
    #Creating an object to handle background images depending on the OS
    wallpaper_handler = utils.get_system_util()
    #gets the current wallpaper and saves it to avoid modifying the original.
    wallpaper_handler.get_baseWallpaper()
    #Position in the image from where the tweets will be added
    text_position_in_image = (1230,30)
    #Creating a new connection to twitter using saved cookies
    browser.session.cookies = connection_handler.get_cookie_twitter()
    #Get the twitter scrapper class
    twitter_scrap = utils.Twitter_scraper(browser, tweets_in_list)

    while True:
        try:
            twitter_scrap.get_tweetsObj_list(tweets_in_list)
            if twitter_scrap.new_tweets_status:
                wallpaper_engine.add_parag_toImg(twitter_scrap.list_tweets,
                                                 wallpaper_handler.get_image_object(),
                                                 text_position_in_image)
                wallpaper_handler.set_wallpaper(os.getcwd()+r"\\newwallpaper.png")
                #ctypes.windll.user32.SystemParametersInfoW(0x14,0,r"newwallpaper.png",0)
            time.sleep(3)
        except:
            wallpaper_handler.set_wallpaper(os.getcwd()+r"\\baseWallpaper.png")
            sys.exit(0)

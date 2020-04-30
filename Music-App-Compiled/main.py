from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import random
import tkinter as tk
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class FindVideos:
    
    def __init__(self):
        options = Options()
        options.add_extension(resource_path('.\\driver\\ublock.crx'))
        self.__driver = webdriver.Chrome(executable_path=resource_path('.\\driver\\chromedriver.exe'), chrome_options=options)
        self._vidList = []
        self.clonedList = []

    def startUp(self):
        self.__driver = webdriver.Chrome()

    def getVideos(self, playlistURLList):
        for playlistURL in playlistURLList:
            self.__driver.get(playlistURL)
            vidLength = int((self.__driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/div[1]/yt-formatted-string[1]").text).split(" ")[0])

            scrollNum = round(vidLength/100)
            for _ in range(scrollNum):
                self.__driver.find_element_by_tag_name('body').send_keys(Keys.END)
                sleep(0.5)

            source = self.__driver.page_source
            soup = BeautifulSoup(source, features='html5lib')

            videos = soup.find_all('ytd-playlist-video-renderer', {'class': 'style-scope ytd-playlist-video-list-renderer'})
            for video in videos:
                a = video.find('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
                span = video.find('span', {'id': 'video-title'})
                try:
                    url = (a['href'].split("&"))[0]
                    title = span['title']
                    if (url, title) not in self._vidList:
                        self._vidList.append((url, title))
                except:
                    pass

    # Make sure it cannot exceed 100...
    def isFinished(self):        
        for i in range(1, 101):
            try:
                self.__driver.find_element_by_xpath(f'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[{i}]/span[2]/span[1]/button').click()
                return True
            except:
                pass
        return False

    def pause(self):
        for i in range(1, 101):
            try:
                self.__driver.find_element_by_xpath(f'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[{i}]/div[2]/div[1]/button').click()
                return True
            except:
                pass
        return False

    def loadVideo(self, url):
        self.__driver.get("https://youtube.com"+url)

    def close(self):
        self.__driver.close()

if __name__ == "__main__":

    x = FindVideos()
    root = tk.Tk()
    root.title("Youtube improved shuffler - By Ben Osborn")

    title = tk.Label(root, text="Youtube improved shuffler - By Ben Osborn")
    title.pack()

    def check():
        result = x.isFinished()
        if result:
            getVideo()
        root.after(3000, check)
    check()

    instructions = tk.Label(root, text="Enter your playlist URL in the field below then press the 'Submit' button to get started. To enter multiple URL's seperate them with a comma. ")
    instructions.pack()

    linkEntry = tk.Entry(root, width=100)
    linkEntry.pack()

    current = tk.Label(root, text="Commencing...")

    def enterURLS():
        try:
            url = linkEntry.get()
            urls = [ul.strip() for ul in url.split(",")]
            x.getVideos(urls)
            linkEntry.destroy()
            submit.destroy()
            instructions.destroy()
            error.destroy()
            current.pack()
            skip.pack()
            pause.pack()
            current.pack()
            getVideo()
        except:
            x._vidList = []
            error.pack()

    submit = tk.Button(root, text="Submit", command=enterURLS)
    submit.pack()

    error = tk.Label(root, text="Error with URL's, please try again.")

    def getVideo():
        if len(x.clonedList) == 0:
            x.clonedList = x._vidList.copy()
        choice = random.choice(x.clonedList)
        x.clonedList.remove(choice)
        x.loadVideo(choice[0])
        current.configure(text=choice[1])

    def pause():
        x.pause()

    skip = tk.Button(root, text="Skip", command=getVideo)
    pause = tk.Button(root, text="Pause/Play", command=pause)

    root.mainloop()
    x.close()

# https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/
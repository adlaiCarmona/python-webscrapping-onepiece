from keyboard import send
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from time import sleep

import sys

# this url is for the menu of every episode
# url = 'https://allwish.me/episode/one-piece-episodes-english-sub/'

# this url is the base of any episode
# url = 'https://btcwet.com/onepieceDubep'

class ScreenerBot:
    def __init__(self) -> None:
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        # try chrome headless, or chrome to see if it doesnt need vvv load timeout and down + enter to download
        self.driver.set_page_load_timeout(10)
        
        self.getLinkButton = '/html/body/div[1]/div/div/div/div[3]/a'
        self.downloadNormalQuality = '/html/body/div[3]/div/table/tbody/tr[2]/td[1]/a'
        self.downloadHighQuality = '/html/body/div[3]/div/table/tbody/tr[3]/td[1]/a'
        self.downloadVideo = '/html/body/div[3]/div/center/form/button'
        self.directDownload = '/html/body/div[3]/div/span/a'
        self.saveButton = False
    
    def goToUrl(self, url):
        self.driver.get(url)
        sleep(2)

    def downloadEpisodes(self):
        for ep in episodes:
            # goes to url of ep
            self.goToUrl(url + str(ep))

            # needs to wait until link is available + 1 sec if it takes too much to load page
            sleep(6)

            # gets link button href
            while True:
                downloadUrl = self.driver.find_element_by_xpath(self.getLinkButton).get_attribute("href")
                if len(downloadUrl) != len('https://sbembed.me/'+'.html'):
                    print(downloadUrl)
                    break
                print('getLinkButton not ready, waiting 1 sec and trying again')
                sleep(1)

            # gets download link
            downloadLink = 'https://sbembed.me/d/' + downloadUrl[len('https://sbembed.me/'):len('.html')*-1] + '#'

            # goes to real downloadLink
            self.goToUrl(downloadLink)
            sleep(1)
            try:
                self.driver.find_element_by_xpath(self.downloadHighQuality).click()
            except:
                print(f'Episode {ep} will be normal quality')
                self.driver.find_element_by_xpath(self.downloadNormalQuality).click()

            # presses download button
            self.driver.find_element_by_xpath(self.downloadVideo).click()
            sleep(2)

            # gets link from direct download button
            downloadUrl = self.driver.find_element_by_xpath(self.directDownload).get_attribute("href")

            # download the file (finally!)
            try:
                self.goToUrl(downloadUrl)
            except Exception as e:
                print(e)
            # to use if using firefox
            #sleep(1)
            #if not self.saveButton:
            #    send('down')
            #    self.saveButton = True
            #send('enter')

            print(f'downloading episode {ep}')
        print('All episodes downloading...')


if len(sys.argv) == 1:
    sys.exit('Usage: onePiece.py first-episode final-episode')
elif len(sys.argv) == 2:
    # just append number of episode to here
    url = 'https://btcwet.com/onepieceDubep'
    
    # this is the episode to download
    try:
        start = int(sys.argv[1])
    except:
        sys.exit('first-episode is supposed to be a number')

    episodes = [start]
else:
    # just append number of episode to here
    url = 'https://btcwet.com/onepieceDubep'

    try:
        # this is the first episode to download
        start = int(sys.argv[1])
        # this is the final episode to download
        end = int(sys.argv[2])
    except:
        sys.exit('first-episode and final-episode are supposed to be numbers')

    episodes = list(range(start, end + 1))

myBot = ScreenerBot()
myBot.downloadEpisodes()
"""
MIT License

Copyright (c) 2020 Monksc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys

import time
import json
import random
import PIL.Image
import os
import filecmp

def getRandomString():
    s = ""
    for i in range(20):
        s += random.choice("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")
    return s


class BumbleBot:
    def getElementXPath(self, xpath, count=180):
        while True:
            try:
                 element = self.driver.find_elements(By.XPATH, xpath)
                 return element
            except:
                count -= 1
                if count == 0:
                    return None
                time.sleep(1)


    def login(self):
        login_btn = self.getElementXPath('/html/body/div[2]/div/div/div/div/div[3]/div[1]/button', count=3)
        
        if login_btn == None:
            #self.swipeStage()
            return


        # havnt really solved loggin in yet
        login_btn.click()

        phoneNumberTXTField = self.getElementXPath('/html/body/div[2]/div/div/div[2]/div[2]/div/input')
        phoneNumberTXTField.send_keys(phoneNumber)

    def swipeLeft(self):
        swipe_left_btn = self.getElementXPath('//div[@class="encounters-action tooltip-activator encounters-action--dislike"]', count=3)[0]
        swipe_left_btn.click()
        self.swipeLeftCount += 1

    def swipeRight(self):
        swipe_right_btn = self.getElementXPath('//div[@class="encounters-action tooltip-activator encounters-action--like"]', count=3)[0]
        swipe_right_btn.click()
        self.swipeRightCount += 1

    def flipThroughImages(self):
        for i in range(10):
            time.sleep(1.0)
            elements = self.driver.find_elements(By.XPATH, '//article[@class="encounters-album"]')
            elements.extend(self.driver.find_elements(By.XPATH, '//article[@class="encounters-album anim-enter-done"]'))
            yield elements
            self.actions.key_down(Keys.DOWN).perform()
            time.sleep(0.3)
            self.actions.key_up(Keys.DOWN).perform()

    def save_images(self, just_first_pic, directory):
        last_file_name='hi.png'
        for elements in self.flipThroughImages():
            for element in elements:
                filename = "data/" + directory + "/" + getRandomString() + ".png"
                element.screenshot(filename)
                time.sleep(1.0)
                if filecmp.cmp(last_file_name, filename):
                    return
                last_file_name = filename
            print('HERE')
            if just_first_pic:
                return

    def startSwiping(self):

        self.swipeRightCount = 0
        self.swipeLeftCount = 0

        while True:
            self.swipeAndSave()
            time.sleep(1)


    def swipeAndSave(self):
        totalYes = 0
        totalNo = 0
        yesConfident = 0
        noConfident = 0

        items = self.getElementXPath('//span[@class="encounters-story-profile__name"]', 10)

        is_abby = False
        for item in items:
            name = item.text
            print(name)
            print(name[:2].lower())
            if name[:2].lower() == 'ab':
                print("FOUND AN ABBY")
                is_abby = True

        if is_abby:
            print('WE FOUND AN ABBY')
            self.save_images(False, 'abby')
            self.swipeRight()
        else:
            self.save_images(True, 'notabby')
            self.swipeLeft()


    def __init__(self):

        self.last_names = []

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=selenium")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://bumble.com")

        self.actions = ActionChains(self.driver)

        self.swipeLeftCount = 0
        self.swipeRightCount = 0

        # with open('cookies.json') as json_file:
        #     data = json.load(json_file)
        #     for cookie in data:
        #         print(cookie)
        #         self.driver.add_cookie(cookie)

        # with open('localStorage.json') as json_file:
        #     data = json.load(json_file)
        #     for key, value in data.items():
        #         self.driver.execute_script("localStorage.setItem('" + key + "', '" + value + "')")

if __name__ == "__main__":
    print('Start')
    bot = BumbleBot()
    #time.sleep(10)
    #bot.startSwiping()


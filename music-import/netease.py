#%%
import os
import json
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


URL = "https://music.163.com"
CWD = os.getcwd()


def wait_element(element):
    while True:
        try:
            return driver.find_element(By.CSS_SELECTOR, element)
        except:
            pass


def wait_click(element):
    while True:
        try:
            element.click()
        except:
            pass


# Start Google Chrome.
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": CWD,
    "profile.default_content_setting_values.automatic_downloads": 1,
}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
# options.add_argument('--headless')  # Uncomment this line to hide the chrome GUI.
driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

# login
driver.get(URL)

with open("config.json", "r") as f:
    config = json.load(f)
wait_element('div[class="m-tophead f-pr j-tflag"]').click()
wait_element('a[class="u-btn2 other"]').click()
wait_element('input[type="checkbox"]').click()
wait_element('a[data-type="netease"]').click()
id_in = wait_element('input[class="js-input u-txt"]')
passwd_in = wait_element('input[type="password"]')
id_in.send_keys(config["ID"])
passwd_in.send_keys(config["PASSWD"])
passwd_in.send_keys(Keys.ENTER)

# Create a album
album_name = "import"
# wait_element('a[data-module="my"]').click()
# driver.switch_to.frame('contentFrame')
# wait_element('a[data-action="create-playlist"]').click()
# # input album name and create
# name_in = wait_element('input[class="u-txt j-flag"]')
# name_in.send_keys(album_name)
# name_in.send_keys(Keys.ENTER)

with open("songs.txt", "r") as f:
    songs_txt = f.readlines()
songs = []
for x in songs_txt:
    for song in x.split():
        songs.append(song)

#%%
n_all = len(songs)
n_not = 0
for song in songs:
    driver.switch_to.default_content()
    search = wait_element('input[type="text"]')
    search.clear()
    search.send_keys(song)
    search.send_keys(Keys.ENTER)

    driver.switch_to.frame("contentFrame")
    # Close popup window
    try:
        driver.find_element(
            By.CSS_SELECTOR, 'img[class="m-vipcashier-title-close"]'
        ).click()
        n_not += 1
    except:
        pass

    # Click the fav button
    tar = wait_element('span[class="icn icn-fav"]')
    ActionChains(driver).move_to_element(tar).click(tar).perform()
    # Found the album and add the song
    lis = driver.find_elements(By.CSS_SELECTOR, 'li[class="xtag "]')
    for li in lis:
        if li.text.split()[0] == album_name:
            wait_click(li)
            break

print("Process: %d/%d" % (n_all - n_not, n_all))
#%%
tar = wait_element('span[class="icn icn-fav"]')
ActionChains(driver).move_to_element(tar).click(tar).perform()

#%%
driver.find_element(By.CSS_SELECTOR, 'img[class="m-vipcashier-title-close"]').click()

import os
import datetime
import time
import json
import re
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


LOGIN_URL = "https://cas.sysu.edu.cn/cas/login?service=http%3A%2F%2Fgym.sysu.edu.cn%2Flogin%2Fpre.html"
URL = "https://gym.sysu.edu.cn/product/show.html?id=35"
CWD = os.path.dirname(os.path.abspath(__file__))
CAPTCHA = CWD + "/captcha.jpg"
TABLE = {
    9: "09:00-10:00",
    10: "10:01-11:00",
    11: "11:01-12:00",
    14: "14:00-15:00",
    15: "15:01-16:00",
    16: "16:01-17:00",
    17: "17:01-18:00",
    18: "18:00-19:00",
    19: "19:01-20:00",
    20: "20:01-21:00",
    21: "21:01-22:00",
}

def cal_interval():
    now_time = datetime.datetime.now()
    if now_time.hour <= 6:
        wtime_reserve = 0
    else:
        tomorrow = now_time + datetime.timedelta(days=+1)
        reserve_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        wtime_reserve = (reserve_time - now_time).seconds 

    wtime_login = 0
    return wtime_login, wtime_reserve

def wait_element(element):
    while True:
        try:
            return driver.find_element(By.CSS_SELECTOR, element)
        except:
            pass

def wait_weak_network(element):
    try:
        return driver.find_element(By.CSS_SELECTOR, element)
    except:
        return False


def dl_captcha():
    # Use javascript to download the captcha image.
    if os.path.exists(CAPTCHA):
        os.remove(CAPTCHA)

    script = """
    var a = document.createElement('a')
    a.download = 'captcha.jpg'
    a.href = 'https://cas.sysu.edu.cn/cas/captcha.jsp?time=0.0114514'   
    a.click()
    """
    driver.execute_script(script)


def get_captcha():
    # Use pytesseract to get string.
    while not os.path.exists(CAPTCHA):
        pass

    img = Image.open(CAPTCHA)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            data = img.getpixel((i, j))
            if data[0] <= 25 and data[1] <= 25 and data[2] <= 25:
                img.putpixel((i, j), (255, 255, 255, 255))

    # img.show()
    captcha = pytesseract.image_to_string(img)
    captcha = re.sub("[^\w]+", "", captcha)

    return captcha


def login(username, password):
    print("Ok, Let's go to log in...")
    driver.get(LOGIN_URL)
    wait_element('div[id="caslogin"]')

    while "cas.sysu.edu.cn" in driver.current_url:
        dl_captcha()

        wait_element('div[id="caslogin"]')
        username_in = driver.find_element(By.CSS_SELECTOR, 'input[id="username"]')
        password_in = driver.find_element(By.CSS_SELECTOR, 'input[id="password"]')
        captcha_in = driver.find_element(By.CSS_SELECTOR, 'input[id="captcha"]')

        username_in.send_keys(username)
        password_in.send_keys(password)
        captcha = get_captcha()
        print('Use captcha result "%s" to log in...' % captcha)
        captcha_in.send_keys(captcha)

        wait_element('input[class="btn btn-submit btn-block"]').click()
        time.sleep(1)

    driver.get(URL)


def reserve(book_date, book_times, switch_time, max_tab):
    print("Let's reserve the field which meet the `config.json` file...")
    driver.get(URL)
    flag = False
    index = 1
    stime = time.time()
    while True:
        if  time.time() - stime >= pow(5, index) and len(driver.window_handles) < max_tab:
            driver.execute_script('window.open("URL")')
            index += 1

        for handle in driver.window_handles:
            time.sleep(switch_time) # Comment this line to destroy CPU!
            driver.switch_to.window(handle)
            if not wait_weak_network('a[rel="shopping"]'):
                continue

            wait_element('a[rel="shopping"]').click()
            # Select date tab.
            driver.find_element(By.CSS_SELECTOR, 'li[data="%s"]' % book_date).click()

            for book_time in book_times:
                # Select all fields meet the time.
                fields = driver.find_elements(
                    By.CSS_SELECTOR, 'span[data-timer="%s"]' % book_time
                )

                print("There has %d field found between %s," % (len(fields), book_time))
                if len(fields) == 0:
                    print("so we don't expect it.")
                    continue

                # Select first empty filed meet the time.
                for i in range(len(fields)):
                    if fields[i].get_attribute("class") == "cell badminton easyui-tooltip":
                        fields[i].click()
                        driver.find_element(By.CSS_SELECTOR, 'button[id="reserve"]').click()
                        flag = True
                        break

                if flag:
                    # Reserve and confirm.
                    wait_element('button[id="reserve"]').click()
                    wait_element('button[class="confirm"]').click()
                    wait_element('button[class="button-large button-info paybutton"]').click()
                    print(', reserving success!')

                    return
                
                print('but no empty field found between %s.' % book_time)

            print('There is no suit field, Please check...')
            return


# Load configs.
with open(CWD + "/config.json", "r") as f:
    config = json.load(f)

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
if config['hide_chrome']:
    options.add_argument('--headless')  # Uncomment this line to hide the chrome GUI.
driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

# Calculate time
wtime_login, wtime_reserve = cal_interval()
# Begin login
time.sleep(wtime_login)
login(config["NetID"], config["Password"])
# Begin reserve
book_times = [TABLE.get(x) for x in config["book_time"]]
print('wait %d seconds to reserve...' % wtime_reserve)
time.sleep(wtime_reserve)
reserve(config["book_date"], book_times, config['switch_time'], config['max_tab'])

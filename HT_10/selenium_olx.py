from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


try:

    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://olx.ua')
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#headerSearch')))
    element.send_keys('Автомобиль')
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#submit-searchmain')))
    element.click()


    #сделаем скриншот не хедера, а самих объявлений
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#offers_table')))
    screen_elem = element.screenshot_as_png
    with open(os.path.join(os.path.dirname(__file__), 'scr.png'), 'wb') as f:
        f.write(screen_elem)


except Exception as error_exp:
    print(error_exp)
    
finally:
    browser.quit()
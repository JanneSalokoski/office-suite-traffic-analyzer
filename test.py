from selenium import webdriver

import time

driver = webdriver.Chrome()
driver.get("https://www.google.com")

while True:
    inp = input()
    if inp == "q":
        break

    time.sleep(1)

driver.quit()

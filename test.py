from selenium import webdriver

import time
import random

from selenium.webdriver.common.by import By
import typer


def main(url: str, file: str):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
    except Exception as e:
        print(f"Could not load '{url}'")
        print(e)
        driver.quit()

    webdriver.ActionChains(driver).key_down(webdriver.Keys.CONTROL).send_keys(
        "a"
    ).key_up(webdriver.Keys.CONTROL).send_keys(webdriver.Keys.BACKSPACE).perform()

    target_wpm = 80
    natural_delay = 0.125  # Delay caused by the loop
    base_delay = (60.0 / (target_wpm * 5)) - natural_delay
    jitter = 0.1

    extra_space_pause = (0.05, 0.15)
    extra_par_pause = (0.5, 1.0)

    print(base_delay)

    with open(file, "r") as f:
        text = f.read()

        words = len(text.split(" "))
        print(f"Should take {(words / target_wpm) * 60} seconds")

        start = time.perf_counter()

        for char in text:
            webdriver.ActionChains(driver).send_keys(char).perform()
            pause = random.gauss(base_delay, jitter)

            if char == " ":
                pause += random.uniform(*extra_space_pause)
            if char in ("\n", "\r"):
                pause += random.uniform(*extra_par_pause)

            time.sleep(max(0, pause))

        end = time.perf_counter()
        print(f"Took: {end - start} seconds")
        print(f"wpm: {(words / (end - start)) * 60}")

    driver.quit()


if __name__ == "__main__":
    typer.run(main)

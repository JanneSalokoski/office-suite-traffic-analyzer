from enum import Enum
from typing import Annotated, Literal, Optional, override
from selenium import webdriver

import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import typer


def read_file(file: str):
    with open(file, "r") as f:
        return f.read()


class TestRunner:
    def __init__(self):
        self.driver: WebDriver = webdriver.Chrome()

    def open(self, url: str):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Could not load url '{url}'")
            print(e)
            self.driver.quit()

    def wait_until_ready(self):
        pass

    def write_to_file(self, text: str, target_wpm: int = 80):
        webdriver.ActionChains(self.driver).key_down(webdriver.Keys.CONTROL).send_keys(
            "a"
        ).key_up(webdriver.Keys.CONTROL).send_keys(webdriver.Keys.BACKSPACE).perform()

        natural_delay = 0.125  # Delay caused by the loop
        base_delay = (60.0 / (target_wpm * 5)) - natural_delay
        jitter = 0.1

        extra_space_pause = (0.05, 0.15)
        extra_par_pause = (0.5, 1.0)

        words = len(text.split(" "))
        print(f"Should take {(words / target_wpm) * 60} seconds")

        start = time.perf_counter()

        for char in text:
            webdriver.ActionChains(self.driver).send_keys(char).perform()
            pause = random.gauss(base_delay, jitter)

            if char == " ":
                pause += random.uniform(*extra_space_pause)
            if char in ("\n", "\r"):
                pause += random.uniform(*extra_par_pause)

            time.sleep(max(0, pause))

        end = time.perf_counter()
        print(f"Took: {end - start} seconds")
        print(f"wpm: {(words / (end - start)) * 60}")

    def run(self, url: str, text: str):
        self.open(url)
        self.wait_until_ready()
        self.write_to_file(text)
        self.driver.close()


class WordTestRunner(TestRunner):
    @override
    def wait_until_ready(self):
        iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
        )

        self.driver.switch_to.frame(iframe)

        _ = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Page"))
        )


class ChromeTestRunner(TestRunner):
    pass


class Mode(str, Enum):
    docs = "docs"
    word = "word"


def main(
    url: str,
    file: str,
    mode: Annotated[
        Mode,
        typer.Option("--mode", "-m", help="Choose docs or word", show_choices=True),
    ] = Mode.docs,
):
    text = read_file(file)

    if mode == Mode.word:
        runner = WordTestRunner()
    else:
        runner = ChromeTestRunner()

    runner.run(url, text)


if __name__ == "__main__":
    typer.run(main)

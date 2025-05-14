from selenium import webdriver

import time

import typer


def main(url: str):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
    except Exception as e:
        print(f"Could not load '{url}'")
        print(e)
        driver.quit()

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    typer.run(main)

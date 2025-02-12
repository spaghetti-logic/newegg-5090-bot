# Bot to watch specific products on newegg and add them to the cart and buy if they become available
import os

from seleniumbase import Driver
import time
from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

items = []

# load items
for i in range(100):
    url = os.getenv("ITEM_{}".format(i))

    if url is None:
        break
    else:
        items.append(url)


def wait_and_fill(element_id: str, text: str, driver: Driver):
    driver.wait_for_element(element_id, timeout=10)

    # Type the email address into the input field
    driver.type(element_id, text)


def do_login_screen(driver: Driver):
    wait_and_fill("#labeled-input-signEmail", USER_EMAIL, driver)
    time.sleep(1)
    driver.click("#signInSubmit")
    wait_and_fill("#labeled-input-password", USER_PASSWORD, driver)
    time.sleep(1)
    driver.click("#signInSubmit")


def main():
    driver = Driver(
        browser="chrome",
        uc=True,
        headless2=False,
        incognito=False,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        do_not_track=False,
        undetectable=True,
    )

    driver.get('https://www.newegg.com')
    time.sleep(4)
    driver.click("div.header2021-account a")

    do_login_screen(driver)

    # run through our list of interest URLs
    for item in items:
        driver.get(item)

        buttons = driver.find_elements("xpath", "//button[contains(@class, 'btn-wide') and contains(., 'Add to cart')]")
        if buttons:
            print("Item is in stock! Adding to cart!")
            buttons[0].click()

            while True:
                buttons = driver.find_elements("xpath",
                                               "//button[contains(@class, 'btn-primary') and contains(., 'Proceed to checkout')]")
                if buttons:
                    break
                else:
                    time.sleep(1)

            buttons[0].click()
            input("Press Enter to close the browser...")
            driver.quit()
            exit(0)
        else:
            time.sleep(2)


if __name__ == "__main__":
    main()
    input("Press Enter to close the browser...")
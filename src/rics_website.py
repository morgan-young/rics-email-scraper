"""
This file contains all the functions relating to
the rics website.

"""

import io
import os
import shutil
import tempfile
import time

import requests
from csv_processing import convert_list_to_csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")


def load_website(chrome):
    """
    This functions loads the rics
    website on the residential surveyor search
    page, so we can grab the details.

    :param chrome: the already instantiated chromedriver

    """

    chrome.get(
        "https://www.ricsfirms.com/residential/?search=true&location=United%20Kingdom&firmname=&service=3"
    )
    WebDriverWait(chrome, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='surveyor-search-results']/div/div[1]/span")
        )
    )

    print("loaded website")


def store_surveyor_profile_urls(chrome) -> list:
    """
    This function loops through all pages of the surveyors
    and stores the url of their rics profile in a list.

    This is so we can go to those URL's and grab the emails.

    :param chrome: the already instantiated chromedriver
    :rytpe: list
    :returns: the list of profile url's

    """
    # 78 pages
    profile_urls = []
    try:
        # replace the second number with however many pages you want to scrape
        for i in range(1, 78):
            # detect the presence of profiles on the page
            WebDriverWait(chrome, 15).until(
                EC.presence_of_element_located((By.ID, "more"))
            )
            all_profiles = chrome.find_elements(By.ID, "more")
            # for all profiles on the page, get the url and save it so we can use it to get the email later
            for profile in all_profiles:
                url = profile.get_attribute("href")
                print(url)
                profile_urls.append(url)
            # find and click the next button
            WebDriverWait(chrome, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//*[@id='surveyor-search-results']/div/div[1]/nav/ul/li[.]/a[.='{i+1}']",
                    )
                )
            )
            try:
                chrome.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div/div/div[2]/div/div/button[2]",
                ).click()
            except:
                print("no popup")
            chrome.find_element(
                By.XPATH,
                f"//*[@id='surveyor-search-results']/div/div[1]/nav/ul/li[.]/a[.='{i+1}']",
            ).click()
        return profile_urls
    except Exception as e:
        print(e)
        convert_list_to_csv(profile_urls, "surveyor_urls")


def store_surveyor_email_address(chrome, profile_url) -> str:
    """
    This function takes a profile url of a surveyor
    on the RICS website and returns their email address.

    :param str chrome: the already instantiated chromedriver
    :param str profile_url:
    :rtype: str
    :returns: the email address on that profile url

    """
    chrome.get(profile_url)
    time.sleep(3)
    WebDriverWait(chrome, 15).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#office-contact > a.office-details__item.office-details__email.brand--hover > span.office-details__content.brand--color",
            )
        )
    )

    # they have put in some clever formatting to avoid the email being scraped. We get around this by manipulating the innerHTML.
    listed_email = chrome.find_element(
        By.XPATH, "//*[@id='office-contact']/a[2]/span[1]"
    )
    split_email = listed_email.get_attribute("innerHTML")
    email_name = split_email.split("<")[0]
    email_domain = split_email.split(">")[4]
    email_address = f"{email_name}@{email_domain}"
    return email_address

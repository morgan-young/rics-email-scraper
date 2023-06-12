import io
import os
import tempfile
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from csv_processing import convert_list_to_csv
from rics_website import (load_website, store_surveyor_email_address,
                          store_surveyor_profile_urls)

options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")

chrome = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def run_scraper(chrome):
    """
    This function runs the whole scraper.

    """

    load_website(chrome)
    url_list = store_surveyor_profile_urls(chrome)
    surveyor_email_list = []
    for url in url_list:
        email = store_surveyor_email_address(chrome, url)
        print(email)
        surveyor_email_list.append(email)
    print(surveyor_email_list)

    convert_list_to_csv(surveyor_email_list, "surveyor_emails_pg1_pg10")


if __name__ == "__main__":
    run_scraper(chrome)

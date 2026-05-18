import os
import shutil
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def base_url():
    handler = partial(SimpleHTTPRequestHandler, directory=str(PROJECT_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    host, port = server.server_address
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{host}:{port}/index.html"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=1)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_path = (
        os.getenv("CHROME_PATH")
        or shutil.which("chrome")
        or shutil.which("google-chrome")
        or shutil.which("chrome.exe")
    )
    if chrome_path:
        options.binary_location = chrome_path

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
    in_ci = os.getenv("GITHUB_ACTIONS") == "true"
    try:
        if chromedriver_path:
            instance = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        else:
            instance = webdriver.Chrome(options=options)
    except NoSuchDriverException as exc:
        if in_ci:
            raise
        pytest.skip(f"Chrome/ChromeDriver not found in local environment: {exc}")

    try:
        yield instance
    finally:
        instance.quit()


def open_form(driver, base_url):
    driver.get(base_url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "feedback-form"))
    )


def test_heading_is_displayed(driver, base_url):
    open_form(driver, base_url)
    title = driver.find_element(By.ID, "form-title")
    assert title.text == "Feedback Form"


def test_submit_is_disabled_on_empty_form(driver, base_url):
    open_form(driver, base_url)
    submit_button = driver.find_element(By.ID, "submit-btn")
    assert not submit_button.is_enabled()


def test_submit_enabled_for_valid_data(driver, base_url):
    open_form(driver, base_url)

    driver.find_element(By.ID, "name").send_keys("Ivan")
    driver.find_element(By.ID, "email").send_keys("ivan@example.com")
    driver.find_element(By.ID, "message").send_keys("Test message")

    submit_button = driver.find_element(By.ID, "submit-btn")
    WebDriverWait(driver, 5).until(lambda d: submit_button.is_enabled())
    assert submit_button.is_enabled()


def test_success_message_after_submit(driver, base_url):
    open_form(driver, base_url)

    driver.find_element(By.ID, "name").send_keys("Maria")
    driver.find_element(By.ID, "email").send_keys("maria@example.com")
    driver.find_element(By.ID, "message").send_keys("Ready to submit")
    driver.find_element(By.ID, "submit-btn").click()

    status = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "status-message"))
    )
    assert status.text == "Thanks, Maria! Form submitted."

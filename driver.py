"""Chrome session for Workday. Prefers the installed browser over Chrome-for-Testing."""

from __future__ import annotations

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import HEADLESS, MAINTENANCE_HINTS


def want_headless(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return explicit
    env = os.environ.get("WORKDAY_HEADLESS")
    if env is not None and str(env).strip() != "":
        return str(env).strip().lower() in {"1", "true", "yes"}
    return HEADLESS


def find_chrome() -> str:
    candidates = [
        os.environ.get("CHROME_BIN", ""),
        r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\Application\\chrome.exe"),
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    return ""


def looks_like_maintenance(driver: Chrome) -> bool:
    href = (driver.current_url or "").lower()
    body = ""
    try:
        body = driver.find_element(By.TAG_NAME, "body").text.lower()
    except Exception:
        pass
    blob = f"{href}\n{body[:4000]}"
    return any(hint in blob for hint in MAINTENANCE_HINTS)


def build_chrome(headless: bool | None = None) -> Chrome:
    options = Options()
    if want_headless(headless):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1100")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.page_load_strategy = "eager"
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
        },
    )
    chrome_bin = find_chrome()
    if chrome_bin:
        options.binary_location = chrome_bin
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
        )
    except Exception:
        pass
    return driver

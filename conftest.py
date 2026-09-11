"""Fixtures, failure screenshots, and pytest-html report wiring."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from selenium.webdriver import Chrome

from driver import build_chrome
from pages import Workday

REPORT_DIR = Path("reports")
SCREEN_DIR = Path("screenshots")
REPORT_DIR.mkdir(parents=True, exist_ok=True)
SCREEN_DIR.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Show the Chrome window (overrides WORKDAY_HEADLESS).",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Force headless Chrome.",
    )


def pytest_configure(config: pytest.Config) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    if config.getoption("--headed"):
        os.environ["WORKDAY_HEADLESS"] = "false"
    elif config.getoption("--headless"):
        os.environ["WORKDAY_HEADLESS"] = "true"
    htmlpath = getattr(config.option, "htmlpath", None)
    if not htmlpath:
        config.option.htmlpath = str(REPORT_DIR / "report.html")
        config.option.self_contained_html = True


def pytest_html_report_title(report) -> None:
    report.title = "ForgeDay — Workday apply report"


@pytest.fixture(scope="session")
def browser() -> Iterator[Chrome]:
    driver = build_chrome()
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def wd(browser: Chrome) -> Workday:
    return Workday(browser)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Iterator[None]:
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when != "call":
        report.extras = extras
        return
    driver = item.funcargs.get("browser")
    if not isinstance(driver, Chrome):
        report.extras = extras
        return
    png = SCREEN_DIR / f"{item.name}-{report.outcome}.png"
    try:
        driver.save_screenshot(str(png))
        extras.append(_html_image(png))
        extras.append(_html_url(driver.current_url))
    except Exception:
        pass
    report.extras = [item for item in extras if item is not None]


def _html_image(path: Path):
    try:
        from pytest_html import extras
        return extras.image(str(path))
    except Exception:
        return None


def _html_url(url: str):
    try:
        from pytest_html import extras
        return extras.url(url)
    except Exception:
        return None

"""Career-site search tests."""

import pytest

from config import CAREER_SITE_URL, JOB_POSTING_URL, SEARCH_KEYWORD
from locators import Locators
from pages import Workday

needs_tenant = pytest.mark.skipif(
    "your-tenant" in CAREER_SITE_URL and not JOB_POSTING_URL,
    reason="Set WORKDAY_URL or WORKDAY_JOB_URL to a real tenant before running live tests.",
)


@needs_tenant
class TestCareerSearch:
    def test_keyword_search_returns_job_cards(self, wd: Workday) -> None:
        wd.open(CAREER_SITE_URL)
        cards = wd.search_jobs(SEARCH_KEYWORD)
        assert len(cards) >= 1

    def test_job_card_has_a_title(self, wd: Workday) -> None:
        titles = wd.css_all(Locators.JOB_TITLE)
        if not titles:
            wd.open(CAREER_SITE_URL)
            wd.search_jobs(SEARCH_KEYWORD)
            titles = wd.css_all(Locators.JOB_TITLE)
        assert titles[0].text.strip()

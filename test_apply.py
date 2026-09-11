"""Apply-flow tests."""

import pytest

from config import (
    ALLOW_SUBMIT,
    CAREER_SITE_URL,
    DRY_RUN,
    JOB_POSTING_URL,
    SEARCH_KEYWORD,
    wants_submit,
)
from locators import Locators
from pages import Workday

needs_tenant = pytest.mark.skipif(
    "your-tenant" in CAREER_SITE_URL and not JOB_POSTING_URL,
    reason="Set WORKDAY_URL or WORKDAY_JOB_URL to a real tenant before running live tests.",
)


@needs_tenant
class TestApplyJourney:
    def test_posting_exposes_apply(self, wd: Workday) -> None:
        if JOB_POSTING_URL.strip():
            wd.open(JOB_POSTING_URL.strip())
        else:
            wd.open(CAREER_SITE_URL)
            wd.search_jobs(SEARCH_KEYWORD)
            wd.open_first_job()
        apply = wd.resolve(Locators.APPLY, *Locators.APPLY_VARIANTS)
        assert apply.is_displayed()

    def test_full_application_flow(self, wd: Workday) -> None:
        """Sign in with email, fill every page, submit unless dry-run is on."""
        result = wd.apply_journey(submit=wants_submit())
        wd.screenshot("flow-result")
        assert result in {"submitted", "dry-run-stopped-on-review", "ended"}
        if wants_submit():
            assert result == "submitted", result
        else:
            assert result != "submitted"


def test_dry_run_flag_is_consistent() -> None:
    if DRY_RUN and not ALLOW_SUBMIT:
        assert wants_submit() is False

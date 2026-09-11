"""Runtime config. Env vars win, then values baked by ForgeDay, then profile.json."""

from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent

CAREER_SITE_URL = os.environ.get("WORKDAY_URL", "https://workday.wd5.myworkdayjobs.com/Workday")
JOB_POSTING_URL = os.environ.get("WORKDAY_JOB_URL", "")
SEARCH_KEYWORD = os.environ.get("WORKDAY_KEYWORD", "Software Engineer")
HEADLESS = os.environ.get("WORKDAY_HEADLESS", "false").lower() in {"1", "true", "yes"}
DRY_RUN = os.environ.get("WORKDAY_DRY_RUN", "true").lower() in {"1", "true", "yes"}
ALLOW_SUBMIT = os.environ.get("WORKDAY_SUBMIT", "false").lower() in {"1", "true", "yes"}
TIMEOUT = int(os.environ.get("WORKDAY_TIMEOUT", "25"))
RESUME_PATH = os.environ.get("WORKDAY_RESUME", "./fixtures/resume.pdf")
SCREENSHOT_DIR = Path(os.environ.get("WORKDAY_SCREENSHOTS", "./screenshots"))
PROFILE_PATH = HERE / "profile.json"

MAINTENANCE_HINTS = (
    "/wday/drs/outage",
    "community.workday.com/maintenance",
    "maintenance-page",
    "under maintenance",
    "workday public cloud maintenance",
    "workday has moved to a new address",
    "this site is currently unavailable",
)


def _load_profile() -> dict:
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return json.loads(r"""{
  \"email\": \"qa.applicant@example.com\",
  \"password\": \"ChangeMe_Workday1!\",
  \"firstName\": \"Alex\",
  \"lastName\": \"Rivera\",
  \"country\": \"United States of America\",
  \"address1\": \"100 Market Street\",
  \"city\": \"San Francisco\",
  \"region\": \"California\",
  \"postalCode\": \"94105\",
  \"phoneType\": \"Mobile\",
  \"phone\": \"4155550199\",
  \"linkedin\": \"https://www.linkedin.com/in/example\",
  \"source\": \"LinkedIn\",
  \"legallyAuthorized\": \"Yes\",
  \"needsSponsorship\": \"No\",
  \"gender\": \"I do not want to answer\",
  \"veteranStatus\": \"I do not want to answer\",
  \"skills\": [\"Python\", \"Selenium\", \"Quality Assurance\"],
  \"work\": [{\"jobTitle\": \"QA Engineer\", \"company\": \"Northline Labs\", \"location\": \"San Francisco, CA\", \"startMonth\": \"03\", \"startYear\": \"2021\", \"endMonth\": \"\", \"endYear\": \"\", \"currentlyWorkHere\": true, \"description\": \"Own end-to-end Selenium coverage for career-site apply flows, including Workday tenants.\"}],
  \"education\": [{\"school\": \"State University\", \"degree\": \"Bachelor of Science\", \"fieldOfStudy\": \"Computer Science\", \"gpa\": \"3.7\", \"firstYearAttended\": \"2016\", \"lastYearAttended\": \"2020\"}],
  \"questions\": [{\"question\": \"Are you legally authorized to work\", \"answer\": \"Yes\"}, {\"question\": \"Will you require sponsorship\", \"answer\": \"No\"}]
}""")


PROFILE = _load_profile()


def wants_submit() -> bool:
    if os.environ.get("WORKDAY_SUBMIT", "").lower() in {"1", "true", "yes"}:
        return True
    if os.environ.get("WORKDAY_DRY_RUN", "").lower() in {"1", "true", "yes"}:
        return False
    if ALLOW_SUBMIT:
        return True
    return not DRY_RUN

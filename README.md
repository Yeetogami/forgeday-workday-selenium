# Workday job-application tests (Selenium + pytest)

End-to-end pytest suite for a Workday career site: search jobs, open a posting, apply manually, **Sign in with email**, fill the application, and stop on Review unless submit is enabled.

Default target: [Workday careers](https://workday.wd5.myworkdayjobs.com/Workday).

## Latest run

pytest-html report from **11 Sep 2026, 16:10 IST** on Windows / Python 3.12 — **7 passed, 1 failed**, 8 tests in 1m 51s.

<img alt="pytest-html report: 7 passed, 1 failed" src="https://cdn.jsdelivr.net/gh/Yeetogami/forgeday-workday-selenium@b45b7297a0378aed263209ad14f7689d8610b3a6/docs/pytest-report.svg" width="900" />

| Result | Test | Notes |
| --- | --- | --- |
| Passed | `test_posting_exposes_apply` | Live career site: search + Apply button |
| Passed | Locator contract (3) | `data-automation-id` selectors |
| Passed | Search tests (2) | Keyword search returns job cards |
| Passed | Dry-run flag | Submit stays off unless forced |
| Failed | `test_full_application_flow` | Reaches Sign In; Workday's React Sign In button still does not complete login |

The HTML report is written to `reports/report.html` on every run (`pytest-html`).

## Layout

```
config.py          # WORKDAY_URL, dry-run, timeouts
driver.py          # Chrome session (headed by default)
locators.py        # data-automation-id CSS
pages.py           # Page object: search → apply → sign in → fill → submit
conftest.py        # --headed / --headless, HTML report, failure screenshots
test_apply.py      # Apply journey
test_search.py     # Career-site search
test_locators.py   # Selector contract (no browser)
profile.json       # Candidate data (use a dummy password in git)
docs/              # README images
```

## Install

Python 3.12+, Google Chrome.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

ChromeDriver is resolved by Selenium 4 Manager. You do not download it by hand.

## Configure

1. Edit `profile.json` — **Sign in with email** uses `email` and `password`.
2. Optional env (see `.env.example`):

| Variable | Default | Meaning |
| --- | --- | --- |
| `WORKDAY_URL` | Workday careers | Tenant career site |
| `WORKDAY_JOB_URL` | empty | Skip search; open this posting |
| `WORKDAY_KEYWORD` | `Software Engineer` | Search term |
| `WORKDAY_HEADLESS` | `false` | Show Chrome |
| `WORKDAY_DRY_RUN` | `true` | Stop on Review, do not submit |
| `WORKDAY_SUBMIT` | `false` | Set `true` to click Submit |
| `WORKDAY_RESUME` | `./fixtures/resume.pdf` | Optional résumé upload |

Do not commit a real password. Keep secrets in `profile.local.json` or env on your machine.

## Run

Headed (Chrome window visible):

```powershell
pytest --headed
start reports\report.html
```

Or `.\run.ps1`.

Only the live apply journey:

```powershell
pytest --headed test_apply.py::TestApplyJourney::test_full_application_flow
```

Actually submit (off by default):

```powershell
$env:WORKDAY_HEADLESS="false"
$env:WORKDAY_DRY_RUN="false"
$env:WORKDAY_SUBMIT="true"
pytest test_apply.py -v
```

## Auth behaviour

- Clicks **Sign in with email**, not Apple/Google.
- Types email and password with real keystrokes (JS `.value` leaves React empty, so Sign In only flashes).
- Submits with **Enter**, then the blue Sign In button.
- Does **not** auto-create an account if the email already exists.

## License

Use and modify as you like for personal QA. You are responsible for any applications submitted against a live tenant.

# API Automation Framework (Playwright + Requests + pytest)

Postman replacement: code-based, version-controlled API tests with two interchangeable HTTP backends:
[Playwright for Python](https://playwright.dev/python/docs/api-testing) (`APIRequestContext`) and
[Python Requests](https://requests.readthedocs.io/). Tests are written once and run against either or both.

## Features
- **Two backends, one API**: `PlaywrightClient` and `RequestsClient` share `ApiClient` (`framework/clients/`),
  returning the same `Result` (`status`, `json()`, `text`, `headers`, `elapsed_ms`), with logging, timing and Allure attachments
- **Requests extras**: pooled `Session`, automatic retries on 502/503/504
- **Data-driven testing** from JSON and CSV (`test-data/`) via `pytest.mark.parametrize`
- **JSON schema validation** (`jsonschema`)
- **Reporting**: self-contained HTML (`reports/report.html`) and Allure (`allure-results/`)
- **CI/CD**: GitHub Actions matrix (one job per backend), parallel tests, JUnit check summary on PRs,
  HTML report artifacts, merged Allure report published to GitHub Pages
- **Config via env vars**: `BASE_URL`, `API_TOKEN`, `API_TIMEOUT_MS`, `API_CLIENT` (or a `.env` file)

## Structure
```
conftest.py            # session-scoped Playwright request context + `api` fixture
framework/clients/     # base ApiClient + Result, Playwright and Requests backends
framework/             # config, data loader
tests/                 # test_posts.py, test_users.py
test-data/             # posts.json, users.json, new_posts.csv
.github/workflows/     # CI pipeline
```

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                    # everything
pytest -m smoke           # smoke only
pytest -n auto            # parallel
pytest --client requests # one backend only (or API_CLIENT=playwright|requests|both)
```
Each test is reported once per backend, e.g. `test_list_posts[playwright]` and `test_list_posts[requests]`.
Open `reports/report.html`. For Allure: `allure serve allure-results` (needs the Allure CLI).

## Point at your own API
```bash
BASE_URL=https://api.yourcompany.com API_TOKEN=xxxx pytest
```
The sample suite targets the public JSONPlaceholder API. Replace the tests and the files in `test-data/`
with your own endpoints and cases.

## Add a data-driven test
1. Add rows to a file in `test-data/`.
2. Parametrize with `load_json("file.json")` or `load_csv("file.csv")` (see `tests/test_posts.py`).

## Write a test
Use the `api` fixture and pass `params=` / `json=` / `headers=`; the same call works on both backends:
```python
def test_create(api):
    r = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
    assert r.status == 201
```

## CI setup
- Optional repo variable `BASE_URL`, optional secret `API_TOKEN`.
- Manual runs (`workflow_dispatch`) let you pick a marker and a backend.
- For the Allure report: enable GitHub Pages from the `gh-pages` branch.

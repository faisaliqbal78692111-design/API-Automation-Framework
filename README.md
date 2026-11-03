# API Automation Framework (Playwright + Requests + pytest)

Postman replacement: code-based, version-controlled API tests with two interchangeable HTTP backends:
[Playwright for Python](https://playwright.dev/python/docs/api-testing) (`APIRequestContext`) and
[Python Requests](https://requests.readthedocs.io/). Tests are written once and run against either or both.
The suite targets the [ReqRes](https://reqres.in/) demo API.

## Features
- **Two backends, one API**: `PlaywrightClient` and `RequestsClient` share `ApiClient` (`framework/clients/`),
  returning the same `Result` (`status`, `json()`, `text`, `headers`, `elapsed_ms`), with logging, timing and Allure attachments
- **Rate-limit aware**: on HTTP 429 the client waits for the server's reset time and retries;
  daily-quota 429s fail fast with the server's message
- **Requests extras**: pooled `Session`, automatic retries on 502/503/504
- **Data-driven testing** from JSON and CSV (`test-data/`) via `pytest.mark.parametrize`
- **JSON schema validation** (`framework/schemas.py`, `jsonschema`)
- **Reporting**: self-contained HTML (`reports/report.html`) and Allure (`allure-results/`)
- **CI/CD**: GitHub Actions matrix (one job per backend), JUnit check summary on PRs,
  HTML report artifacts, merged Allure report published to GitHub Pages
- **Config via env vars** (or a `.env` file): `BASE_URL`, `API_KEY`, `API_KEY_HEADER`, `API_TOKEN`,
  `API_TIMEOUT_MS`, `API_CLIENT`, `RATE_LIMIT_RETRIES`, `RATE_LIMIT_MAX_WAIT_S`

## Structure
```
conftest.py            # `api` fixture, parametrized per backend
framework/clients/     # base ApiClient + Result, Playwright and Requests backends
framework/             # config, data loader, JSON schemas
tests/                 # test_users.py, test_resources.py, test_auth.py
test-data/             # users.json, user_pages.json, resources.json, auth_cases.json, new_users.csv
.github/workflows/     # CI pipeline
```

## Test coverage (ReqRes)
| Area | Endpoints | Cases |
|---|---|---|
| Users | `GET /users`, `GET /users/{id}`, `POST`, `PUT`, `PATCH`, `DELETE /users/{id}` | list + schema, pagination, single user, 404, create (CSV), update, delete, delayed response |
| Resources | `GET /unknown`, `GET /unknown/{id}` | list + schema, single resource, 404 |
| Auth | `POST /login`, `POST /register` | valid login/register, missing email/password, unknown user |

## ReqRes API key (required for automated runs)
ReqRes allows only **40 requests/day per IP** from scripts without a key; one full run sends ~62.
1. Create a free account at https://app.reqres.in/sign-up and copy your API key.
2. Locally, create `.env` in the project root (it is git-ignored):
   ```
   API_KEY=your-reqres-key
   ```
3. In GitHub: **Settings → Secrets and variables → Actions → New repository secret**, name `API_KEY`.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                    # everything, both backends
pytest -m smoke           # smoke only
pytest --client requests  # one backend only (or API_CLIENT=playwright|requests|both)
```
Each test is reported once per backend, e.g. `test_list_users[playwright]` and `test_list_users[requests]`.
Open `reports/report.html`. For Allure: `allure serve allure-results` (needs the Allure CLI).
Avoid `-n auto` against ReqRes: the per-minute limit makes parallel workers wait on 429s.

## Point at another API
```bash
BASE_URL=https://api.yourcompany.com API_TOKEN=xxxx pytest
```
Replace the tests, `framework/schemas.py` and the files in `test-data/` with your own endpoints and cases.

## Add a data-driven test
1. Add rows to a file in `test-data/`.
2. Parametrize with `load_json("file.json")` or `load_csv("file.csv")` (see `tests/test_auth.py`).

## Write a test
Use the `api` fixture and pass `params=` / `json=` / `headers=`; the same call works on both backends:
```python
def test_create(api):
    r = api.post("/users", json={"name": "morpheus", "job": "leader"})
    assert r.status == 201
```

## CI setup
- Secret `API_KEY` (ReqRes key). Optional repo variable `BASE_URL`, optional secret `API_TOKEN`.
- Manual runs (`workflow_dispatch`) let you pick a marker and a backend.
- For the Allure report: enable GitHub Pages from the `gh-pages` branch.

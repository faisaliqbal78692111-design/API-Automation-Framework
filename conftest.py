import pytest

from framework import config
from framework.clients import PlaywrightClient, RequestsClient


def pytest_addoption(parser):
    parser.addoption(
        "--client",
        choices=["playwright", "requests", "both"],
        help="HTTP backend to run tests with (overrides API_CLIENT env var)",
    )


def pytest_generate_tests(metafunc):
    # Every test using the `api` fixture runs once per selected backend.
    if "api" in metafunc.fixturenames:
        opt = metafunc.config.getoption("--client")
        clients = config.CLIENTS if not opt else (["playwright", "requests"] if opt == "both" else [opt])
        metafunc.parametrize("api", clients, indirect=True, scope="session")


@pytest.fixture(scope="session")
def playwright_client(playwright):
    ctx = playwright.request.new_context(
        extra_http_headers=config.default_headers(),
        timeout=config.TIMEOUT_MS,
    )
    yield PlaywrightClient(ctx, config.BASE_URL)
    ctx.dispose()


@pytest.fixture(scope="session")
def requests_client():
    client = RequestsClient(config.BASE_URL, config.default_headers(), config.TIMEOUT_MS)
    yield client
    client.close()


@pytest.fixture(scope="session")
def api(request):
    # Resolve lazily so a requests-only run never starts Playwright.
    return request.getfixturevalue(f"{request.param}_client")

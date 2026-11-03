from playwright.sync_api import APIRequestContext

from framework.clients.base import ApiClient, Result


class PlaywrightClient(ApiClient):
    """Backend using Playwright's APIRequestContext."""

    name = "playwright"

    def __init__(self, context: APIRequestContext):
        self.context = context

    def _request(self, method, path, *, params=None, json=None, headers=None) -> Result:
        resp = self.context.fetch(path, method=method, params=params, data=json, headers=headers)
        return Result(status=resp.status, url=resp.url, text=resp.text(), headers=resp.headers)

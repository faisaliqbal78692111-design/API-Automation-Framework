import allure
import pytest

from framework.data_loader import load_json


@allure.feature("Authentication")
class TestAuth:
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", load_json("auth_cases.json"), ids=lambda c: c["name"])
    def test_auth_data_driven(self, api, case):
        r = api.post(case["endpoint"], json=case["payload"])
        assert r.status == case["expectedStatus"]
        body = r.json()
        if case["expectedError"]:
            assert body["error"] == case["expectedError"]
            assert "token" not in body
        else:
            assert body["token"]

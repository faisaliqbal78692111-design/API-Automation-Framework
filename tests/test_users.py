import allure
import pytest

from framework.data_loader import load_json


@allure.feature("Users")
class TestUsers:
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", load_json("users.json"), ids=lambda c: f"user-{c['id']}")
    def test_get_user_data_driven(self, api, case):
        r = api.get(f"/users/{case['id']}")
        assert r.status == 200
        body = r.json()
        assert body["name"] == case["expectedName"]
        assert body["email"] == case["expectedEmail"]

    @pytest.mark.regression
    def test_user_not_found(self, api):
        assert api.get("/users/9999").status == 404

    @pytest.mark.regression
    def test_user_posts_nested(self, api):
        r = api.get("/users/1/posts")
        assert r.status == 200
        assert len(r.json()) > 0

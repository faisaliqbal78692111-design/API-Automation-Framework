import allure
import pytest
from jsonschema import validate

from framework import schemas
from framework.data_loader import load_csv, load_json


@allure.feature("Users")
class TestUsers:
    @pytest.mark.smoke
    def test_list_users(self, api):
        r = api.get("/users", params={"page": 2})
        assert r.status == 200
        body = r.json()
        validate(body, schemas.page_of(schemas.USER))
        assert body["page"] == 2
        assert len(body["data"]) == body["per_page"]

    @pytest.mark.regression
    @pytest.mark.parametrize("case", load_json("user_pages.json"), ids=lambda c: f"page-{c['page']}")
    def test_pagination_data_driven(self, api, case):
        r = api.get("/users", params={"page": case["page"]})
        assert r.status == 200
        assert [u["id"] for u in r.json()["data"]] == case["expectedIds"]

    @pytest.mark.smoke
    @pytest.mark.parametrize("case", load_json("users.json"), ids=lambda c: f"user-{c['id']}")
    def test_get_user_data_driven(self, api, case):
        r = api.get(f"/users/{case['id']}")
        assert r.status == 200
        user = r.json()["data"]
        validate(user, schemas.USER)
        for field in ("email", "first_name", "last_name"):
            assert user[field] == case[field]

    @pytest.mark.regression
    @pytest.mark.parametrize("user_id", [23, 999])
    def test_user_not_found(self, api, user_id):
        r = api.get(f"/users/{user_id}")
        assert r.status == 404
        assert r.json() == {}

    @pytest.mark.regression
    @pytest.mark.parametrize("row", load_csv("new_users.csv"), ids=lambda r: r["name"])
    def test_create_user_data_driven(self, api, row):
        r = api.post("/users", json=row)
        assert r.status == 201
        body = r.json()
        assert body["name"] == row["name"]
        assert body["job"] == row["job"]
        assert body["id"]
        assert body["createdAt"]

    @pytest.mark.regression
    def test_update_user_put(self, api):
        r = api.put("/users/2", json={"name": "morpheus", "job": "zion resident"})
        assert r.status == 200
        assert r.json()["job"] == "zion resident"
        assert "updatedAt" in r.json()

    @pytest.mark.regression
    def test_update_user_patch(self, api):
        r = api.patch("/users/2", json={"job": "zion resident"})
        assert r.status == 200
        assert r.json()["job"] == "zion resident"

    @pytest.mark.regression
    def test_delete_user(self, api):
        r = api.delete("/users/2")
        assert r.status == 204
        assert r.text == ""

    @pytest.mark.regression
    def test_delayed_response(self, api):
        r = api.get("/users", params={"delay": 2})
        assert r.status == 200
        assert r.elapsed_ms >= 2000
        assert len(r.json()["data"]) > 0

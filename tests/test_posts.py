import allure
import pytest
from jsonschema import validate

from framework.data_loader import load_csv, load_json

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "body"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}


@allure.feature("Posts")
class TestPosts:
    @pytest.mark.smoke
    def test_list_posts(self, api):
        r = api.get("/posts")
        assert r.status == 200
        assert len(r.json()) == 100
        assert r.elapsed_ms < 5000

    @pytest.mark.regression
    @pytest.mark.parametrize("case", load_json("posts.json"), ids=lambda c: f"post-{c['id']}")
    def test_get_post_data_driven(self, api, case):
        r = api.get(f"/posts/{case['id']}")
        assert r.status == case["expectedStatus"]
        if case["expectedStatus"] == 200:
            body = r.json()
            validate(body, POST_SCHEMA)
            assert body["userId"] == case["userId"]

    @pytest.mark.regression
    @pytest.mark.parametrize("row", load_csv("new_posts.csv"), ids=lambda r: r["title"])
    def test_create_post_data_driven(self, api, row):
        payload = {"title": row["title"], "body": row["body"], "userId": int(row["userId"])}
        r = api.post("/posts", json=payload)
        assert r.status == int(row["expectedStatus"])
        body = r.json()
        assert body["title"] == payload["title"]
        assert "id" in body

    @pytest.mark.regression
    def test_update_post(self, api):
        r = api.put("/posts/1", json={"id": 1, "title": "updated", "body": "b", "userId": 1})
        assert r.status == 200
        assert r.json()["title"] == "updated"

    @pytest.mark.regression
    def test_patch_post(self, api):
        r = api.patch("/posts/1", json={"title": "patched"})
        assert r.status == 200
        assert r.json()["title"] == "patched"

    @pytest.mark.regression
    def test_delete_post(self, api):
        assert api.delete("/posts/1").status == 200

    @pytest.mark.regression
    def test_filter_posts_by_user(self, api):
        r = api.get("/posts", params={"userId": 1})
        assert r.status == 200
        assert all(p["userId"] == 1 for p in r.json())

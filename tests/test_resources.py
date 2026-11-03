import allure
import pytest
from jsonschema import validate

from framework import schemas
from framework.data_loader import load_json


@allure.feature("Resources")
class TestResources:
    @pytest.mark.smoke
    def test_list_resources(self, api):
        r = api.get("/unknown")
        assert r.status == 200
        validate(r.json(), schemas.page_of(schemas.RESOURCE))

    @pytest.mark.regression
    @pytest.mark.parametrize("case", load_json("resources.json"), ids=lambda c: c["name"])
    def test_get_resource_data_driven(self, api, case):
        r = api.get(f"/unknown/{case['id']}")
        assert r.status == 200
        resource = r.json()["data"]
        validate(resource, schemas.RESOURCE)
        assert resource["name"] == case["name"]
        assert resource["year"] == case["year"]
        assert resource["color"] == case["color"]

    @pytest.mark.regression
    def test_resource_not_found(self, api):
        assert api.get("/unknown/23").status == 404

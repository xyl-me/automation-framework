import pytest
import allure
from pydantic import BaseModel
from base.base_api import BaseAPI

class Pet(BaseModel):
    id: int = None
    name: str
    status: str

@allure.feature("Pet API")
@allure.story("宠物管理")
class TestPetAPI:

    @pytest.fixture
    def api(self):
        return BaseAPI()

    @allure.title("新增宠物并验证响应结构")
    def test_add_pet(self, api):
        pet_data = {
            "id": 1001,
            "name": "doggie",
            "status": "available"
        }
        response = api.post("/pet", json=pet_data)
        assert response.status_code == 200
        pet = Pet(**response.json())
        assert pet.name == "doggie"
        assert pet.status == "available"

    @allure.title("根据 petId 查询宠物")
    def test_get_pet_by_id(self, api):
        pet_id = 1001
        response = api.get(f"/pet/{pet_id}")
        assert response.status_code == 200
        pet = Pet(**response.json())
        assert pet.id == pet_id

    @allure.title("删除宠物")
    def test_delete_pet(self, api):
        pet_id = 1001
        # 先删除
        delete_resp = api.delete(f"/pet/{pet_id}")
        assert delete_resp.status_code == 200
        # 再查询应返回 404
        get_resp = api.get(f"/pet/{pet_id}")
        assert get_resp.status_code == 404
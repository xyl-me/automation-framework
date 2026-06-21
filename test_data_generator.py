import os
import csv
import json
import pytest
from faker import Faker


# ---------------------------- 1. 验证生成的文件是否存在 ----------------------------
def test_files_exist():
    """测试所有预期文件是否生成"""
    expected_files = [
        "test_data/users.csv",
        "test_data/users.json",
        "test_data/boundary_age.csv",
        "test_data/boundary_phone.csv",
        "test_data/boundary_username.csv",
        "test_data/boundary_email.csv",
        "test_data/boundary_all.json"
    ]
    for file_path in expected_files:
        assert os.path.exists(file_path), f"文件不存在: {file_path}"
    print("✅ 所有文件存在性验证通过")


# ---------------------------- 2. 验证正常用户数据 ----------------------------
def test_normal_users_csv():
    """验证 users.csv 文件结构及数据质量"""
    with open("test_data/users.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 1. 数据总量应为1000条
    assert len(rows) == 1000, f"期望1000条，实际{len(rows)}条"

    # 2. 检查字段是否齐全
    expected_fields = {"id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"}
    assert expected_fields.issubset(reader.fieldnames), f"缺少字段: {expected_fields - set(reader.fieldnames)}"

    # 3. 抽样检查数据格式（前几条）
    for row in rows[:5]:
        # id 必须是数字
        assert row["id"].isdigit(), f"id非数字: {row['id']}"
        # 用户名、邮箱、手机号不能为空
        assert row["username"], "用户名为空"
        assert "@" in row["email"], f"邮箱格式错误: {row['email']}"
        assert len(row["phone"]) >= 11, f"手机号过短: {row['phone']}"
        # userStatus 应为0或1
        assert row["userStatus"] in ("0", "1"), f"userStatus异常: {row['userStatus']}"

    print("✅ 正常用户CSV数据验证通过")


def test_normal_users_json():
    """验证 users.json 文件结构与数据一致性（与CSV对比）"""
    with open("test_data/users.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 1. 数据量应为1000条
    assert len(json_data) == 1000

    # 2. 检查每个用户字段类型
    for user in json_data[:5]:
        assert isinstance(user["id"], int)
        assert isinstance(user["username"], str)
        assert "@" in user["email"]
        assert user["userStatus"] in (0, 1)

    # 3. 验证与CSV数据的一致性（抽样前5条）
    with open("test_data/users.csv", "r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        csv_rows = list(csv_reader)
    for i in range(5):
        assert str(json_data[i]["id"]) == csv_rows[i]["id"]
        assert json_data[i]["username"] == csv_rows[i]["username"]
        assert json_data[i]["email"] == csv_rows[i]["email"]

    print("✅ 正常用户JSON数据验证通过")


# ---------------------------- 3. 验证边界值数据 ----------------------------
def test_boundary_age():
    """测试年龄边界数据：包含0,1,18,60,121"""
    with open("test_data/boundary_age.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    expected_ages = {"0", "1", "18", "60", "121"}
    actual_ages = {row["age"] for row in rows}
    assert actual_ages == expected_ages, f"年龄边界值不完整，应为{expected_ages}，实际{actual_ages}"

    # 检查用户名应包含边界信息
    for row in rows:
        assert f"boundary_age_{row['age']}" in row["username"]
    print("✅ 年龄边界数据验证通过")


def test_boundary_phone():
    """测试手机号边界数据：包含空、正常、超长、含字母、过短"""
    with open("test_data/boundary_phone.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 预期手机号用例数（至少5条）
    assert len(rows) >= 5
    # 检查特殊用例：空手机号
    empty_phone = [r for r in rows if r["phone"] == ""]
    assert len(empty_phone) == 1, "空手机号用例缺失"
    # 检查超长手机号（12位）
    long_phone = [r for r in rows if len(r["phone"]) == 12]
    assert len(long_phone) == 1, "12位手机号用例缺失"
    # 检查含字母手机号
    alpha_phone = [r for r in rows if any(c.isalpha() for c in r["phone"])]
    assert len(alpha_phone) == 1, "含字母手机号用例缺失"
    print("✅ 手机号边界数据验证通过")


def test_boundary_username():
    """测试用户名长度边界：1位、20位、21位、含特殊字符、含空格"""
    with open("test_data/boundary_username.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    length_map = {}
    for row in rows:
        length_map[len(row["username"])] = row["username"]

    # 预期长度：1,20,21
    assert 1 in length_map
    assert 20 in length_map
    assert 21 in length_map
    # 检查特殊字符用例
    special = [r for r in rows if any(c in r["username"] for c in "@#$%")]
    assert len(special) >= 1
    print("✅ 用户名边界数据验证通过")


def test_boundary_email():
    """测试邮箱格式边界：正常、无@、多个@、开头特殊字符、含空格、纯数字"""
    with open("test_data/boundary_email.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    cases = {row["firstName"] for row in rows}  # firstName 存储用例描述
    expected_cases = {"正常邮箱", "无@符号", "多个@符号", "开头特殊字符", "包含空格", "纯数字邮箱"}
    assert expected_cases.issubset(cases), f"缺失邮箱用例: {expected_cases - cases}"

    # 验证无@符号的邮箱确实不含@
    no_at = [r for r in rows if r["firstName"] == "无@符号"][0]
    assert "@" not in no_at["email"]
    print("✅ 邮箱边界数据验证通过")


# ---------------------------- 4. 可选：调用 Petstore API 测试注册用户（需网络） ----------------------------
@pytest.mark.sketch  # 标记为草图测试，默认不执行，如需执行请去掉该标记
def test_register_user_with_generated_data():
    """使用生成的数据向 Petstore API 发送 POST 请求，验证接口响应"""
    import requests
    from base.base_api import BaseAPI  # 如果你有 BaseAPI 类，可以复用；否则直接用 requests

    # 加载前3条正常用户数据
    with open("test_data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    api = BaseAPI()  # 假设你已有 base_api.py
    # 或直接使用 requests：BASE_URL = "https://petstore.swagger.io/v2"

    success_count = 0
    for user in users[:3]:
        response = api.post("/user", json=user)
        if response.status_code == 200:
            success_count += 1
            print(f"✅ 用户 {user['username']} 注册成功")
        else:
            print(f"❌ 用户 {user['username']} 注册失败，状态码: {response.status_code}")

    assert success_count >= 2, "注册成功率过低"
    print("✅ API 调用测试通过")


# ---------------------------- 5. 运行测试入口 ----------------------------
if __name__ == "__main__":
    # 使用 pytest 运行本文件
    pytest.main([__file__, "-v", "-s"])
import csv
import json
from faker import Faker

fake = Faker('zh_CN')
Faker.seed(42)


def generate_normal_user(user_id):
    """生成正常用户数据（用于对照）"""
    return {
        "id": user_id,
        "username": fake.user_name(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=10),
        "phone": fake.phone_number(),
        "userStatus": 1
    }


def generate_boundary_age_users():
    """生成年龄边界值测试数据"""
    age_cases = [0, 1, 18, 60, 121]
    users = []
    for i, age in enumerate(age_cases, start=1):
        user = {
            "id": 1000 + i,
            "username": f"boundary_age_{age}",
            "firstName": f"年龄",
            "lastName": f"{age}岁",
            "email": f"age_{age}@test.com",
            "password": "123456",
            "phone": fake.phone_number(),
            "age": age,  # 测试年龄字段的边界
            "userStatus": 1
        }
        users.append(user)
        print(f"边界用例: 年龄 = {age}")
    return users


def generate_boundary_phone_users():
    """生成手机号边界值测试数据"""
    phone_cases = [
        ("空手机号", ""),
        ("11位正常手机号", fake.phone_number()),
        ("12位超长手机号", "138123456789"),
        ("含字母手机号", "138abc45678"),
        ("9位过短手机号", "123456789")
    ]
    users = []
    for i, (case_desc, phone) in enumerate(phone_cases, start=1):
        user = {
            "id": 2000 + i,
            "username": f"boundary_phone_{i}",
            "firstName": case_desc,
            "lastName": "测试",
            "email": f"phone_{i}@test.com",
            "password": "123456",
            "phone": phone,
            "userStatus": 0  # 异常数据可能不会注册成功
        }
        users.append(user)
        print(f"边界用例: {case_desc} = '{phone}'")
    return users


def generate_boundary_username_users():
    """生成长度边界值测试数据"""
    username_cases = [
        ("1位用户名", "a"),
        ("20位最大长度", "a" * 20),
        ("21位超限用户名", "a" * 21),
        ("含特殊字符用户名", "admin@#$%"),
        ("含空格用户名", "test user")
    ]
    users = []
    for i, (case_desc, username) in enumerate(username_cases, start=1):
        user = {
            "id": 3000 + i,
            "username": username,
            "firstName": case_desc,
            "lastName": "测试",
            "email": f"username_{i}@test.com",
            "password": "123456",
            "phone": fake.phone_number(),
            "userStatus": 0
        }
        users.append(user)
        print(f"边界用例: {case_desc} = '{username}'")
    return users


def generate_boundary_email_users():
    """生成邮箱格式边界值测试数据"""
    email_cases = [
        ("正常邮箱", fake.email()),
        ("无@符号", "testexample.com"),
        ("多个@符号", "test@@example.com"),
        ("开头特殊字符", "-test@example.com"),
        ("包含空格", "test user@example.com"),
        ("纯数字邮箱", "123456")
    ]
    users = []
    for i, (case_desc, email) in enumerate(email_cases, start=1):
        user = {
            "id": 4000 + i,
            "username": f"boundary_email_{i}",
            "firstName": case_desc,
            "lastName": "测试",
            "email": email,
            "password": "123456",
            "phone": fake.phone_number(),
            "userStatus": 0
        }
        users.append(user)
        print(f"边界用例: {case_desc} = '{email}'")
    return users


def save_to_csv(users, filename):
    if not users:
        return
    keys = users[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(users)
    print(f"✅ CSV数据已保存至: {filename}")


def save_to_json(users, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON数据已保存至: {filename}")


def main():
    print("=" * 50)
    print("开始生成边界值测试数据...")
    print("=" * 50)

    # 1. 年龄边界值（用于年龄输入框测试）
    print("\n📌 1. 年龄边界值数据")
    age_users = generate_boundary_age_users()
    save_to_csv(age_users, "test_data/boundary_age.csv")

    # 2. 手机号边界值
    print("\n📌 2. 手机号边界值数据")
    phone_users = generate_boundary_phone_users()
    save_to_csv(phone_users, "test_data/boundary_phone.csv")

    # 3. 用户名长度边界值
    print("\n📌 3. 用户名长度边界值数据")
    username_users = generate_boundary_username_users()
    save_to_csv(username_users, "test_data/boundary_username.csv")

    # 4. 邮箱格式边界值
    print("\n📌 4. 邮箱格式边界值数据")
    email_users = generate_boundary_email_users()
    save_to_csv(email_users, "test_data/boundary_email.csv")

    # 5. 合并所有边界数据为JSON
    all_boundary = age_users + phone_users + username_users + email_users
    save_to_json(all_boundary, "test_data/boundary_all.json")

    print("\n" + "=" * 50)
    print(f"✅ 边界值数据生成完成！共 {len(all_boundary)} 条测试数据")
    print(f"   - boundary_age.csv: 年龄边界")
    print(f"   - boundary_phone.csv: 手机号边界")
    print(f"   - boundary_username.csv: 用户名长度边界")
    print(f"   - boundary_email.csv: 邮箱格式边界")
    print(f"   - boundary_all.json: 全部合并数据")
    print("=" * 50)


if __name__ == "__main__":
    main()
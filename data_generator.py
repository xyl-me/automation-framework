import csv
import json
import random
from faker import Faker

# 初始化Faker，使用中文语言
fake = Faker('zh_CN')

# 设置随机种子，保证每次生成的数据一致，便于复现测试
Faker.seed(42)
random.seed(42)


def generate_user(user_id):
    """
    生成单个用户数据
    """
    return {
        "id": user_id,
        "username": fake.user_name(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=10),
        "phone": fake.phone_number(),
        "userStatus": random.choice([0, 1])
    }


def generate_batch_users(count):
    """
    批量生成用户数据
    """
    users = []
    for i in range(1, count + 1):
        user = generate_user(i)
        users.append(user)
    return users


def save_to_csv(users, filename):
    """
    将用户数据导出为CSV文件
    """
    if not users:
        return
    keys = users[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(users)
    print(f"✅ CSV数据已保存至: {filename}")


def save_to_json(users, filename):
    """
    将用户数据导出为JSON文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON数据已保存至: {filename}")


def main():
    print("开始生成用户测试数据...")
    users = generate_batch_users(1000)
    print(f"✅ 已生成 {len(users)} 条用户数据")

    # 导出为CSV和JSON
    save_to_csv(users, "test_data/users.csv")
    save_to_json(users, "test_data/users.json")

    # 打印前3条示例数据
    print("\n📋 示例数据（前3条）:")
    for user in users[:3]:
        print(user)


if __name__ == "__main__":
    main()
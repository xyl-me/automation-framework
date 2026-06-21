# OrangeHRM + Petstore 自动化测试套件

[![Python 3.11+](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/pytest-8.0+-green.svg)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-2.32.0-orange.svg)](https://allurereport.org/)
[![GitHub Actions](https://github.com/yourusername/orangehrm-automation/actions/workflows/run_tests.yml/badge.svg)](https://github.com/yourusername/orangehrm-automation/actions)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com/)

> 企业级 UI + API 自动化测试框架 | Pytest + Selenium + Page Object | Allure 报告 | Docker 化 | CI/CD 集成

## 🚀 核心特性

- **UI 自动化**：OrangeHRM 人力资源管理平台（登录、员工增删查改）
- **API 自动化**：Petstore Swagger 开放接口（宠物模块）
- **Page Object Model**：UI 元素与测试逻辑完全解耦
- **数据驱动**：CSV 文件管理测试数据，支持多场景批量验证
- **Allure 报告**：自动生成带截图、请求/响应、步骤的美观报告
- **持续集成**：GitHub Actions 每日定时 + PR 自动触发，报告发布至 GitHub Pages
- **容器化运行**：Docker + Docker Compose 一键执行，环境零依赖

## 📦 技术栈

| 领域         | 工具/库                          |
|--------------|----------------------------------|
| 测试框架     | Pytest                           |
| UI 自动化    | Selenium + WebDriver Manager     |
| API 自动化   | Requests + Pydantic              |
| 报告         | Allure Framework                 |
| CI/CD        | GitHub Actions                   |
| 容器化       | Docker, Docker Compose           |
| 版本控制     | Git                              |

## 🛠️ 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/orangehrm-automation.git
cd orangehrm-automation


# 有界面模式（默认）
    # pytest

    # 无头模式（CI 推荐）
    # pytest - -headless

    # 仅 UI 测试
    # pytest tests / ui_tests /
    #

    # 仅 API 测试
    # pytest tests / api_tests /


    #pytest --alluredir=allure-results
    #allure serve allure-results

#使用 Docker 运行（无需本地 Chrome）
#bash
#cd docker
#docker-compose up --build


pytest tests/ui_tests/test_login.py -v



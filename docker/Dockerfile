FROM python:3.11-slim

# 安装 Chrome 浏览器（用于 Selenium）
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 安装 Allure 命令行
RUN curl -sL https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz | tar -xz -C /opt/ \
    && ln -s /opt/allure-2.32.0/bin/allure /usr/local/bin/allure

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# 默认命令：运行全部测试并生成 Allure 报告
CMD ["pytest", "tests/", "--alluredir=allure-results", "--headless"]
# 企业微信 Webhook 转发器

这是一个基于 Python Flask 的轻量级 Webhook 服务，用于将格式化的消息通过企业微信（WeCom）的应用进行推送。

## 功能特性

-   **Webhook 入口**: 提供一个标准的 `/` POST 接口用于接收消息。
-   **健康检查**: 提供 `/health` GET 接口，便于容器编排系统进行健康状态探测。
-   **认证机制**: 支持基于 `Authorization: Bearer <token>` 的请求头认证。
-   **Markdown 格式**: 专为企业微信优化的 Markdown 消息格式。
-   **灵活配置**: 同时支持 `config.yaml` 文件和环境变量进行配置，环境变量优先级更高。
-   **容器化支持**: 提供 `Dockerfile`，支持健康检查，并优化了国内构建体验。
-   **部署清单**: 提供 `deployment.yaml`，用于快速部署到 Kubernetes (K3s) 环境。
-   **版本管理**: 通过 `VERSION` 文件和 `CHANGELOG.md` 进行规范的版本和变更管理。

## API 端点

### `POST /`

用于发送消息。

-   **请求头**:
    -   `Content-Type: application/json`
    -   `Authorization: Bearer YOUR_SECRET_AUTH_TOKEN`
-   **请求体 (JSON)**:
    ```json
    {
      "content": "您的 Markdown 格式消息"
    }
    ```
-   **请求示例**:
    ```bash
    curl -X POST http://127.0.0.1:5000/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_secret_auth_token" \
    -d '{
        "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n> 类型:<font color=\"comment\">用户反馈</font> \n> 普通用户反馈:<font color=\"info\">110例</font> \n> VIP用户反馈:<font color=\"comment\">22例</font>"
    }'
    ```

### `GET /health`

用于健康检查。

-   **请求示例**:
    ```bash
    curl http://127.0.0.1:5000/health
    ```
-   **成功响应**:
    ```json
    {
      "status": "ok"
    }
    ```

## 本地运行

### 1. 准备

-   安装 Python 3.x
-   克隆本仓库

### 2. 配置

复制 `config.yaml.tmpl` 为 `config.yaml`，并填入您的企业微信应用凭证和自定义的 `AUTH_TOKEN`。

```yaml
# 企业微信公司ID
WECOM_CORPID: "your_corpid_here"
# 企业微信应用ID
WECOM_AGENTID: "your_agentid_here"
# 企业微信应用Secret
WECOM_APPSEC: "your_appsec_here"
# Webhook 鉴权 Token
AUTH_TOKEN: "your_secret_auth_token"
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动服务

```bash
python main.py
```
服务将默认在 `http://0.0.0.0:5000` 启动。

## Docker 部署

### 1. 构建镜像

该命令会自动读取 `VERSION` 文件作为镜像标签。

```bash
# 通用命令
docker build -t wxchat_webhook:$(cat VERSION) .

# 国内加速构建
docker build --build-arg ZONE=CN -t wxchat_webhook:$(cat VERSION) .
```
> **Windows 用户提示**: 在 PowerShell 中使用 `$(Get-Content VERSION)` 替代 `$(cat VERSION)`。

### 2. 运行容器

**方式一：通过挂载 `config.yaml` 文件 (推荐用于测试)**

```bash
docker run -d -p 5000:5000 \
--name wxchat-webhook-app \
-v $(pwd)/config.yaml:/app/config.yaml \
wxchat_webhook:$(cat VERSION)
```

**方式二：通过环境变量 (推荐用于生产)**

```bash
docker run -d -p 5000:5000 \
--name wxchat-webhook-app \
-e WECOM_CORPID="your_corpid_here" \
-e WECOM_AGENTID="your_agentid_here" \
-e WECOM_APPSEC="your_appsec_here" \
-e AUTH_TOKEN="your_secret_auth_token" \
wxchat_webhook:$(cat VERSION)
```

## 部署

关于如何将此应用部署到 Kubernetes 以及如何与 GitLab CI/CD 集成，请参考以下专门的文档：

-   **[Kubernetes 部署指南](./docs/kubernetes_deployment.md)**
-   **[GitLab CI/CD 集成指南](./docs/cicd_integration.md)**
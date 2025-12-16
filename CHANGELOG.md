# 变更日志

所有此项目的显著变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
且本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。
## [1.2.0] - 2025-12-03

### 新增

-   为应用增加 `/health` 健康检查端点（由用户实现）。
-   在 `Dockerfile` 中添加 `HEALTHCHECK` 指令，以利用容器运行时的健康检查能力。
-   在 `deployment.yaml` 中为 Kubernetes 部署添加 `livenessProbe` 和 `readinessProbe`，以实现更可靠的部署和服务管理。

### 变更

-   **部署清单**:
    -   将 `deployment.yaml` 中的 `Service` 类型从 `NodePort` 修改为 `ClusterIP`。
    -   在 `deployment.yaml` 中添加了基于 Kong 的 `Ingress` 资源定义，以通过域名暴露服务。
-   **文档**:
    -   将 `README.md` 中关于 Kubernetes 和 CI/CD 的部署说明剥离为独立的文档 (`docs/kubernetes_deployment.md` 和 `docs/cicd_integration.md`)。
    -   更新 `README.md` 以链接到新的部署指南。
    -   更新 `main.py` webook 接收路径改变至 `/` 根目录下

### 修复

-   修正 `.gitlab-ci.yml` 文件中的 YAML 语法错误，确保 `script` 块中的命令列表和多行命令格式正确，以通过 GitLab CI 的 Linter 校验。


## [1.1.0] - 2025-12-03

### 新增

-   `deployment.yaml` 文件，用于将应用部署到 Kubernetes (K3s) 集群。
-   `VERSION` 文件，用于项目版本管理。
-   更新 `README.md`，增加了 Kubernetes 部署说明和 GitLab CI/CD 集成示例。


## [1.0.0] - 2025-12-03

### 新增

-   基于 Flask 的 webhook 主服务 (`main.py`)，用于接收和转发消息。
-   通过 `config.yaml` 和环境变量进行配置。
-   支持 Bearer Token 鉴权。
-   支持向企业微信应用发送 Markdown 消息。
-   `requirements.txt` 文件，用于管理 Python 依赖。
-   `.gitignore` 文件，用于忽略敏感配置和缓存文件。
-   `Dockerfile` 用于容器化部署。
-   `README.md` 提供详细的项目介绍和使用说明。

### 优化

-   `Dockerfile` 增加对国内 PyPI 镜像源的支持，以改善国内用户的构建体验。
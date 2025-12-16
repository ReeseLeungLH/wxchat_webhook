# GitLab CI/CD 集成指南

您可以使用项目根目录下的 `.gitlab-ci.yml` 文件将此应用自动化构建和部署。

## 前置条件

在运行 CI/CD 流水线之前，请确保满足以下条件：

1.  **Kubernetes Secret 已创建**: 您已经按照 [Kubernetes 部署指南](./kubernetes_deployment.md) 在目标集群中手动创建了 `wxchat-webhook-secret`。
2.  **GitLab Runner 配置**: GitLab Runner 已正确安装，能够执行 Docker 命令，并且已配置 `kubectl` 使其能够连接到您的 Kubernetes 集群。
3.  **CI/CD 变量**: 在 GitLab 项目的 "Settings" -> "CI/CD" -> "Variables" 中，设置了名为 `KUBE_CONFIG` 的变量，其内容为您的 `kubeconfig` 文件，用于授权 Runner 访问集群。

## 部署流程

流水线配置在 `.gitlab-ci.yml` 中，包含两个主要阶段：

1.  **Build**:
    -   此阶段会构建 Docker 镜像。
    -   镜像的标签（Tag）将从项目根目录的 `VERSION` 文件中读取。
    -   构建完成后，镜像会被推送到 GitLab 项目的内置镜像仓库。

2.  **Deploy**:
    -   此阶段首先使用 `sed` 命令，将 `deployment.yaml` 文件中的 `image` 字段替换为上一步构建的、带有唯一提交 SHA 标签的镜像地址。这是一个最佳实践，确保每次部署都使用确切的镜像版本。
    -   然后，使用 `kubectl apply -f deployment.yaml` 命令，将更新后的部署应用到 Kubernetes 集群。`kubectl apply` 会智能地更新发生变化的资源。

更多实现细节，请直接参考 `.gitlab-ci.yml` 和 `deployment.yaml` 文件中的注释。
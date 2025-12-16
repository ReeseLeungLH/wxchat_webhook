# Kubernetes 部署指南

本文档提供了将 `wxchat-webhook` 应用部署到 Kubernetes (包括 K3s) 集群的详细步骤。部署清单 `deployment.yaml` 包含了 Secret, Deployment, Service 和 Ingress 的完整定义。

## 1. 手动创建 Secret

在进行自动化部署之前，您需要先在您的 Kubernetes 集群中手动创建 `wxchat-webhook-secret`。这个 Secret 包含了应用运行所需的所有敏感凭证。

**请将以下命令中的占位符替换为您的实际值，然后在您的终端中执行：**
```bash
kubectl create secret generic wxchat-webhook-secret \
  -n infra \
  --from-literal=WECOM_CORPID='your_corpid_here' \
  --from-literal=WECOM_AGENTID='your_agentid_here' \
  --from-literal=WECOM_APPSEC='your_appsec_here' \
  --from-literal=AUTH_TOKEN='your_secret_auth_token'
```
> **注意:** 此操作只需执行一次。如果凭证需要更新，您可以删除旧的 Secret (`kubectl delete secret wxchat-webhook-secret -n infra`) 然后重新创建，或者使用 `kubectl edit secret wxchat-webhook-secret -n infra` 进行编辑。

## 2. 应用部署

完成 Secret 创建后，您可以使用提供的 `deployment.yaml` 文件来部署应用。

```bash
kubectl apply -f deployment.yaml
```

此命令将创建或更新 `infra` 命名空间中的以下资源：
- **Deployment**: `wxchat-webhook-deployment`，负责管理应用的 Pod。
- **Service**: `wxchat-webhook-service`，在集群内部暴露应用端口。
- **Ingress**: `wxchat-webhook-ingress`，通过 Kong Ingress Controller 将服务暴露到外部网络。

更多详情，请参考 `deployment.yaml` 文件中的注释。
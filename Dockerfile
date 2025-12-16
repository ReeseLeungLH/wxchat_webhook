# 使用官方 Python 运行时作为父镜像
# 在国内环境构建时，您可能需要使用镜像仓库，例如：
# FROM registry.cn-hangzhou.aliyuncs.com/library/python:3.9-slim
FROM python:3.9-slim

# 设置构建时参数，用于指定区域
ARG ZONE

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖，根据 ZONE 参数选择或回退到国内镜像源
RUN \
  PIP_INDEX_URL="https://pypi.python.org/simple" && \
  CN_PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple" && \
  if [ "$ZONE" = "CN" ]; then \
    echo "ZONE=CN detected, using Chinese mirror: $CN_PIP_INDEX_URL"; \
    pip install --no-cache-dir -i $CN_PIP_INDEX_URL -r requirements.txt; \
  else \
    echo "Using default pip index with fallback to Chinese mirror."; \
    pip install --no-cache-dir -i $PIP_INDEX_URL -r requirements.txt || \
    (echo "Default pip index failed, trying Chinese mirror..." && \
    pip install --no-cache-dir -i $CN_PIP_INDEX_URL -r requirements.txt); \
  fi

# 复制项目代码到工作目录
COPY . .

# 暴露 Flask app 运行的端口
EXPOSE 5000

# 增加健康检查指令
# 使用 curl 检查 /health 端点，--fail 表示如果 HTTP 状态码不是 2xx 则返回错误
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# 定义容器启动时运行的命令
CMD ["python", "main.py"]
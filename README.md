
<img src="assets/vstudio_wordmark.png">

## 1. 创建环境

推荐 Python 3.11 或 3.12。

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## 2. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env`：

```env
ARK_API_KEY=你的火山方舟_API_Key
```

## 3. 本地运行

`config.yaml` 默认：

```yaml
app:
  environment: "local"
```

运行：

```bash
python app.py
```

浏览器访问：

```text
http://127.0.0.1:7860
```

## 4. ModelScope

推荐在 ModelScope Secret / 环境变量里配置：

```text
ARK_API_KEY
```

然后设置环境变量：

```text
APP_ENV=modelscope
```

或者把 `config.yaml` 改为：

```yaml
app:
  environment: "modelscope"
```

ModelScope 模式会监听 `0.0.0.0`。

## 5. 配置职责

- `.env`：API Key 等敏感信息
- `config.yaml`：模型、端口、Prompt、风格、视角
- `config.py`：统一读取和环境变量覆盖
- `agent.py`：Agent 路由 + Seedream API
- `app.py`：Gradio UI

## 6. 环境变量覆盖

环境变量优先级高于 YAML，可用：

```text
ARK_API_KEY
APP_ENV
APP_HOST
APP_PORT
SEEDREAM_MODEL
SEEDREAM_API_URL
```


## HEIC / iPhone 图片支持

图片上传支持： JPG、PNG、WEBP，以及 iPhone 常见的 HEIC/HEIF。

如果pillow是从旧版本升级，请执行：

```bash
pip install -U pillow-heif
```

然后重新启动：

```bash
python app.py
```

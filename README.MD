# PyNCMAPI

PyNCMAPI 是网易云音乐 API 服务的 Python/FastAPI 迁移版，目标是尽量兼容原 Node.js 版的 HTTP 路由、参数形式、cookie 行为、静态页面和模块调用方式。

当前项目已经迁移为 Python 项目形态：接口模块位于 `modules/`，公共请求、加密、配置和服务入口位于根目录。

## 功能特性

- FastAPI HTTP 服务，兼容原接口路由，例如 `/login/status`、`/song/url/v1`、`/playlist/detail`。
- 保留特殊旧路由：`/fm_trash`、`/personal_fm`、`/ugc/user/devote`。
- 支持 query、JSON、form 和 multipart 上传参数。
- 支持 cookie 透传、`NETEASE_COOKIE` 环境变量、CORS、代理和通用解灰配置。
- 支持 Python 直接调用模块函数，例如 `login_status()`。
- 内置 2 分钟成功响应缓存，降低重复请求压力。

## 环境要求

- Python 3.13+
- uv
- 可选：Node.js，用于调用原 `@neteasecloudmusicapienhanced/unblockmusic-utils` 解灰桥接能力

安装 uv 可参考官方安装方式；如果本机已经有 `uv`，直接进入下一步即可。

## 快速开始

安装依赖：

```powershell
uv sync
```

启动服务：

```powershell
uv run python main.py
```

指定地址和端口：

```powershell
uv run python main.py --host 0.0.0.0 --port 3000
```

启动后默认访问：

```text
http://localhost:3000
```

示例请求：

```text
http://localhost:3000/login/status
http://localhost:3000/search?keywords=海阔天空
http://localhost:3000/song/url/v1?id=33894312&level=lossless
```

静态页面也会从 `public/` 目录提供，例如：

```text
http://localhost:3000/login.html
```

## 配置

复制示例环境文件：

```powershell
Copy-Item .env.example .env
```

常用配置项：

```dotenv
# CORS allowed origins, comma-separated
CORS_ALLOW_ORIGIN=

# Proxy settings
ENABLE_PROXY=false
PROXY_URL=

# Song unblock
ENABLE_GENERAL_UNBLOCK=false
ENABLE_FLAC=false

# NetEase cookie, for example: MUSIC_U=xxx
NETEASE_COOKIE=

# Server
PORT=3000
HOST=
```

说明：

- `NETEASE_COOKIE` 可用于需要登录态的接口。
- `CORS_ALLOW_ORIGIN` 为空时会按请求来源返回 CORS 头；设置为 `*` 时允许任意来源。
- `ENABLE_GENERAL_UNBLOCK=true` 会在 `/song/url/v1` 获取失败或试听限制时尝试通用解灰。
- `PROXY_URL` 可配合 `ENABLE_PROXY=true` 使用。

## HTTP 调用

GET 和 POST 都可调用接口。参数可以放在 query string、JSON body、表单 body 或 multipart form 中。

GET 示例：

```powershell
curl "http://localhost:3000/playlist/detail?id=3778678"
```

POST JSON 示例：

```powershell
curl -X POST "http://localhost:3000/search" `
  -H "Content-Type: application/json" `
  -d "{\"keywords\":\"周杰伦\",\"limit\":10}"
```

上传接口示例：

```powershell
curl -X POST "http://localhost:3000/playlist/cover/update" `
  -F "id=123456" `
  -F "imgFile=@cover.jpg"
```

如果需要单次请求传 cookie，可以使用 `cookie` 参数：

```text
/login/status?cookie=MUSIC_U=xxx;__csrf=yyy
```

## Python 调用

项目入口会动态暴露 `modules/` 下的接口函数。函数名与模块文件名一致，参数为 `dict`。

```python
import asyncio
import PyNCMAPI


async def main():
    result = await PyNCMAPI.login_status({
        "cookie": "MUSIC_U=xxx;__csrf=yyy",
    })
    print(result)


asyncio.run(main())
```

也可以获取 FastAPI app：

```python
import PyNCMAPI

app = PyNCMAPI.construct_server()
```

## 测试

运行测试：

```powershell
uv run pytest -q
```

语法编译检查：

```powershell
uv run python -m compileall -q .
```

当前测试覆盖：

- 加密函数
- Node/Python 模块数量和名称对齐
- 特殊路由兼容
- 静态文件服务
- 成功响应缓存
- HTTPS Set-Cookie 兼容
- multipart 上传参数归一化
- 请求层自定义 headers
- Python 包入口调用

## 项目结构

```text
.
├── main.py              # CLI 启动入口
├── server.py            # FastAPI 应用和路由加载
├── request.py           # 网易云请求封装
├── crypto.py            # weapi/eapi/linuxapi 加密
├── config.py            # 配置和常量
├── modules/             # API 接口模块
├── plugins/             # 上传等复用插件
├── public/              # 静态页面和文档资源
├── tests/               # 测试
├── pyproject.toml       # Python 项目配置
└── uv.lock              # uv 锁文件
```

## 迁移状态

PyNCMAPI 以原 Node.js 版 `4.32.0` 行为为兼容基准。当前 Python 模块数量与原 `module/*.js` 对齐，HTTP 路由按文件名生成，并保留原版特殊路由规则。

仍建议在生产使用前对关键接口做一次真实账号和网络环境验证，因为网易云接口本身可能随服务端策略变化而变化。

## License

MIT

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fish Audio TTS 客户端 —— 调用 Fish Audio API 将文本合成为语音，输出 MP3 文件。

## 快速使用

```bash
# 安装依赖
pip install httpx

# 方式一：直接指定文本
python fish.py -t "待合成文本"

# 方式二：从文件读取文本
python fish.py -f input.txt

# 方式三：创建 input.txt 后无参数运行
echo "待合成文本" > input.txt
python fish.py
```

## 配置

API 密钥存放在 `config.json` 中：

```json
{
  "api_key": "你的 Fish Audio API 密钥"
}
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `-t 文本` | 直接传入合成文本 |
| `-f 文件` | 从指定文件读取文本 |
| 无参数 | 尝试读取项目目录下的 `input.txt`，不存在则报错 |

`-t` 和 `-f` 互斥，不能同时使用。

## 运行逻辑

| 步骤 | 说明 |
|------|------|
| 加载配置 | 从 `config.json` 读取 `api_key`，不存在或为空则报错退出 |
| 获取文本 | 按 `-t` / `-f` / 无参数三种模式获取；文本为空则报错退出 |
| 生成文件名 | 取文本前 6 个字作为文件名（如 `大江东去浪淘.mp3`） |
| 重名处理 | 文件已存在则追加 `-序号`（`-1`, `-2`...），最多 99 个 |
| API 调用 | `POST https://api.fish.audio/v1/tts`，`model: s2.1-pro-free` |
| 输出 | 将音频二进制写入 `.mp3` 文件 |

## Fish Audio API 要点

- **模型**: `s2.1-pro-free`（免费版）、`s2-pro`（高质量默认）
- **认证**: `Authorization: Bearer <API_KEY>`
- **输入**: JSON body，`text` 字段为合成文本
- **输出格式**: mp3/wav/pcm/opus
- **超时**: 脚本设置 120 秒超时，网络不稳定时需要等待

## 项目文件

| 文件 | 说明 |
|------|------|
| `fish.py` | 主脚本 |
| `config.json` | API 密钥配置 |

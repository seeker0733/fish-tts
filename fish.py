import argparse
import json
import sys
from pathlib import Path

import httpx

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"错误: 配置文件 {CONFIG_FILE} 不存在")
        print(f"请创建 {CONFIG_FILE}，内容格式:")
        print('  { "api_key": "你的 Fish Audio API 密钥" }')
        sys.exit(1)

    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)

    api_key = config.get("api_key")
    if not api_key:
        print("错误: 配置文件中缺少 api_key 字段")
        sys.exit(1)

    return api_key


def get_text_from_args():
    parser = argparse.ArgumentParser(description="Fish Audio TTS 客户端")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", metavar="文本", help="直接指定合成文本")
    group.add_argument("-f", metavar="文件", help="从文件读取合成文本")
    args = parser.parse_args()

    # -f：从指定文件读取
    if args.f:
        file_path = Path(args.f)
        if not file_path.exists():
            print(f"错误: 文件不存在 {file_path}")
            sys.exit(1)
        return file_path.read_text(encoding="utf-8").strip()

    # -t：直接使用传入文本
    if args.t:
        text = args.t.strip()
        if not text:
            print("错误: 文本不能为空")
            sys.exit(1)
        return text

    # 无参数：尝试读取 input.txt
    input_file = SCRIPT_DIR / "input.txt"
    if input_file.exists():
        return input_file.read_text(encoding="utf-8").strip()

    print(f"错误: 未指定文本，请使用 -t 或 -f 参数，或创建 {input_file}")
    sys.exit(1)


def get_output_path(text):
    base_name = text[:6]
    mp3_path = SCRIPT_DIR / f"{base_name}.mp3"
    if not mp3_path.exists():
        return mp3_path

    for i in range(1, 100):
        mp3_path = SCRIPT_DIR / f"{base_name}-{i}.mp3"
        if not mp3_path.exists():
            return mp3_path

    print("错误: 文件名冲突过多（超过 99 个）")
    sys.exit(1)


def tts(api_key, text):
    body = {
        "text": text,
        "format": "mp3",
    }

    with httpx.Client(timeout=120) as client:
        res = client.post(
            "https://api.fish.audio/v1/tts",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "model": "s2.1-pro-free",
            },
            json=body,
        )

    res.raise_for_status()
    return res.content


def main():
    api_key = load_config()
    text = get_text_from_args()
    output_path = get_output_path(text)

    audio_data = tts(api_key, text)

    with open(output_path, "wb") as f:
        f.write(audio_data)

    print(f"成功生成音频: {output_path}")


if __name__ == "__main__":
    main()

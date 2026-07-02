Fish Audio TTS 客户端 —— 调用 Fish Audio API 将文本合成为语音，输出 MP3 文件。

1、命令行参数
只要运行就可以生成你指定文字所合成的音频。
输入文本可以通过txt，也可以通过命令行参数输入
1、如果有input.txt，直接运行fish.py，默认读取该文件
2、如果有别的txt，则fish.py -f 文件名.txt
3、如果是在命令行输入文本，则 fish.py -t 文本字符

2、配置文件内容
config.json：
{
  "api_key": "xxxxx"
}
api_key，就是fish audio的免费key

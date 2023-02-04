

```
本文阐述了QuecPython的audio模块的用法，描述了audio模块最新版本的特性。
```



# <font color='red'>`audio` </font> - 音频播放相关功能

`audio`模块包含音频播放相关的功能，支持TTS、mp3以及AMR文件播放。

**示例：**

```python
import audio

if __name__ == '__main__':
    tts = audio.TTS(1)
    tts.play(1, 1, 2, 'QuecPython') # 执行播放
    tts.close()   # 关闭TTS功能
```



## Classes

- [class TTS](./audio.TTS.md)

- [class Audio](audio.Audio.md)

- [class Record](audio.Record.md)


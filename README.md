# ClipMP4Tube

ffmpeg - YouTube Clip To MP4

## 安裝

```
choco install ffmpeg
pip install yt-dlp
```

## 使用方法

```
python ytmp4.py <YouTube網址> -s <開始時間> -e <結束時間> -o <輸出檔名>
```

## 範例

```
python ytmp4.py https://www.youtube.com/watch?v=ldOn4FfS98A -s 4:54 -e 4:57 -o output.mp4
```

## 參數格式

- `-s`, `--start`: 開始時間 (格式: 秒數 或 "分:秒" 或 "時:分:秒")
- `-e`, `--end`: 結束時間 (同上)
- `-o`, `--output`: 輸出檔案名稱

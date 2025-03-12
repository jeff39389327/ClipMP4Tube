import yt_dlp
import argparse
import os
import tempfile
import shutil

def download_youtube_video(url, start_time=None, end_time=None, output_file=None):
    """
    下載YouTube影片的指定時間區段
    
    參數:
        url (str): YouTube影片網址
        start_time (str): 開始時間 (格式: 秒數或 "分:秒" 或 "時:分:秒")
        end_time (str): 結束時間 (格式同上)
        output_file (str): 輸出檔案名稱
    """
    # 獲取影片信息
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    # 如果沒有指定輸出檔案，使用影片標題
    if not output_file:
        output_file = f"{info['title']}.mp4"
        # 移除檔名中的非法字符
        output_file = "".join(c for c in output_file if c.isalnum() or c in " ._-").strip()
    
    # 確保有 .mp4 副檔名
    if not output_file.lower().endswith('.mp4'):
        output_file += '.mp4'
    
    print(f"影片標題: {info['title']}")
    print(f"影片時長: {format_seconds(info['duration'])}")
    
    # 創建臨時目錄
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "temp_download.%(ext)s")
    
    try:
        # 解析時間範圍
        start_seconds = parse_time(start_time) if start_time else 0
        end_seconds = parse_time(end_time) if end_time else None
        
        time_range_str = ""
        if start_seconds > 0 or end_seconds is not None:
            time_range_str = f"從 {format_seconds(start_seconds)} 到 "
            time_range_str += f"{format_seconds(end_seconds)}" if end_seconds else "結束"
            print(f"下載時間區段: {time_range_str}")
        
        # 準備下載選項
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': temp_file,
            'quiet': False,
        }
        
        # 添加時間範圍處理
        if start_seconds > 0 or end_seconds is not None:
            ydl_opts['postprocessor_args'] = {
                'ffmpeg': []
            }
            
            if start_seconds > 0:
                ydl_opts['postprocessor_args']['ffmpeg'].extend(['-ss', str(start_seconds)])
            
            if end_seconds is not None:
                duration = end_seconds - start_seconds
                ydl_opts['postprocessor_args']['ffmpeg'].extend(['-t', str(duration)])
        
        print(f"開始下載影片...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # 尋找下載好的檔案
        downloaded_files = os.listdir(temp_dir)
        if not downloaded_files:
            raise Exception("下載失敗，沒有找到下載的檔案")
        
        downloaded_file = os.path.join(temp_dir, downloaded_files[0])
        
        # 移動到最終位置
        shutil.move(downloaded_file, output_file)
        print(f"影片已成功下載到 {os.path.abspath(output_file)}")
        
    finally:
        # 清理臨時目錄
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"警告: 清理臨時檔案失敗: {str(e)}")

def parse_time(time_str):
    """解析時間字符串為秒數"""
    if not time_str:
        return 0
    
    try:
        # 如果只是數字，直接當作秒數
        if str(time_str).isdigit():
            return int(time_str)
        
        # 處理 分:秒 格式
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                minutes, seconds = parts
                return int(minutes) * 60 + int(seconds)
            elif len(parts) == 3:
                hours, minutes, seconds = parts
                return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        
        # 嘗試直接轉換為浮點數（秒）
        return float(time_str)
        
    except ValueError:
        raise ValueError(f"無法解析時間格式: {time_str}")

def format_seconds(seconds):
    """將秒轉換為 HH:MM:SS 格式"""
    if seconds is None:
        return "結束"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='下載YouTube影片的指定時間區段')
    parser.add_argument('url', help='YouTube影片網址')
    parser.add_argument('-s', '--start', help='開始時間 (格式: 秒數或 "分:秒" 或 "時:分:秒")')
    parser.add_argument('-e', '--end', help='結束時間 (格式同上)')
    parser.add_argument('-o', '--output', help='輸出檔案名稱')
    
    args = parser.parse_args()
    
    try:
        download_youtube_video(args.url, args.start, args.end, args.output)
    except Exception as e:
        print(f"錯誤: {str(e)}")
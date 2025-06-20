import requests
import os
import json
from datetime import datetime, timedelta

def download_epg():

    url = os.environ.get("EPG_URL", "")
    output_file = "pl.xml.gz"
    
    try:
        print(f"开始下载EPG数据...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # 转换为MB
        print(f"下载完成! 文件大小: {file_size:.2f} MB")
        
        # 获取北京时间
        beijing_time = get_beijing_time()
        print(f"更新时间: {beijing_time}")
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False

def get_json_info():

    json_url = os.environ.get("JSON_URL", "")
    json_output_file = "pl.json"
    
    try:
        print(f"开始获取JSON数据...")
        response = requests.get(json_url)
        response.raise_for_status()
        
        # 保存完整的JSON文件
        with open(json_output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        # 解析JSON并提取所有频道信息
        data = response.json()
        
        # 获取频道列表
        channels = []
        if isinstance(data, list):
            # 如果是频道列表数组
            channels = data
        elif isinstance(data, dict) and "channels" in data:
            # 如果是包含channels字段的对象
            channels = data.get("channels", [])
        elif isinstance(data, dict):
            # 如果是单个频道信息
            channels = [data]
            
        print(f"JSON数据获取完成! 共找到 {len(channels)} 个频道")
        
        # 更新README文件
        update_readme(channels)
        
        return channels
    except Exception as e:
        print(f"获取JSON数据失败: {str(e)}")
        return None

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    utc_now = datetime.utcnow()
    beijing_time = utc_now + timedelta(hours=8)
    return beijing_time.strftime('%Y-%m-%d %H:%M:%S')

def update_readme(channels):
    try:
        # 生成频道列表表格
        channel_table = "| 频道名称 | 数据源 | 节目数量 | 日期范围 |\n| --- | --- | --- | --- |\n"
        
        for channel in channels:
            name = channel.get("name", "未知")
            source = channel.get("source", "未知")
            count = channel.get("programme_count", 0)
            
            date_range = channel.get("date_range", {})
            start_date = date_range.get("start", "未知")
            end_date = date_range.get("end", "未知")
            date_info = f"{start_date} 至 {end_date}"
            
            channel_table += f"| {name} | {source} | {count} | {date_info} |\n"
        
        # 获取北京时间
        beijing_time = get_beijing_time()
        
        readme_content = f"""# EPG-电子节目单

## 使用方法

### 直接下载
您可以直接从仓库下载最新的EPG数据文件：
```
https://raw.githubusercontent.com/litiande03/epg/refs/heads/master/pl.xml.gz
```
或
```
https://github.com/litiande03/epg/raw/refs/heads/master/pl.xml.gz
```

### 在IPTV播放器中使用
在大多数IPTV播放器中，您可以直接设置EPG源为上述URL。

## 更新信息
- **最后更新时间**: {beijing_time} (北京时间)
- **频道总数**: {len(channels)}

## 频道列表
{channel_table}
"""
        
        with open("README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"README.md 更新成功!")
        return True
    except Exception as e:
        print(f"更新README.md失败: {str(e)}")
        return False

if __name__ == "__main__":
    download_epg()
    get_json_info() 

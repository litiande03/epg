# EPG数据自动更新仓库

此仓库每天自动获取最新的EPG数据（电子节目指南），并保存为`pl.xml.gz`文件。

## 文件说明

- `pl.xml.gz` - 最新的EPG数据文件（自动更新）
- `update_epg.py` - 用于下载EPG数据的Python脚本
- `.github/workflows/update-epg.yml` - GitHub Actions工作流配置

## 安全设置

为保护EPG数据源地址，本仓库使用GitHub Secrets存储敏感URL。您需要设置以下Secret：

1. 前往仓库的"Settings" > "Secrets and variables" > "Actions"
2. 点击"New repository secret"
3. 名称填写`EPG_URL`
4. 值填写您的EPG数据源完整URL
5. 点击"Add secret"保存

设置后，工作流将使用此Secret访问EPG数据源，而不会在代码中暴露URL。

## 自动更新

EPG数据会通过GitHub Actions自动每天更新一次。更新时间为每天UTC时间0:00（北京时间8:00）。

## 使用方法

### 直接下载

您可以直接从仓库下载最新的EPG数据文件：
```
https://raw.githubusercontent.com/你的用户名/你的仓库名/main/pl.xml.gz
```

### 在IPTV播放器中使用

在大多数IPTV播放器中，您可以直接设置EPG源为上述URL。

## 手动触发更新

如需手动触发更新，可以：
1. 前往仓库的"Actions"标签页
2. 选择"每日更新EPG数据"工作流
3. 点击"Run workflow"
4. 确认运行

## 本地运行

如需在本地运行更新脚本：

```bash
# 安装依赖
pip install requests

# 设置环境变量并运行脚本
export EPG_URL="您的EPG数据源URL"
python update_epg.py
``` 
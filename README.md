# 房产成交数据看板 🏠

实时整合每日网签数据,助您洞察市场动态。

## 📊 功能特性

- **数据整合**: 自动读取并整合多个 Excel 文件的房产成交数据
- **可视化分析**: 
  - 每日成交量趋势图
  - 各区域成交占比
  - 单价分布分析
- **灵活筛选**: 支持日期、区域、价格、面积等多维度筛选
- **模糊搜索**: 快速查找特定小区
- **深色模式**: 支持浅色/深色主题切换

## 🚀 本地运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 准备数据
将 Excel 数据文件放入 `原始文件` 目录,文件名需包含日期(如 `2025年11月22日.xlsx`)

### 3. 启动应用
```bash
streamlit run app.py
```

或使用启动脚本:
```bash
./run_dashboard.sh
```

应用将在浏览器中自动打开,默认地址: http://localhost:8501

## ☁️ 云端部署

### 使用 Streamlit Cloud(推荐)

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **部署到 Streamlit Cloud**
   - 访问 https://streamlit.io/cloud
   - 使用 GitHub 账号登录
   - 点击 "New app"
   - 选择您的仓库、分支和主文件 (`app.py`)
   - 点击 "Deploy"

3. **访问应用**
   - 部署完成后会生成公开访问链接
   - 例如: `https://your-app.streamlit.app`

### 其他部署选项

- **Heroku**: 适合需要更多自定义配置的场景
- **Railway**: 简单快速的部署平台
- **自建服务器**: 使用 Docker 容器化部署

## 📁 项目结构

```
房产成交数据看板/
├── app.py                 # 主应用文件
├── data_processor.py      # 数据处理模块
├── requirements.txt       # Python 依赖
├── .gitignore            # Git 忽略配置
├── 原始文件/              # Excel 数据文件目录
└── README.md             # 项目说明
```

## 📝 数据格式要求

Excel 文件应包含以下列:
- 区域
- 小区名
- 楼层
- 面积
- 单价
- 总价

文件名需包含日期信息,例如: `2025年11月22日.xlsx`

## 🛠️ 技术栈

- **Streamlit**: Web 应用框架
- **Pandas**: 数据处理
- **Plotly**: 交互式图表
- **OpenPyXL**: Excel 文件读取

## 📄 许可证

MIT License

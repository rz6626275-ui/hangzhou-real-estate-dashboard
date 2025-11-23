#!/bin/bash

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "正在检查依赖环境..."

# 检查并安装依赖
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "正在安装 streamlit..."
    pip3 install streamlit
fi

if ! python3 -c "import pandas" &> /dev/null; then
    echo "正在安装 pandas..."
    pip3 install pandas
fi

if ! python3 -c "import plotly" &> /dev/null; then
    echo "正在安装 plotly..."
    pip3 install plotly
fi

if ! python3 -c "import openpyxl" &> /dev/null; then
    echo "正在安装 openpyxl..."
    pip3 install openpyxl
fi

echo "正在启动房产数据看板..."
echo "请在浏览器中访问显示的地址 (通常是 http://localhost:8501)"

# 启动 Streamlit
python3 -m streamlit run app.py

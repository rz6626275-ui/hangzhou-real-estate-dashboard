#!/bin/bash

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "   房产数据看板 - Debug 模式"
echo "=================================================="
echo "正在启动..."
echo "如果遇到错误，请截图此窗口发送给开发者。"
echo "--------------------------------------------------"

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

# 启动 Streamlit
python3 -m streamlit run app.py

echo "--------------------------------------------------"
echo "程序已停止。"
echo "按任意键退出..."
read -n 1 -s

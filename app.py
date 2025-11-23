import streamlit as st
import pandas as pd
import plotly.express as px
import data_processor
import os

# 设置页面配置
st.set_page_config(
    page_title="房产成交数据看板", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="auto",  # 移动端自动收起,桌面端自动展开
    menu_items={
        'About': "# 房产成交数据看板\n实时整合每日网签数据,助您洞察市场动态。"
    }
)

# --- 🌓 深色模式逻辑 ---
st.sidebar.header("🎨 外观设置")
dark_mode = st.sidebar.toggle("🌙 深色模式", value=True)

# 定义主题配色
theme = {
    "light": {
        "bg_color": "#FFFFFF",
        "sidebar_bg": "#F8FAFC",
        "text_color": "#1E293B",
        "subtext_color": "#64748B",
        "card_bg": "#FFFFFF",
        "card_border": "#E2E8F0",
        "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        "plotly_template": "plotly_white",
        "chart_bg": "rgba(255,255,255,0)"
    },
    "dark": {
        "bg_color": "#0E1117",
        "sidebar_bg": "#262730",
        "text_color": "#FAFAFA",
        "subtext_color": "#A0A0A0",
        "card_bg": "#1E1E1E",
        "card_border": "#414141",
        "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.3)",
        "plotly_template": "plotly_dark",
        "chart_bg": "rgba(0,0,0,0)"
    }
}

current_theme = theme["dark"] if dark_mode else theme["light"]

# --- 🎨 动态 CSS 注入 ---
st.markdown(f"""
<style>
    /* 全局字体 */
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }}
    
    /* 全局背景和文字 */
    .stApp {{
        background-color: {current_theme['bg_color']};
        color: {current_theme['text_color']};
    }}
    
    /* 标题样式 */
    h1, h2, h3 {{
        color: {current_theme['text_color']} !important;
        font-weight: 700;
    }}
    p {{
        color: {current_theme['text_color']};
    }}
    
    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {{
        background-color: {current_theme['sidebar_bg']};
        border-right: 1px solid {current_theme['card_border']};
    }}
    
    /* 指标卡片样式 */
    div[data-testid="stMetric"] {{
        background-color: {current_theme['card_bg']};
        border: 1px solid {current_theme['card_border']};
        border-radius: 12px;
        padding: 16px;
        box-shadow: {current_theme['shadow']};
        transition: transform 0.2s;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {current_theme['subtext_color']};
        font-size: 0.875rem;
    }}
    div[data-testid="stMetricValue"] {{
        color: {current_theme['text_color']};
        font-weight: 700;
    }}
    
    /* 图表容器样式 */
    .stPlotlyChart {{
        background-color: {current_theme['card_bg']};
        border-radius: 12px;
        box-shadow: {current_theme['shadow']};
        padding: 10px;
        border: 1px solid {current_theme['card_border']};
    }}
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    
    
    /* ========== 📱 移动端优化 ========== */
    @media (max-width: 768px) {{
        /* 主标题 */
        h1 {{
            font-size: 1.75rem !important;
            margin-bottom: 0.5rem !important;
        }}
        
        /* 副标题 */
        h2, h3 {{
            font-size: 1.25rem !important;
        }}
        
        /* 描述文字 */
        p {{
            font-size: 0.875rem !important;
        }}
        
        /* 指标卡片 - 移动端更紧凑 */
        div[data-testid="stMetric"] {{
            padding: 12px !important;
            margin-bottom: 8px !important;
        }}
        
        div[data-testid="stMetricLabel"] {{
            font-size: 0.75rem !important;
        }}
        
        div[data-testid="stMetricValue"] {{
            font-size: 1.25rem !important;
        }}
        
        /* 图表容器 - 移动端优化 */
        .stPlotlyChart {{
            padding: 5px !important;
            margin-bottom: 1rem !important;
        }}
        
        /* 侧边栏 - 移动端全宽 */
        section[data-testid="stSidebar"] {{
            width: 100% !important;
        }}
        
        /* 输入框和滑块 - 增大触摸区域 */
        input, select, button {{
            min-height: 44px !important;
            font-size: 16px !important;
        }}
        
        /* 滑块 */
        .stSlider {{
            padding: 10px 0 !important;
        }}
        
        /* 数据表 - 横向滚动 */
        div[data-testid="stDataFrame"] {{
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }}
        
        /* 按钮 - 增大触摸区域 */
        .stButton > button {{
            width: 100% !important;
            min-height: 44px !important;
            font-size: 16px !important;
        }}
        
        /* 多选框 */
        .stMultiSelect {{
            font-size: 14px !important;
        }}
        
        /* 日期选择器 */
        .stDateInput {{
            font-size: 14px !important;
        }}
    }}
    
    /* 小屏手机优化 (< 480px) */
    @media (max-width: 480px) {{
        h1 {{
            font-size: 1.5rem !important;
        }}
        
        h2, h3 {{
            font-size: 1.1rem !important;
        }}
        
        div[data-testid="stMetric"] {{
            padding: 10px !important;
        }}
        
        div[data-testid="stMetricValue"] {{
            font-size: 1.1rem !important;
        }}
    }}
    
    /* 触摸设备优化 */
    @media (hover: none) and (pointer: coarse) {{
        /* 移除悬停效果 */
        div[data-testid="stMetric"]:hover {{
            transform: none !important;
        }}
        
        /* 增大可点击区域 */
        button, a, input, select {{
            min-height: 44px !important;
            min-width: 44px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# 标题
st.title("🏠 房产成交数据看板")
st.markdown(f"<p style='color: {current_theme['subtext_color']}; margin-bottom: 20px;'>实时整合每日网签数据,助您洞察市场动态。</p>", unsafe_allow_html=True)

# 加载数据
@st.cache_data(ttl=60)
def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '原始文件')
    return data_processor.load_data(data_dir)

with st.spinner('正在读取并整合数据...'):
    df = get_data()

if df.empty:
    st.warning("当前目录下未找到有效的 Excel 数据文件,请确保文件名包含日期(如 '2025年11月22日')。")
    st.stop()

# --- 主内容区筛选面板 (作为侧边栏的替代) ---
with st.expander("🔍 **筛选与搜索**", expanded=True):
    st.markdown("### 数据筛选")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        # 模糊搜索
        search_term_main = st.text_input("🔎 搜索小区名", placeholder="输入关键词,如 '绿城'", key="search_main")
        
        # 日期筛选
        min_date = df['日期'].min().date()
        max_date = df['日期'].max().date()
        date_range_main = st.date_input(
            "📅 日期范围",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_main"
        )
        
        # 区域筛选
        all_regions = df['区域'].unique().tolist()
        selected_regions_main = st.multiselect(
            "📍 选择区域",
            options=all_regions,
            default=all_regions,
            key="region_main"
        )
    
    with col_f2:
        # 总价筛选
        min_price = int(df['总价'].min()) if not df['总价'].isna().all() else 0
        max_price = int(df['总价'].max()) if not df['总价'].isna().all() else 1000
        price_range_main = st.slider(
            "💰 总价范围 (万)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            key="price_main"
        )
        
        # 面积筛选
        min_area = int(df['面积'].min()) if not df['面积'].isna().all() else 0
        max_area = int(df['面积'].max()) if not df['面积'].isna().all() else 200
        area_range_main = st.slider(
            "📐 面积范围 (㎡)",
            min_value=min_area,
            max_value=max_area,
            value=(min_area, max_area),
            key="area_main"
        )
    
    # 使用主内容区的筛选值
    search_term = search_term_main
    date_range = date_range_main
    selected_regions = selected_regions_main
    price_range = price_range_main
    area_range = area_range_main

# --- 侧边栏筛选 ---
st.sidebar.header("🔍 筛选与搜索")

# 0. 模糊搜索
search_term_sidebar = st.sidebar.text_input("搜索小区名", placeholder="输入关键词,如 '绿城'", key="search_sidebar")

st.sidebar.markdown("---")

# 1. 日期筛选
date_range_sidebar = st.sidebar.date_input(
    "📅 日期范围",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_sidebar"
)

# 2. 区域筛选
selected_regions_sidebar = st.sidebar.multiselect(
    "📍 选择区域",
    options=all_regions,
    default=all_regions,
    key="region_sidebar"
)

# 3. 总价筛选
price_range_sidebar = st.sidebar.slider(
    "💰 总价范围 (万)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    key="price_sidebar"
)

# 4. 面积筛选
area_range_sidebar = st.sidebar.slider(
    "📐 面积范围 (㎡)",
    min_value=min_area,
    max_value=max_area,
    value=(min_area, max_area),
    key="area_sidebar"
)

# --- 数据过滤 ---
# 组合主面板和侧边栏的筛选条件 (取交集)
# 只有当用户修改了默认值时,筛选条件才会生效

mask = (
    # 日期筛选 (主面板 & 侧边栏)
    (df['日期'].dt.date >= date_range_main[0]) & (df['日期'].dt.date <= date_range_main[1]) &
    (df['日期'].dt.date >= date_range_sidebar[0]) & (df['日期'].dt.date <= date_range_sidebar[1]) &
    
    # 区域筛选 (主面板 & 侧边栏)
    (df['区域'].isin(selected_regions_main)) &
    (df['区域'].isin(selected_regions_sidebar)) &
    
    # 总价筛选 (主面板 & 侧边栏)
    (df['总价'] >= price_range_main[0]) & (df['总价'] <= price_range_main[1]) &
    (df['总价'] >= price_range_sidebar[0]) & (df['总价'] <= price_range_sidebar[1]) &
    
    # 面积筛选 (主面板 & 侧边栏)
    (df['面积'] >= area_range_main[0]) & (df['面积'] <= area_range_main[1]) &
    (df['面积'] >= area_range_sidebar[0]) & (df['面积'] <= area_range_sidebar[1])
)

# 应用模糊搜索 (主面板 OR 侧边栏)
if search_term_main:
    mask = mask & (df['小区名'].str.contains(search_term_main, case=False, na=False))
if search_term_sidebar:
    mask = mask & (df['小区名'].str.contains(search_term_sidebar, case=False, na=False))

# 应用模糊搜索 (已在上方处理)
# if search_term:
#     mask = mask & (df['小区名'].str.contains(search_term, case=False, na=False))

filtered_df = df[mask]

# --- 关键指标 (KPI) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏠 成交套数", f"{len(filtered_df)}", delta="当前筛选范围")
avg_price = filtered_df['单价'].mean() if not filtered_df.empty else 0
col2.metric("🏷️ 平均单价", f"{avg_price:.2f} 万/㎡")
avg_total = filtered_df['总价'].mean() if not filtered_df.empty else 0
col3.metric("💰 平均总价", f"{avg_total:.2f} 万")
avg_area = filtered_df['面积'].mean() if not filtered_df.empty else 0
col4.metric("📐 平均面积", f"{avg_area:.2f} ㎡")

st.markdown("---")

# --- 图表分析 ---
# 定义配色
colors = px.colors.qualitative.Prism

# 响应式列布局 - 移动端单列,桌面端双列
col_chart1, col_chart2 = st.columns([1, 1], gap="medium")

with col_chart1:
    st.subheader("📈 每日成交量趋势")
    if not filtered_df.empty:
        daily_counts = filtered_df.groupby('日期').size().reset_index(name='成交量')
        fig_trend = px.bar(
            daily_counts, 
            x='日期', 
            y='成交量',
            template=current_theme['plotly_template'],
            color_discrete_sequence=["#3B82F6"] # Blue
        )
        fig_trend.update_layout(
            plot_bgcolor=current_theme['chart_bg'], 
            paper_bgcolor=current_theme['chart_bg'],
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor='#333' if dark_mode else '#F1F5F9', tickfont=dict(size=10)),
            margin=dict(l=40, r=20, t=40, b=40),
            font=dict(size=12)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("暂无数据")

with col_chart2:
    st.subheader("📊 各区域成交占比")
    if not filtered_df.empty:
        region_counts = filtered_df['区域'].value_counts().reset_index()
        region_counts.columns = ['区域', '成交量']
        fig_pie = px.pie(
            region_counts, 
            values='成交量', 
            names='区域', 
            hole=0.6, # Donut chart
            template=current_theme['plotly_template'],
            color_discrete_sequence=colors
        )
        fig_pie.update_layout(
            plot_bgcolor=current_theme['chart_bg'], 
            paper_bgcolor=current_theme['chart_bg'],
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=12),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("暂无数据")

# --- 新增：单价分布图 ---
st.subheader("🏷️ 单价分布 (万/㎡)")
if not filtered_df.empty:
    # 填充单价空值
    plot_df = filtered_df.copy()
    plot_df['单价'] = plot_df['单价'].fillna(0)
    
    # 计算平均单价
    avg_unit_price = plot_df['单价'].mean()
    
    fig_strip = px.strip(
        plot_df,
        x="单价",
        y="区域",
        color="区域",
        hover_data=['小区名', '总价', '面积', '日期'],
        template=current_theme['plotly_template'],
        color_discrete_sequence=colors,
    )
    
    # 添加平均线
    fig_strip.add_vline(
        x=avg_unit_price, 
        line_width=2, 
        line_dash="dash", 
        line_color="#FF4B4B",
        annotation_text=f"平均: {avg_unit_price:.2f}", 
        annotation_position="top right"
    )
    
    fig_strip.update_layout(
        plot_bgcolor=current_theme['chart_bg'], 
        paper_bgcolor=current_theme['chart_bg'],
        xaxis=dict(showgrid=True, gridcolor='#333' if dark_mode else '#F1F5F9', tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor='#333' if dark_mode else '#F1F5F9', tickfont=dict(size=10)),
        margin=dict(l=80, r=20, t=40, b=40),
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_strip, use_container_width=True)
else:
    st.info("暂无数据")



# --- 明细数据表 ---
st.subheader("📋 成交明细表")
st.dataframe(
    filtered_df[['日期', '区域', '小区名', '楼层', '面积', '单价', '总价']].sort_values('日期', ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "日期": st.column_config.DateColumn("成交日期", format="YYYY-MM-DD"),
        "单价": st.column_config.NumberColumn("单价 (万/㎡)", format="%.2f"),
        "总价": st.column_config.NumberColumn("总价 (万)", format="%.2f"),
        "面积": st.column_config.NumberColumn("面积 (㎡)", format="%.2f"),
    }
)

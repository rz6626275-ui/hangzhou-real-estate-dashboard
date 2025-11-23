import pandas as pd
import os
import re

def extract_date_from_filename(filename):
    """
    从文件名中提取日期。
    支持格式：
    - 2025年11月22日
    - 2025年10月26、27日 (提取第一个日期)
    """
    # 优先匹配标准格式
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})[日、]', filename)
    if match:
        return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
    return None

def load_data(directory):
    """
    读取指定目录下的所有 Excel 文件并合并。
    """
    all_data = []
    files = [f for f in os.listdir(directory) if f.endswith('.xlsx') and not f.startswith('~$')]
    
    print(f"Found {len(files)} Excel files in {directory}")

    for file in files:
        file_path = os.path.join(directory, file)
        try:
            # 读取 Excel，假设第二行（索引1）是表头
            df = pd.read_excel(file_path, header=1)
            
            # 提取日期
            date_str = extract_date_from_filename(file)
            if date_str:
                df['日期'] = pd.to_datetime(date_str)
            else:
                # 如果无法提取日期，使用文件修改时间
                df['日期'] = pd.to_datetime(os.path.getmtime(file_path), unit='s')
            
            # 统一将日期归一化为 00:00:00 (去除时间部分)
            df['日期'] = df['日期'].dt.normalize()
            
            # 数据清洗
            if '小区' in df.columns:
                # 拆分 区域/小区名
                # 假设格式为 "区域/小区名"，如果只有小区名则区域为空
                split_data = df['小区'].astype(str).str.split('/', n=1, expand=True)
                if split_data.shape[1] == 2:
                    df['区域'] = split_data[0]
                    df['小区名'] = split_data[1]
                else:
                    df['区域'] = '未知'
                    df['小区名'] = df['小区']
            
            # 转换数值列
            numeric_cols = ['面积', '单价', '总价']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # --- 修正单价 ---
            # 用户要求：单价 = 总价 / 面积
            # 避免除以零错误
            if '总价' in df.columns and '面积' in df.columns:
                df['单价'] = df.apply(
                    lambda row: row['总价'] / row['面积'] if row['面积'] > 0 and pd.notnull(row['面积']) and pd.notnull(row['总价']) else 0, 
                    axis=1
                ).round(2)

            # 确保楼层列为字符串，避免 pyarrow 序列化错误
            if '楼层' in df.columns:
                df['楼层'] = df['楼层'].astype(str)
            
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not all_data:
        return pd.DataFrame()

    final_df = pd.concat(all_data, ignore_index=True)
    
    # --- 区域清洗逻辑 ---
    VALID_REGIONS = ["上城", "拱墅", "西湖", "滨江", "萧山", "余杭", "临平", "钱塘"]
    
    def clean_region(val):
        if pd.isna(val):
            return None
        val = str(val).strip()
        # 去除空格和换行
        val = re.sub(r'\s+', '', val)
        
        # 常见 OCR 错误修正
        if '饯塘' in val: return '钱塘'
        if '滨汇' in val: return '滨江'
        if 'I:城' in val or ':城' in val: return '上城'
        
        # 包含匹配
        for region in VALID_REGIONS:
            if region in val:
                return region
        return None

    if '区域' in final_df.columns:
        final_df['区域'] = final_df['区域'].apply(clean_region)
        # 只保留有效区域的数据 (过滤掉表头行和无法识别的行)
        final_df = final_df[final_df['区域'].isin(VALID_REGIONS)]

    return final_df

if __name__ == "__main__":
    # 测试代码
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = load_data(current_dir)
    print(df.head())
    print(df.info())

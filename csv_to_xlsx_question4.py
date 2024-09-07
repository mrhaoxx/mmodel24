import pandas as pd
import sys

# 读取 CSV 文件
csv_file_loc = sys.argv[1]
csv_file_spd = sys.argv[2]

def get_spd_row_name(i):
    if i == 0:
        return "龙头 (m/s)"
    elif i == 223:
        return "龙尾（后）(m/s)"
    elif i == 222:
        return "龙尾 (m/s)"
    else:
        return f"第 {i} 节龙身 (m/s)"
    
def get_loc_row_name(ri):
    i = ri // 2
    t = "x" if ri % 2 == 0 else "y"
    if i == 0:
        return f"龙头{t}(m)"
    elif i == 222:
        return f"龙尾{t}(m)"
    elif i == 223:
        return f"龙尾（后）{t}(m)"
    else:
        return f"第 {i} 节龙身{t}(m)"

df_loc = pd.read_csv(csv_file_loc, header=None)
df_transposed_loc = df_loc.transpose()

df_transposed_loc.columns = [f"{i - 100}s" for i in range(df_transposed_loc.shape[1])]

df_transposed_loc.index = [get_loc_row_name(i) for i in range(df_transposed_loc.shape[0])]

df_spd = pd.read_csv(csv_file_spd, header=None)
df_transposed_spd = df_spd.transpose()

df_transposed_spd.columns = [f"{i}s" for i in range(df_transposed_spd.shape[1])]
df_transposed_spd.index = [get_spd_row_name(i) for i in range(df_transposed_spd.shape[0])]



xlsx_file = f'result4.xlsx'

with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
    df_transposed_loc.head(448).to_excel(writer, sheet_name='位置')
    df_transposed_spd.head(224).to_excel(writer, sheet_name='速度')

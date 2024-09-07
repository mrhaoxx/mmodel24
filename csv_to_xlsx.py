import pandas as pd
import sys

# 读取 CSV 文件
csv_file = sys.argv[1]

Type = "spd" if "spd" in csv_file else "loc" if "loc" in csv_file else "unknow"

if Type == "unknow":
    print("未知文件类型")
    exit(1)

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

df = pd.read_csv(csv_file, header=None)
df_transposed = df.transpose()

df_transposed.columns = [f"{i}s" for i in range(df_transposed.shape[1])]

if Type == "spd":
    df_transposed.index = [get_spd_row_name(i) for i in range(df_transposed.shape[0])]
elif Type == "loc":
    df_transposed.index = [get_loc_row_name(i) for i in range(df_transposed.shape[0])]

xlsx_file = f'{sys.argv[1]}.xlsx'

df_limited = df_transposed.head(224 if Type == "spd" else 448)

df_limited.to_excel(xlsx_file)

print(f"已将 {csv_file} 转置并转换为 {xlsx_file}")
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

df_transposed_loc.columns = [f"{i}s" for i in range(df_transposed_loc.shape[1])]

df_transposed_loc.index = [get_loc_row_name(i) for i in range(df_transposed_loc.shape[0])]

df_spd = pd.read_csv(csv_file_spd, header=None)
df_transposed_spd = df_spd.transpose()

df_transposed_spd.columns = [f"{i}s" for i in range(df_transposed_spd.shape[1])]
df_transposed_spd.index = [get_spd_row_name(i) for i in range(df_transposed_spd.shape[0])]



selected_columns = df_transposed_loc.iloc[:, [0, 60, 120, 180, 240, 300]]
selected_columns_spd = df_transposed_spd.iloc[:, [0, 60, 120, 180, 240, 300]]

selection = [0,1, 51, 101, 151, 201, 223]

selected_rows = selected_columns.iloc[[(2 * selection[i//2] if i % 2 == 0 else 2 * selection[i//2] + 1)  for i in range(len(selection) * 2)]]
selected_rows_spd = selected_columns_spd.iloc[selection]

selected_rows.to_csv('result1_latex_loc.csv')
selected_rows_spd.to_csv('result1_latex_spd.csv')
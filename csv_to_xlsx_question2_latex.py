import pandas as pd
import sys

# 读取 CSV 文件
csv_file_loc = sys.argv[1]
csv_file_spd = sys.argv[2]

def get_row_name(i):
    if i == 0:
        return "龙头"
    elif i == 223:
        return "龙尾（后）"
    elif i == 222:
        return "龙尾"
    else:
        return f"第 {i} 节龙身"


df_loc = pd.read_csv(csv_file_loc, header=None)
df_transposed_loc = df_loc.transpose()

df_transposed_loc.columns = [f"{i}s" for i in range(df_transposed_loc.shape[1])]

# df_transposed_loc.index = [get_loc_row_name(i) for i in range(df_transposed_loc.shape[0])]
df_even = df_transposed_loc[::2].reset_index(drop=True)  # 偶数行数据 (0, 2, 4,...)
df_odd = df_transposed_loc[1::2].reset_index(drop=True)  # 奇数行数据 (1, 3, 5,...)
# df_transposed_loc.index = [get_loc_row_name(i) for i in range(df_transposed_loc.shape[0])]


df_spd = pd.read_csv(csv_file_spd, header=None)
df_transposed_spd = df_spd.transpose()

df_cb = pd.concat([df_even, df_odd, df_transposed_spd], axis=1)


df_cb.columns = ["横坐标x (m)","纵坐标y (m)","速度 (m/s)"]
df_cb.index = [get_row_name(i) for i in range(df_transposed_spd.shape[0])]




selection = [0,1, 51, 101, 151, 201, 223]

selected_rows_spd = df_cb.iloc[selection]

selected_rows_spd.to_csv('result2_latex.csv')

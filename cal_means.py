import pandas as pd
import os

root_path = "F:/Programming/Dataset/StockInformation/"
file_path = root_path + "sh1_each_stock_data-bak/"
result_path = root_path + "sh1_each_stock_data/"
if not os.path.exists(result_path):
    os.mkdir(result_path)

files = os.listdir(file_path)
for f in files:
    csv_data = pd.read_csv(file_path + f)
    csv_data.set_index("SecurityID", drop=False, inplace=True)
    csv_data['Mean5'] = csv_data.LastPx.rolling(5).mean()
    csv_data['Mean10'] = csv_data.LastPx.rolling(10).mean()
    csv_data['Mean20'] = csv_data.LastPx.rolling(20).mean()
    csv_data['Mean30'] = csv_data.LastPx.rolling(30).mean()

    csv_data.to_csv(result_path + f, index=False, header=True)

import pandas as pd


user_info=pd.read_csv('../input/UserInfo.tsv',delimiter='\t',encoding='utf-8')
print(list(user_info.columns.values)) #file header

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# arima 时序模型
import pandas as pd

forecastnum=5
filepath=r"C:\E\Information\DATA Analysis\FlatFile\FileList\design.csv"
df=pd.read_csv(filepath,encoding="GBK",low_memory=False,index_col=0)

# 去除文件类型为.db的数据
data=df[df['文件类型']!='.db']
#获取重复文件的占比
df1=df[(df.duplicated(['文件名'])==True)&(df.duplicated(['文件大小'])==True)]
dup_data=format((df1.文件大小.sum())/(df.文件大小.sum()),'0.2%')
print('重复文件大小占比：' ,dup_data)
# 提取创建时间和文件大小列
data=data[['创建日期','文件大小']]
#改变创建日期列类型为datatime
data['创建日期']=pd.to_datetime(data.创建日期)
new_data=data.set_index('创建日期')
#new_data=new_data['2010':'2017']
result=new_data.resample('A').sum()
result=result.dropna()









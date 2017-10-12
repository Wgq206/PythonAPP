# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# arima 时序模型
import pandas as pd

forecastnum=5
filepath="C:\E\Information\DATA Analysis\FlatFile\FileList\seat.csv"
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
new_data=new_data['2010':'2017']
result=new_data.resample('BM').sum()
result=result.dropna()

#根据zscore滤除异常值

#def a3(dataframe, threshold=3.5):
#  dd = dataframe['文件大小']
#  MAD = (dd - dd.median()).abs().median()
#  zscore = ((dd - dd.median())* 0.6475 /MAD).abs()
#  dataframe['isAnomaly'] = zscore > threshold
#  return dataframe
#a=a3(result,threshold=3.5)
#b=a
#result=b.drop(['isAnomaly'],axis=1)
#时序图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
result.plot()
plt.show()

#自相关图

from statsmodels.graphics.tsaplots import plot_acf
plot_acf(result).show()

#平稳性检测

from statsmodels.tsa.stattools import adfuller as ADF
diff=0
adf=ADF(result['文件大小'])
while adf[1]>=0.05: #adf[1]为p值，p值小于0.05认为是平稳的
    diff=diff+1
    adf=ADF(result['文件大小'].diff(diff).dropna())
    
print('原始数据经过%s阶差分后归于平稳，p值为%s' %(diff,adf[1]))
#返回值依次为adf\pvalue\usedlag\nobs\critical\values\icbest\regresults\resstore

#差分后的结果  
D_data=result.diff().dropna()
D_data.columns=['文件大小差分']
D_data.plot()
plt.show()
plot_acf(D_data).show()
print('差分序列的ADF检验结果为：',ADF(D_data['文件大小差分'])) #平稳性检测

#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox
[[lb],[p]]=acorr_ljungbox(result['文件大小'],lags=1)
if p<0.05:
    print('原始序列为非白噪声序列，对应的p值为： %s' %p)
else:
    print('原始序列为白噪声序列，对应的p值为： %s' %p)

[[lb],[p]]=acorr_ljungbox(result['文件大小'].diff().dropna(),lags=1)
if p<0.05:
    print('一阶差分序列为非白噪声序列，对应的p值为： %s' %p)
else:
    print('一阶差分序列为白噪声序列，对应的p值为： %s' %p)
#print('差分序列的白噪声检验结果为：',acorr_ljungbox(D_data,lags=1))#返回统计量和p值

#定阶

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import AR
#pmax=int(len(D_data)/10) #一般阶数不超过10
#qmax=int(len(D_data)/10) #一般阶数不超过10
#bic_matrix=[] #bic矩阵
#for p in range(pmax+1):
#    tmp=[]
#    for q in range(qmax+1):
#        try: #存在部分报错，所以用try来跳过报错
#            tmp.append(ARMA(result,(p,0)).fit().bic)
##            tmp.append(ARIMA(result,(p,1,q)).fit().bic)
#        except:
#            tmp.append(None)
#    bic_matrix.append(tmp)
#bic_matrix=pd.DataFrame(bic_matrix)
#p=bic_matrix.stack().idxmin()#先用stack展平，然后用idxmin找到最小值的位置
##p,q=bic_matrix.stack().idxmin()#先用stack展平，然后用idxmin找到最小值的位置
#print('BIC最小的p值和q值为：%s、%s' %(p,q))
#print('BIC最小的p值和q值为：%s、%s' %(p,q))
ts=result['文件大小']
def adf_test(ts):
    adftest = ADF(ts, autolag='AIC')
    adf_res = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])

    for key, value in adftest[4].items():
        adf_res['Critical Value (%s)' % key] = value
    return adf_res
def draw_ar(ts, w):
    arma = ARMA(ts, order=(w,0)).fit(disp=-1)
    ts_predict = arma.predict()
    pred_error = (xdata_pred-xdata).dropna()  #计算残差
    pred_error=pred_error[pred_error>0]
    lb,p =acorr_ljungbox(pred_error,lags=lagnum)
    h=(p<0.05).sum() #p值小于0.05，认为是非白噪声
    if h>0:
        print('模型ARIMA(0,1,1)不符合白噪声检验')
    else:
        print('模型ARIMA(0,1,1)符合白噪声检验')

    plt.clf()
    plt.plot(ts_predict, label="PDT")
    plt.plot(ts, label = "ORG")
    plt.legend(loc="best")
    plt.title("AR Test %s" % w)
#    plt.savefig("./PDF/test_ar_"+ str(w) +".pdf", format='pdf'

#模型检验
lagnum=12 #残差延迟个数
xdata=result['文件大小']
arima=ARMA(xdata,(1,0).fit() #建立训练模型
#arima=ARIMA(xdata,(0,1,1)).fit() #建立训练模型
xdata_pred = arima.predict() #预测
pred_error = (xdata_pred-xdata).dropna()  #计算残差
pred_error=pred_error[pred_error>0]
lb,p =acorr_ljungbox(pred_error,lags=lagnum)
h=(p<0.05).sum() #p值小于0.05，认为是非白噪声
if h>0:
    print('模型ARIMA(0,1,1)不符合白噪声检验')
else:
    print('模型ARIMA(0,1,1)符合白噪声检验')
#model=ARIMA(result,(p,1,q)).fit()  #建立ARIMA(0,1,1)模型
#print(model.summary2())
#print(model.forecast(5))








# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 14:03:48 2017

@author: awangg2
"""

import os
import time
import win32security
import pandas as pd

filePath="\\\\a-cgqsu04\\PC-Programs\\Tracking_Reports"

column=[u'文件名',u'文件路径',u'文件类型',u'创建者',u'文件大小',u'创建日期',u'访问日期',u'修改日期']
data=pd.DataFrame(columns=column)

'''for循环os.walk获取文件目录下所有文件的所在路径，文件夹所有子目录的名字，文件名称
返回的是三个touple
'''


fileList=[]
listName=[]
listpath=[]
listtype=[]
listuser=[]
listsize=[]
listctime=[]
listatime=[]
listmtime=[]
#listerror=[]
for parent,dirnames,filenames in os.walk(filePath):
#    for dirname in dirnames: 
##        list.append(dirname)
    for filename in filenames : 
    #输出文件路径信息 
        currentPath = os.path.join(parent,filename) 
#            st = os.stat(currentPath)
    
        try:
            f = win32security.GetFileSecurity(currentPath, win32security.OWNER_SECURITY_INFORMATION)
            (username, domain, sid_name_use) =  win32security.LookupAccountSid(None, f.GetSecurityDescriptorOwner())
            filelocat,filetype=os.path.splitext(currentPath) 
            filesize = os.path.getsize(currentPath)/1024/1024 
            filecreatetime=time.strftime('%Y%m%d %H:%M:%S',time.localtime(os.path.getctime(currentPath)))
            filevsitetime=time.strftime('%Y%m%d %H:%M:%S',time.localtime(os.path.getatime(currentPath)))
            filemondifytime=time.strftime('%Y%m%d %H:%M:%S',time.localtime(os.path.getmtime(currentPath)))
        except (OSError,ValueError):
            pass
#            listerror.append(filename)
 
#                print(filename)
 
        
        fileList.append(filename)
        listName.append(filename)
        listpath.append(parent)
        listtype.append(filetype)
        listuser.append(username)
        listsize.append(filesize)
        listctime.append(filecreatetime)
        listatime.append(filevsitetime)
        listmtime.append(filemondifytime)
# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 13:28
# @Author  : ha1g0
# @Site    : http://whc.dropsec.xyz
# @File    : spider.py.py

import os
import re
import time

import db
import requests
from pymongo import MongoClient




class read_file():
    '''
    :param filename:主域名文件
    :param schools: 学校[{'school':'中原工学院','top_domain':'zzti.edu.cn','sec_domain':[1,2,3]}]
    '''
    def __init__(self,filename,schools):
        self.filename=filename
        self.schools=schools

    def read(self):
        with open(self.filename) as f:
            count=0
            for line in f.readlines():
                information = {}
                top_domain,school_name=(line.strip('\n')).split('|')
                information["_id"]=count
                information['school']=school_name
                information['top_domain']=top_domain
                information['sec_domain']=[]
                self.schools.append(information)
                count+=1
        return


class craw_domains():
    '''
    :param: key:主域名
    :param: domains: 二级域名列表
    '''
    def __init__(self,key,domains):
        self.key=key
        self.domains=domains

    def craw(self,url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
        response = requests.get(url, headers=header)
        response_html = response.text
        response_html.replace('\xa0','')
        # 正则
        match = 'style="text-decoration:none;">(.*?)/'
        subdomains = re.findall(match, response_html)
        for i in subdomains:
            i.strip('&nbsp')
        return subdomains

    def craw_all(self):
        for i in range(10):
            url = "http://www.baidu.com/s?wd=site:" + str(self.key) + "&cl=3&pn=%s" % (i*10)
            subdomains=[]
            self.url=url
            subdomains = self.craw(url)
            self.domains.extend(subdomains)
            # set去重
            self.domains = list(set(self.domains))
        return self.domains




def main():
    filename =u'./主域名.txt'
    schools=[]
    read_file(filename,schools).read()
    con = db.db("test","test1")
    # print (schools)
    for school in schools:
        sec_domain=[]
        top_domain=school['top_domain']
        start =time.clock()
        craw=craw_domains(top_domain,sec_domain)
        sec_domain=craw.craw_all()
        end =time.clock()
        print("%s  爬取二级域名耗费时间为%f秒"%(school['school'],(end - start)))
        school['sec_domain'].extend(sec_domain)
        try:
            con.insert(school)
        except:
            con.save(school)



if __name__ == '__main__':
    main()
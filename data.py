# -*- coding: utf-8 -*-
# @Date    : 2017-12-27 10:13:27
# @Author  : ha1g0
# @Email   : 1321375781@qq.com


'''
对爬取到的数据进行处理
二级域名跟ip的对应关系
'''

import os
import socket

import db


class ipConvert:
    '''
    单个域名解析成IP
    '''

    def __init__(self, domain):
        self.domain = domain
        self.ip = ''

    def gethostbyname(self):
        # 从域名解析到ip
        try:
            self.ip = socket.gethostbyname(self.domain)
        except:
            print(str(self.domain) + "has no ip")
        # finally:
        #     return self.ip

    def relation(self):
        self.gethostbyname()
        return {self.domain: self.ip}


class dictChange:
    '''
    把二级域名的数据从 [{'mooc1.zut.edu.cn': '202.196.32.91'}, {'fgcgjs.zut.edu.cn': '202.196.32.45'}]变成｛'202.196.32.91': ['study.zut.edu.cn', 'mooc.zut.edu.cn']｝
    '''

    def __init__(self, information):
        self.information = information
        self.result = []

    def induceDomain(self):
        tmp = {}
        for dir in self.information:
            ip = list(dir.values())[0]
            domain = list(dir.keys())
            if ip not in tmp:
                tmp[ip] = domain
            else:
                tmp[ip].extend(domain)
        # self.result.append(tmp)
        for item in tmp.items():
            tmp2 = {}
            tmp2[item[0]] = item[1]
            self.result.append(tmp2)
        return self.result


def main():
    test1 = db.selectDB("test", "test1")
    test2 = db.selectDB("test", "test2")
    information = []
    information = test1.find()  # 从数据库中查找所有的文档
    count = 0
    for item in information:

        sec_domains = []
        sec_domains = item[
            'sec_domain']  # ['www.cie.zut.edu.cn', 'zsc.zut.edu.cn' , 'fangzhi.zut.edu.cn', 'job.zut.edu.cn', 'oa.zut.edu.cn']
        school_name = item['school']
        domain_ip = []  # [{'www.cie.zut.edu.cn': '202.196.32.47'}, {'zsc.zut.edu.cn': '202.196.32.28'}]
        domain_ip_changed = []
        for i in sec_domains:
            dict = {}
            dict = ipConvert(i).relation()
            domain_ip.append(dict)

        domain_ip_changed = dictChange(domain_ip).induceDomain()
        print({"_id": count, "school": school_name, "ip_domain": domain_ip_changed})
        data = {"_id": count, "school": school_name, "ip_domain": domain_ip_changed}
        try:
            test2.insert(data)
        except:
            test2.save(data)
        count += 1
        # print(1)


if __name__ == '__main__':
    main()

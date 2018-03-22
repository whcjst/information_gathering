# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 9:40
# @Author  : ha1g0
# @Site    : http://whc.dropsec.xyz
# @File    : scan.py


'''
根据ip探测主机信息  操作系统和开放端口

'''

import queue
import threading
import nmap
import libnmap
import db


class scanthread(threading.Thread):

    def __init__(self,q,information):
        threading.Thread.__init__(self)
        self.q = q
        self.information = information

    def run(self):
        scan(self.q,self.information)


class hostScan:
    '''
    根据ip对主机进行 端口 和 os的探测
    '''
    def __init__(self,ip):
        self.ip = ip
        self.ports = []
        self.osname =''
        self.accuracy = ''

        self.nm = nmap.PortScanner()
        self.__ip_scan()

    def  __ip_scan(self):
        try:
            self.nm.scan(self.ip, arguments="-O")
            print("调用 %s " % (self.nm.command_line()))
        except nmap.PortScannerError:
            pass

    def ip_ports(self):
        try:
            self.ports = self.nm[self.ip].all_tcp()
            return self.ports
        except Exception as e:
            print("主机%s不存活 " % self.ip)
            pass

    def ip_os(self):
        try:
            self.osname = self.nm[self.ip]["osmatch"][0]['name']
            self.accuracy = self.nmp[self.ip]["osmatch"][0]["accuracy"]
            return self.osname
        except Exception as e :
            pass
        else:
            if self.osname == '':
                self.osname = self.accuracy

    def ip_info(self):
        self.ip_ports()
        self.ip_os()
        return self.ports,self.osname


def scan(q,information):
    tmp = {}
    queuelock.acquire()
    ip =q.get()
    queuelock.release()
    scan = hostScan(ip)
    ports, osname = scan.ip_info()
    tmp['ip'] = ip
    tmp['port'] = ports
    tmp['osname'] = osname
    information.append(tmp)



def main():
    test2 = db.selectDB("test","test2")
    test3 = db.selectDB("test","test3")
    information =[]
    information = test2.find()
    count = 0
    find = test3.find_one({"_id": count})

    for item in information:
        find = {}
        find= test3.find_one({"_id":count})
        if find ==None:
            ip_domain =item['ip_domain']
            school_name =item['school']
            ips =[]
            ipinformation =[]

            for i in ip_domain:
                ip =(list(i.keys())[0])
                ips.append(ip)


            global queuelock
            queuelock = threading.Lock()
            ipqueue = queue.Queue(len(ips))
            queuelock.acquire()
            for ip in ips:
                ipqueue.put(ip)
            queuelock.release()

            thread_count = len(ips)
            threads = []

            for i in range(thread_count):
                thread = scanthread( ipqueue,ipinformation)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            data = {'_id': count, 'school': school_name, 'host_info': ipinformation}
            try:
                test3.insert(data)
                print (("-------%s 插入数据成功-------")%school_name)
            except:
                test3.save(data)
                print(("-------%s 插入数据成功-------")%school_name)

        count+=1


if __name__ == '__main__':
    main()
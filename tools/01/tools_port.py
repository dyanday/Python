#-*- coding=utf-8 -*-
#@Time:2020/4/7 21:41
#@Author:大雁
#@File:tools_port.py
#@Software:PyCharm
# 端口扫描
import threading
import socket
lock=threading.Lock()
def get_ip_status(ip,port):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        server.connect((ip,port))
        print('{0} 端口{1} 开启'.format(ip, port))
    except Exception as err:
        # print('{0} 端口 {1} 关闭'.format(ip,port))
        pass

    finally:
        server.close()
if __name__ == '__main__':
    host=input("请输入ip地址:")
    p=int(input("请输入端口范围"))
    for port in range(20,p):
        t=threading.Thread(target=get_ip_status,args=(host,port))
        t.start()
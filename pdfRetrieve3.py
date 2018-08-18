# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from urllib import request, parse
import os
import json
import threading
import socket

#set the default timeout to 180s
socket.setdefaulttimeout(180)

ID_list = []
fail_list = []
suc_list = []
lock = threading.Lock()

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    :param blocknum: 已经下载的数据块
    :param blocksize: 数据块的大小
    :param totalsize: 远程文件的大小
    :return:
    '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print ('%.2f%%' % per)

def download_report(stock_id, local_path, report_year):
    #print('Connect to cninfo.com.cn...')
    print('Stock ID: %s' % stock_id)
    #print('Local Path: %s' % local_path)

    post_data = parse.urlencode([
        ('stock',stock_id),
        ('category','category_ndbg_szsh;'),
        ('pageNum', 1),
        ('pageSize', 15),
        ('column', 'szse_main'),
        ('tabName', 'fulltext')
    ])

    req = request.Request('http://www.cninfo.com.cn/cninfo-new/announcement/query')
    req.add_header('Referer', 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/showFulltext/' + stock_id)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
    req.add_header('Origin', 'http://www.cninfo.com.cn')

    try:
        rtn = request.urlopen(req, data = post_data.encode('utf-8'))
        receive_data = json.loads(rtn.read().decode('utf-8'))
    except Exception as e:
        print (e)
        print ('Cannot connect to cninfo.com.cn')
        lock.acquire()
        fail_list.append(stock_id)
        lock.release()
        return False    

    for item in receive_data['announcements']:
        if item['announcementTitle'].find('摘要') == -1 and item['announcementTitle'].find('已取消') == -1 and item['announcementTitle'].find('英文') == -1 and item['announcementTitle'].find(str(report_year)) != -1:
            print('%s_%s %s' % (stock_id, item['announcementTitle'], ' 下载中...'))
            filename = '%s_%s.%s' % (stock_id, item['announcementTitle'], item['adjunctUrl'].split('.')[1])
            if not os.path.exists(os.path.join(local_path, filename)):
                try:
                    request.urlretrieve('http://www.cninfo.com.cn/' + item['adjunctUrl'], os.path.join(local_path, filename))
                except Exception as e:
                    print ('%s_%s %s' % (stock_id, item['announcementTitle'], ' 下载失败'))
                    print(e)
                    lock.acquire()
                    fail_list.append(stock_id)
                    lock.release()
                    if os.path.exists(os.path.join(local_path, filename)):
                        os.remove(os.path.join(local_path, filename))
                    return False
            print('%s_%s %s' % (stock_id, item['announcementTitle'], ' 下载成功'))
            lock.acquire()
            suc_list.append(filename)
            lock.release()
    return True

def startdownload(local_path, report_year, poolsize=10):
    '''开始下载
    :param local_path: 下载至本地的路径
    :param report_year: 报告年份
    :param poolsize: 线程池大小
    '''

    length_ofIDlist = len(ID_list)
    
    print('Report Year: %s' % report_year)
    print('There are %d reports to be downloaded' % length_ofIDlist)
    for j in range(0, length_ofIDlist, poolsize):
        thread_pool = []
        for i in range(0, poolsize):
            if j+i >= length_ofIDlist:
                break
            stock_id = ID_list[i+j]
            thread_pool.append(threading.Thread(target=download_report,args=(stock_id,local_path,report_year,)))
        # if there is no more lines in the file, break out while
        if not any(thread_pool):
            break
        for job in thread_pool:
            job.start()
        for job in thread_pool:
            job.join()

def getrange(start_id, end_id):
    '''获取股票范围，存储到ID_list中
    :param start_id: 启始股票ID
    :param end_id: 结束股票ID
    '''
    
    f = open('./stock.txt', 'r', -1, 'utf-8')
    line = f.readline()
    stock_id = line.split('\t')[0]
    
    while int(stock_id) < int(start_id):
        stock_id = f.readline().split('\t')[0]
        
    while int(stock_id) <= int(end_id):
        ID_list.append(stock_id)
        stock_id = f.readline().split('\t')[0]
        
    f.close()
 
    
if __name__=='__main__':
    start_id    = input("Input start stock ID : ")
    end_id      = input("Input end stock ID   : ")
    report_year = input("Input report year    : ")
    local_path = './Report'+report_year

    if not os.path.exists(local_path):
        os.mkdir(local_path)

    getrange(start_id, end_id)

    repeat_num = 0
    while any(ID_list):
        startdownload(local_path, report_year)
        repeat_num += 1
        if repeat_num > 5:
            break
        if len(fail_list) > 10:
            ID_list = fail_list
            fail_list = []
        else:
            break

    fail_list.sort()
    fail_num = len(fail_list)
    suc_num = len(suc_list)
    print('%d successfully downloaded' % suc_num)
    print('%d falied' % fail_num)
    if fail_num != 0:
        print('They are the following')
        for x in fail_list:
            print(x)
   # if suc_num != 0:
   #     f = open('filelist_'+report_year+'.txt','w')
   #     for line in suc_list:
   #         f.write(line+'\n')
   #     f.close()

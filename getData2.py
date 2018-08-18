#coding:utf-8
import os
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
    
if __name__=='__main__':
    file_path = './'
    result_list = []

    keywords = ['开发支出','开发费用','开发投入','研发支出','研发费用','研发投入','研究支出','研究费用','研究投入']
    keyword_pattern = ''
    for word in keywords:
        keyword_pattern += word.decode('utf8')+'|'
    print "searching keywords : " + keyword_pattern[:-1]

    pattern = re.compile(u"((?:%s)[\u4e00-\u9fa5.%%\(\)\s\uff05\uff08\uff09]*)((?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})*)(?:.[0-9]{1,2})?)([\u4e00-\u9fa5\s]+)" % (keyword_pattern[:-1]))

    file_list = os.listdir(file_path)
    for file in file_list:
        name = file.split('.')
        if name[1].lower() == 'txt':

            f = open(file,'r')
            print ' '
            print file
            result = pattern.findall(f.read().decode('utf8'))
            if result:
                for sentence in result:
                    result_list.append([file,sentence[1], u"%s%s%s" % (sentence[0],sentence[1],sentence[2])])       
            else:
                print('nothing')
            f.close()


 #   ID_list = {}
 #   f = open('../stock.txt', 'r')
 #   line = f.readline()
 #   while line:
 #       ID_list[line.split('\t')[0]] = line.split('\t')[1].replace('"','').replace('\n','').replace(u'\u201d','').replace(u'\u201c','')
 #       line = f.readline()
 #   f.close()

    finalresult_list = []
    for result in result_list:
        ID = result[0].split('_')[0]
        finalresult_list.append((ID,result[0],result[1].replace(',',''),result[2].replace(u'\uff0c','').replace(',','').replace('\n','').replace('\t','')))
    
    headers = ['Stock ID','File Name','Cost','Description']

 #   for i in result_list:
 #       print(i)
    with open('result.csv','w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(finalresult_list)

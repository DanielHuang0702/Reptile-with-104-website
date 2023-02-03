import requests
from bs4 import BeautifulSoup
import jieba
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import openpyxl

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#if not os.path.exists('job_104_file'):
#    os.mkdir('job_104_file')

url = "https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001000&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=17&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

headers = {"User-Agent":user_agent}

page = 1

title_name_total_list=[]
title_url_total_list=[]
title_company_total_list=[]
title_content_total_list=[]
skill_list = []
total_list = []

skill_check_list = [
                    'CI', 'PYTHON', 'RUBY', 'JAVASCRIPT', 'GITLAB', 'JENKINS', 'DJANGO',
                    'NODE.JS', 'RESTFUL', 'MS SQL', 'GIT', 'GITHUB', 'C', 'C++', 'JAVA', 'RAILS', 'HTML', 'CSS',
                    'POSTGRESQL', 'MYSQL', 'MONGODB', 'QUNIT', 'MOCHA', 'JASMINE', 'RSPEC', 'DOCKER', 'K8S', 'VUEJS', 'RDBMS',
                    'NOSQL', 'KUBERNETS',
                    'KOTLIN', 'ANDROID STUDIO', 'SELENIUM', 'CUCUMBER', 'POSTMAN', 'SOAPUI', 'UI.VISION RPA', 'AA', 'UIPATH', 'C#',
                     'ASP.NET',
                    'HTML5', 'POSTAGESQL', 'BOOTSTRAP', 'JQUERY', 'SASS', 'REDIS', 'CELERY', 'KAFKA', 'MYSQL', 'MSSQL',
                    'POSTGRESQL', 'CLICKHOUSE',
                    'ANGULAR', 'CVS', 'SVN', 'C', 'HOOKS API', 'CUSTOMHOOKS', 'SWIFT', 'XCODE', 'LINUX', 'AWS', 'NUMPY', 'PANDAS',
                    'MATPLOTLIB', 'SEABORN',
                    'FLASK', 'SCRAPY', 'RPA', 'SAP', 'PHP', 'MEMCACHED', 'GCP', 'GO', 'AJAX', 'RTOS', 'ADMOB', 'EXCEL', 'SPRING',
                    'RABBITMQ', 'ROCKETMQ', 'NOSQL', 'NET',
                    'CNN', 'RNN', 'LSTM', 'SEQ2SEQ', 'NLP', 'JAVASE', 'JAVAEE', 'MYBATIS', 'AZURE', 'CASSANDRA', 'ECLIPSE', 'REACT',
                    'MCU', 'UNITY', 'SPLUNK', 'ARCSIGHT', 'ELK', 'QRADAR',
                    'SIEM', 'SOAR', 'ELK', 'BI', 'MYBATIS', 'WORDPRESS', 'RUBY', 'QUNIT', 'MOCHA', 'RSPEC', 'ANGULAR', 'TYPESCRIPT',
                    'BOOTSTRAP', 'FLUTTER', 'TCP/UDP', 'HTTP',
                    'UBUNTU', 'RED HAT', 'ORACLE', 'SQLITE', 'REDIS', 'POSTGRESQL', 'DOCKER', 'NGINX', 'GUNICORN', 'TORNADO',
                    'FPGA', 'CPLD', 'MC', 'MONGODB', 'RENDER', 'SHADER', 'VULKAN', 'MATLAB',
                    'PLC', 'SCADA', 'HMI', 'GOOGLE CLOUD PLATFORM', 'VB6', 'MVC', 'SWIFT', 'FLUTTER', 'SCRUM', 'OBJECTIVE-C',
                    'PANDAS', 'PLOTLY', 'VISUAL STUDIO C++', 'TCPIP', 'COCOS2D',
                    'HYPER-V', 'VMWARE', 'JSP', 'SCS', 'VEUX', 'SCRUM', 'KANBAN', 'SKETCH', 'ZEPLIN', 'AXURE', 'ILLUSTRATOR',
                    'PHOTOSHOP', 'MODBUS' ,'R','ASPNET','MVCNET','WORD','POWERPOINT','GIS','KERAS','TENSOR FLOW','PYTORCH',
                    'REDHAT','CICD','UIUX','.Net','NODEJS','AUTOCAD','ERP','ETL','TRELLO','BITBUCKET','TSQL','VB','BCB',
                    'PHOTOSHOP','ANDROID','LINUXBSP','BPM','MES','CCNA','RHCE','WINDOWS','IOS','HLK','WHCK','RS232','BIOS','CEPH',
                    'OPENSTACK','HIBERNATE','THYMELEAF','VISUALSTUDIO','COCOS','COBOL','OPENCV','DLIB','STSM32','MICROCHIP',
                    'VIEW','KUBERNETES','GCP','CISCO','OFFICE','ORCAD','MACHINELEARNING','DNN']

for i in range(0,150):

    res = requests.get(url.format(page), headers=headers)
    # print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    # print(soup)

    title_head_list = soup.select('[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
    for title_tag_list in title_head_list:
        if title_tag_list.find('a') == None:
            continue
        title_name_list = title_tag_list.find('a').text
        print(title_name_list)
        title_name_total_list.append(title_name_list)

        if title_tag_list.find('a') == None:
            continue
        title_url_list = 'http:'+title_tag_list.find('a')['href']
        print(title_url_list)
        title_url_total_list.append(title_url_list)

        title_company_list = title_tag_list['data-cust-name']
        print(title_company_list)
        title_company_total_list.append(title_company_list)
        # print(title_company_total_list)

        if title_tag_list.find('p') == None:
            continue
        title_content_list = title_tag_list.find('p').text
        title_content_total_list.append(title_name_list)
        print(title_content_list)

        if len(title_name_total_list) != len(title_content_total_list):
            title_content_total_list.append('NA')
            skill_list.append('NA')

        jieba.load_userdict('MY_104_DICT.txt')
        wc_generator = jieba.cut(title_content_list)

        wc_list = []
        for w in wc_generator:
            z = w.upper()  # 全改大寫
            y = z.replace(" ", "")  # 消除空格
            r = y.replace(".", "")  # 消除'.'
            u = r.replace("/", "")  # 消除'/'
            if u not in skill_check_list:  # 文字技能檢查
                continue
            wc_list.append(u)
            total_list.append(u)

        r = set(wc_list)  # 消除重複
        wc_list = list(r)  # 改回list
        skill_list.append(wc_list)
        print(wc_list)
        print('*' * 100)

    print("=" * 50, page, "=" * 50)
    page += 1
# counter
wc_map = dict()
for w in total_list:
    if w in wc_map:
        wc_map[w] += 1
    else:
        wc_map[w] = 1
# sort
wc_sort_list = [(k, v) for k, v in wc_map.items()]
wc_sort_list.sort(key=lambda x: x[1], reverse=True)
print(wc_sort_list)

# Data frame
mylabels_dataFrame = []
for i in range(10):
    mylabels_dataFrame.append(wc_sort_list[i][0])
    # print(mylabels_dataFrame)

a = (len(title_name_total_list),10)
zero_data = np.zeros(a)

df_skill = pd.DataFrame(zero_data,columns=mylabels_dataFrame)
print(len(title_name_total_list))
print(len(title_content_total_list))
print(len(skill_list))


for i in range(len(title_name_total_list)):
    for j in range(10):
        # skill_list[i] = list(map(str,skill_list[i]))
        if (mylabels_dataFrame[j]) in skill_list[i]:
            df_skill.loc[i][j] += 1


print(df_skill)

data = {

    "職缺" : title_name_total_list,
    "公司名稱" : title_company_total_list,
    "網址": title_url_total_list

}

df = pd.DataFrame(data)
final_df = pd.concat([df,df_skill],axis=1)
final_df = final_df.reset_index(drop=True)
print(final_df)

final_df.to_excel("job_104_file.xlsx")


# 圓餅圖
y = []
mylabels = []
for i in range(10):
    y.append(wc_sort_list[i][1])
    y_np = np.array(y)
    mylabels.append(wc_sort_list[i][0])

print(mylabels,":",y_np)

plt.figure(figsize = (20,6.5))
plt.pie(y_np, labels = mylabels,autopct='%.2f%%')
plt.legend(title = "TOP 10 tools",loc='upper left')
plt.show()

# 文字雲
wordcloud = WordCloud(font_path='fonts/TaipeiSansTCBeta-Regular.ttf').generate_from_frequencies(wc_map)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

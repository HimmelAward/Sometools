import argparse,json
from concurrent.futures import ThreadPoolExecutor
import requests_html




def config_open(type):
    allow = ['php','jsp','asp','mdb']
    with open("web_config/DIR.txt",'r') as fb:
        dir = [l.strip("\n") for l in fb.readlines()]
        if type == 'asp':
            with open("web_config/ASP.txt",'r') as f1:
                with open("web_config/ASPX.txt",'r') as f2:
                    return dir+[l.strip("\n") for l in f1.readlines()] + [l.strip("\n") for l in f2.readlines()]
        if type == 'php':
            with open("web_config/PHP.txt",'r') as f1:
                return dir + [l.strip("\n") for l in f1.readlines()]
        if type == 'jsp':
            with open('web_config/JSP.txt','r') as f1:
                 return dir + [l.strip("\n") for l in f1.readlines()]
        if type not in allow:
            print("Error Type")

def scan(url,headers):
    session = requests_html.HTMLSession()
    try:
        response =  session.get(url,headers = headers)
        if response.status_code == 200:
            return url
    except:
        pass

def show(results):
    for result in results:
        if result != None:
            print("{} is ok ".format(result))

def main(url,type = 'php',threads = 5, headers = {}):
    results = []
    pool = ThreadPoolExecutor(max_workers=threads)

    sites = config_open(type)
    for site in sites:
        full_url = url.strip("/") + site
        res = pool.submit(scan,full_url,headers)
        results.append(res.result())
    show(results)

if __name__ == "__main__":

    arg = argparse.ArgumentParser(description="this is a simple scanner of web")
    arg.add_argument('--url',type=str,)
    arg.add_argument('--type',type=str,default="php")
    arg.add_argument('--threads',type=int,default=5)
    arg.add_argument('--headers',type=str,)
    args = arg.parse_args()

    if args.url and args.type and args.threads:
        if args.headers:
            main(args.url,args.type,args.threads,json.loads(args.headers))
        else:
            main(args.url,args.type,args.threads)
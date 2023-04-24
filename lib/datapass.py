import argparse

from itertools import permutations

special = ['!','@','#','$','%','^','&','*','?','=','-','~','+']

def all_format_str(str):
    res = []
    str2 = ''.join([s for s in str if str>='A' and str<='Z'])

    for s in [str2,str]:
        res.append(s.lower())
        res.append(s.upper())
        res.append(s.title())

    return res

def get_pass_order(data:list,orders:list):
    password = ''
    for order in orders:
        password += data[order]

    return password

def is_int(int_str):
    is_true = [1 for n in int_str if n>='0' and n<='9']
    return len(is_true) == len(int_str)

def get_pass_key(keys):
    indexes = [i for i in range(len(keys))]
    orders = [list(o) for o in permutations(indexes)]
    res = []
    for order in orders:
        res.append(get_pass_order(keys,order))

    return res

def data_passwd(full_date,name):
    date = [full_date[:4],full_date[4:],full_date]
    names = all_format_str(name)
    res = []
    for d in date:
        for n in names:
            for e in special:
                res+= get_pass_key([d,n,e])

    return res

def main(args):
    res = data_passwd(full_date=args.data,name=args.name)
    with open(args.file,'w+') as fi:
        for r in res:
            fi.write(r+'\n')

import mwclient as mw
from mwclient import listing
from config import *
import os
import re


def open_browser(url: str):
    old_path = os.getcwd()
    os.chdir(chrome_path)
    os.system(f'./chrome "{url}"')
    os.chdir(old_path)


def generate_reason(reason: str):
    temp = reason.split('|')
    for i in range(len(temp)):
        try:
            temp[i] = eval(temp[i])
        except NameError:
            pass
    return '|'.join(temp)


def delete(page):
    pass


def keep(page):
    pass


def main():
    zh = mw.Site('zh.wikipedia.org')
    zh.login(username, passwd)
    csd = listing.Category(site=zh, name='Category:快速删除候选')
    for page in csd:
        curr_text = page.text()
        print(f'{curr_text}\n\n《{page.name}》\n\n')
        while 1:
            opt = input('[D]elete, [K]eep, [S]kip, [O]pen browser')
            if opt.upper() == 'D':
                delete(page)
            elif opt.upper() == 'K':
                keep(page)
            elif opt.upper() == 'S':
                continue
            elif opt.upper() == 'O':
                open_browser(f'zh.wikipedia.org/wiki/{page.name}')
            else:
                pass

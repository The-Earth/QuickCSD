import os
import re
import time

import mwclient as mw
from mwclient import listing

from config import *

delreg = re.compile(pattern)


def open_browser(url: str):
    old_path = os.getcwd()
    os.chdir(chrome_path)
    os.system(f'.\\chrome "{url}"')
    os.chdir(old_path)


def generate_reason(reason: str):
    temp = reason.split('|')
    for i in range(len(temp)):
        try:
            temp[i] = eval(temp[i])
        except:
            pass
    return '；'.join(temp)


def delete(page):
    while 1:
        reason = generate_reason(input('Reason: '))
        print('Reason: ', reason)
        confirm = input('Confirm? [Y]es, [N]o or [Q]uit:')
        if confirm.upper() == 'Y':
            print(page.delete(reason))
            break
        elif confirm.upper() == 'Q':
            break
        else:
            continue


def keep(page):
    while 1:
        reason = input('Reason: ')
        print('Reason: ', reason)
        confirm = input('Confirm? [Y]es, [N]o or [Q]uit:')
        if confirm.upper() == 'Y':
            old = page.text()
            new = re.sub(delreg, '', old)
            print(page.save(new, reason))
            break
        elif confirm.upper() == 'Q':
            break
        else:
            continue


def show_revision(rev):
    print('\nPrinting last 5 revisions:\n')
    for i in range(5):
        try:
            next_rev = next(rev)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', next_rev['timestamp'])
            print(f'User:{next_rev["user"]} - Time: {timestamp} - Comment: {next_rev["comment"]} - Revid:'
                  f' {next_rev["revid"]}')
        except StopIteration:
            print('No more revisions.\n')
            break


def main():
    zh = mw.Site(site)
    zh.login(username, passwd)
    csd = listing.Category(site=zh, name=csd_cat)
    for page in csd:
        if page.name.startswith('File') or page.name.startswith('Category'):
            continue
        curr_text = page.text()
        print(f'\n\n--------\n{curr_text}\n\n《{page.name}》\n')
        rev = page.revisions()
        while 1:
            opt = input('[D]elete, [K]eep, [S]kip, [O]pen browser or show last [R]evision: ')
            if opt.upper() == 'D':
                delete(page)
                break
            elif opt.upper() == 'K':
                keep(page)
                break
            elif opt.upper() == 'S':
                break
            elif opt.upper() == 'O':
                open_browser(f'{site}/wiki/{page.name}')
                break
            elif opt.upper() == 'R':
                show_revision(rev)
            else:
                pass


if __name__ == '__main__':
    main()
    os.system('pause')

import mwclient as mw
from mwclient import listing
from config import *
import os
import re

delreg = re.compile(r'\{\{\s*(db|[Dd]|sd|csd|speedy|delete|速刪|速删|快刪|快删)(\|.+)*\}\}')


def open_browser(url: str):
    old_path = os.getcwd()
    os.chdir(chrome_path)
    os.system(f'.\chrome "{url}"')
    os.chdir(old_path)


def generate_reason(reason: str):
    temp = reason.split('|')
    for i in range(len(temp)):
        try:
            temp[i] = eval(temp[i])
        except NameError:
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
            new = re.sub(delreg, '', old, count=1)
            print(page.save(new, reason))
            break
        elif confirm.upper() == 'Q':
            break
        else:
            continue


def main():
    zh = mw.Site(site)
    zh.login(username, passwd)
    csd = listing.Category(site=zh, name=csd_cat)
    for page in csd:
        if page.name.startswith('File') or page.name.startswith('Category'):
            continue
        curr_text = page.text()
        rev = page.revisions()
        print(f'\n\n--------\n{curr_text}\n\n《{page.name}》\n')
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
                print('\nPrinting last 5 revisions:\n')
                for i in range(5):
                    try:
                        print(next(rev))
                    except StopIteration:
                        pass
            else:
                pass


if __name__ == '__main__':
    main()
    os.system('pause')

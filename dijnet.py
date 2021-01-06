import mechanicalsoup
import traceback
import sys
import os

browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'}, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')

def login():
    browser.open('https://www.dijnet.hu/ekonto/control/nyitolap')
    browser.select_form('form[action="/ekonto/login/login_check_password"]')
    browser['username'] = ''
    browser['password'] = ''
    browser.submit_selected()

def logout():
    browser.open('https://www.dijnet.hu/ekonto/control/logout')
    browser.close()

def escapeFt(text):
    text = text.replace('Ft', '')
    text = text.replace('*', '')
    text = ''.join(text.split())
    return text

def parse_row(tr):
    td = tr.find_all('td')
    print(';'.join([escapeFt(t.text) if 'Ft' in t.text else t.text for t in td]))

def download_invoice(index, target_dir):
    url = 'https://www.dijnet.hu/ekonto/control/szamla_select?vfw_coll=szamla_list&vfw_rowid={}&exp=K'.format(index)
    browser.open(url)
    browser.open('https://www.dijnet.hu/ekonto/control/szamla_letolt')
    page = browser.get_current_page()
    links = page.find('div', class_='xt_link_cell__download')
    for link in links:
        if 'Hiteles számla' in link:
            download_link = browser.find_link(link_text=link)
    if download_link:
        data = browser.session.get(browser.absolute_url(download_link['href']))
        header = data.headers['Content-Disposition']
        fname = header.split(';')[1].split('=')[1]
        print('Downloading file: '.format(fname))
        with open(os.path.join(target_dir, fname), "wb") as f:
            f.write(data.content)
    
    browser.follow_link(page.select('a.xt_link__title')[0])

def list_invoices(download=True):
    browser.follow_link(link_text=u'Számlakeresés')
    browser.select_form(nr=0)
    if len(sys.argv) >= 3:
        browser['datumtol'] = sys.argv[2]
    if len(sys.argv) == 4:
        browser['datumig'] = sys.argv[3]
    browser.submit_selected()
    results = browser.get_current_page().find('table', class_='szamla_table').find_all('tr')
    index = 0
    for r in results:
        parse_row(r)
        if download:
            download_szamla(index, sys.argv[1])
        index = index + 1

try:
    login()
    list_invoices()
except:
    traceback.print_exc()
finally:
    logout()

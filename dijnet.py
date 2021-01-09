import mechanicalsoup
import traceback
import os
from util import *

class Dijnet():
    def __init__(self, args):
        self.browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'}, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        self.args = args

    def login(self):
        self.browser.open('https://www.dijnet.hu/ekonto/control/nyitolap')
        self.browser.select_form('form[action="/ekonto/login/login_check_password"]')
        auth = load_config('.dijnet', 'AUTH')
        self.browser['username'] = auth['username']
        self.browser['password'] = auth['password']
        self.browser.submit_selected()

    def logout(self):
        self.browser.open('https://www.dijnet.hu/ekonto/control/logout')
        self.browser.close()

    def escapeFt(self, text):
        return ''.join(text.replace('Ft', '').replace('*', '').split())

    def parse_row(self, tr):
        td = tr.find_all('td')
        return ';'.join([self.escapeFt(t.text) if 'Ft' in t.text else t.text for t in td])

    def download_invoice(self, index):
        downloaded = []
        if not self.args.downloadpath:
            return downloaded

        url = 'https://www.dijnet.hu/ekonto/control/szamla_select?vfw_coll=szamla_list&vfw_rowid={}&exp=K'.format(index)
        self.browser.open(url)
        self.browser.open('https://www.dijnet.hu/ekonto/control/szamla_letolt')
        page = self.browser.get_current_page()
        links = page.find_all('div', class_='xt_link_cell__download')
        for link in links:
            if 'Hiteles számla' in link.text or 'Terhelési összesítő és a hozzá tartozó számlák' in link.text:
                download_link = self.browser.find_link(link_text=link.text)
                if download_link:
                    data = self.browser.session.get(self.browser.absolute_url(download_link['href']))
                    header = data.headers['Content-Disposition']
                    fname = header.split(';')[1].split('=')[1]
                    with open(os.path.join(self.args.downloadpath, fname), "wb") as f:
                        f.write(data.content)
                    downloaded.append(fname)
        self.browser.follow_link(page.select('a.xt_link__title')[0])
        return downloaded

    def list_invoices(self):
        self.browser.follow_link(link_text=u'Számlakeresés')
        self.browser.select_form(nr=0)
        if self.args.datefrom:
            self.browser['datumtol'] = self.args.datefrom
        if self.args.dateto:
            self.browser['datumig'] = self.args.dateto
        self.browser.submit_selected()
        results = self.browser.get_current_page().find('table', class_='szamla_table').find_all('tr')
        index = 0
        for r in results:
            downloaded = self.download_invoice(index)
            index = index + 1
            print('{};{}'.format(self.parse_row(r), '{}'.format(','.join(downloaded)) if len(downloaded)>0 else ''))

def main(args):
    dijnet = Dijnet(args)
    try:
        dijnet.login()
        dijnet.list_invoices()
    except:
        traceback.print_exc()
    finally:
        dijnet.logout()

if __name__ == '__main__':
    args = create_argparser(__file__).parse_args()
    main(args)
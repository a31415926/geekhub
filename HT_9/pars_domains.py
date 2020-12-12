import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import choice
import os




main_domain = 'https://www.expireddomains.net'

def parse_list_domain_on_page(path = '/deleted-domains/?&ftlds[]=12#listing'):
    headers = {'user-agent':'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'upgrade-insecure-requests': '1', 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru', 'cache-control': 'no-cache',
            'pragma': 'no-cache', 'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1'}
    sleep(60)
    req = requests.get(f'{main_domain}{path}', headers = headers)
    soup = BeautifulSoup(req.text, 'lxml')
    lst_dmn = soup.select('.base1>tbody>tr')
    
    for dmn_info in lst_dmn:
        full_info_domain = {}
        full_info_domain['name'] = dmn_info.select_one('.namelinks').text
        full_info_domain['bl'] = dmn_info.select_one('.bllinks').text
        full_info_domain['dp'] = dmn_info.select_one('.field_domainpop').text
        full_info_domain['aby'] = dmn_info.select_one('.field_abirth').text
        full_info_domain['acr'] = dmn_info.select_one('.field_aentries').text
        full_info_domain['alexa'] = dmn_info.select_one('.field_alexa').text
        full_info_domain['field_dmoz'] = dmn_info.select_one('.field_dmoz').text
        full_info_domain['s_com'] = dmn_info.select_one('.field_statuscom').text
        full_info_domain['s_net'] = dmn_info.select_one('.field_statusnet').text
        full_info_domain['s_org'] = dmn_info.select_one('.field_statusorg').text
        full_info_domain['s_de'] = dmn_info.select_one('.field_statusde').text
        full_info_domain['tld_reg'] = dmn_info.select_one('.field_statustld_registered').text
        full_info_domain['rdt'] = dmn_info.select_one('.field_related_cnobi').text
        full_info_domain['dropped'] = dmn_info.select_one('.field_changes').text
        full_info_domain['status'] = dmn_info.select_one('.field_whois').text
        temp_link_status = dmn_info.select_one('.status_free')
        full_info_domain['status_link'] = f'{main_domain}{temp_link_status.get("href")}' if temp_link_status else ''

        write_domain_info_on_csv(full_info_domain)


    next_page = soup.select_one('.right .next') 
    if next_page:
        parse_list_domain_on_page(next_page.get('href'))


def write_domain_info_on_csv(domain_info_csv):
    with open(os.path.join(os.path.dirname(__file__), 'parse_domain.csv'), 'a+', newline='',encoding='utf-8') as f:
            fields = ['name', 'bl', 'dp', 'aby', 'acr', 'alexa', 'dmoz', 'free_com', 'free_net', 'free_org', 'free_de',
                        'tld_reg', 'rdt', 'dropped', 'status', 'status_link']
            
            dmn_csv = csv.DictWriter(f, fieldnames = fields, delimiter='|')
            dmn_csv.writerow({'name':domain_info_csv['name'], 'bl':domain_info_csv['bl'], 'dp':domain_info_csv['dp'], 'aby':domain_info_csv['aby'], 
                            'acr':domain_info_csv['acr'], 'alexa':domain_info_csv['alexa'], 'dmoz':domain_info_csv['field_dmoz'], 'free_com':domain_info_csv['s_com'],
                            'free_net':domain_info_csv['s_net'], 'free_org':domain_info_csv['s_org'], 'free_de':domain_info_csv['s_de'],'tld_reg':domain_info_csv['tld_reg'], 
                            'rdt':domain_info_csv['rdt'], 'dropped':domain_info_csv['dropped'], 'status':domain_info_csv['status'], 'status_link':domain_info_csv['status_link']})


def main():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'parse_domain.csv')):
        with open(os.path.join(os.path.dirname(__file__), 'parse_domain.csv'), 'w', newline='',encoding='utf-8') as f:
            fields = ['name', 'bl', 'dp', 'aby', 'acr', 'alexa', 'dmoz', 'free_com', 'free_net', 'free_org', 'free_de',
                        'tld_reg', 'rdt', 'dropped', 'status', 'status_link']
            dmn_csv = csv.DictWriter(f, fieldnames = fields, delimiter='|')
            dmn_csv.writeheader()

    parse_list_domain_on_page()



if __name__ == "__main__":
    main()
import requests

from bs4 import BeautifulSoup
from typing import Dict

# Função que faz  o scraping de produtos do mercado livre
def scraping_product_information(url) -> Dict:
    headers: dict = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find('h1', class_='ui-pdp-title')
    real = soup.find_all('span', class_='andes-money-amount__fraction')
    cents = soup.find_all('span', class_='andes-money-amount__cents')

    name_status = name.text.strip() if name else 'Não encontrado'
    price_status = real[1].text.strip() + '.' + cents[1].text.strip() if real and cents else 'Não encontrado'

    return {'name': name_status, 'price': price_status}
     

if __name__ == '__main__':
    product = scraping_product_information('https://www.mercadolivre.com.br/prinknut-creme-de-avel-balde-1kg/p/MLB19538579#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb-equivalent-offer&wid=MLB3707599765&reco_client=home_navigation-recommendations&reco_item_pos=0&reco_backend_type=function&reco_id=46ace3f2-d759-4bd6-a2d2-2a9887028361&sid=recos&c_id=/home/navigation-recommendations/element&c_uid=450b2219-b75d-480b-8eb5-d523c94359dc')
    print(product)
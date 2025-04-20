import requests

from bs4 import BeautifulSoup

from typing import Dict

# Função que faz  o scraping de produtos do mercado livre
def scraping_product_information(url: str) -> Dict:
    headers: dict = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find('h1', class_='ui-pdp-title')
    name_status = name.text.strip() if name else 'Não encontrado'
    price_parent_tag = soup.select_one('span.andes-money-amount[aria-label]') 
    
    if price_parent_tag:
        real = price_parent_tag.find('span', class_='andes-money-amount__fraction')
        cents = price_parent_tag.find('span', class_='andes-money-amount__cents')
        if not cents:
            price = float(real.text.strip().replace('.', '')) if real else 'Não Encontrado'
        else:
            price = float(real.text.strip().replace('.', '') + '.' + cents.text.strip()) if real else 'Não encntrado'
    
    return {'name': name_status, 'price': price}
     
if __name__ == '__main__':
    product = scraping_product_information('https://www.mercadolivre.com.br/redmi-note-13-4g-dual-sim-256gb-preto-8-gb-ram/p/MLB29751162#polycard_client=recommendations_home_second-best-navigation-trend-recommendations&reco_backend=machinalis-homes-univb&wid=MLB5261379674&reco_client=home_second-best-navigation-trend-recommendations&reco_item_pos=5&reco_backend_type=function&reco_id=f43cb33f-4710-4048-b62b-9af779f777b5&sid=recos&c_id=/home/second-best-navigation-trend-recommendations/element&c_uid=289a593c-455a-4e68-90f1-05c9d752f4ef')
    print(product)
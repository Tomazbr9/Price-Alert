import requests

from bs4 import BeautifulSoup

from typing import Dict

def scraping_product_information(url: str) -> Dict:
    """
    Função que faz o scraping de produtos do mercado livre
    """
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
     
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
        price = float(f'{real.text.strip()}.{cents.text.strip()}') if real and cents else 'Não Encontrado' 
        return {'name': name_status, 'price': price}
    

    return {'name': name_status, 'price': 'Não Encontrado'}
     
if __name__ == '__main__':
    product = scraping_product_information('https://www.mercadolivre.com.br/sony-playstation-4-slim-1tb-fifa-19-bundle-cor-preto-onyx/p/MLB13876219#reco_item_pos=1&reco_backend=item_decorator&reco_backend_type=function&reco_client=home_items-decorator-legacy&reco_id=c91c4ea7-5d40-49ae-a626-16acd405a1fc&reco_model=&c_id=/home/navigation-trends-recommendations/element&c_uid=42adda19-3d61-4a85-bc9d-a09571502d04&da_id=navigation_trend&da_position=3&id_origin=/home/dynamic_access&da_sort_algorithm=ranker')
    print(product)
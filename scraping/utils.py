import requests
from bs4 import BeautifulSoup

def get_offers():
    url = 'https://www.mercadolibre.com.ar/ofertas#nav-header'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Asegúrate de encontrar el contenedor correcto para los productos
        products_container = soup.find_all('div', class_='poly-card__content')

        offers = []
        for product in products_container:
            title_element = product.find('a', class_='poly-component__title')
            price_element = product.find('span', class_='andes-money-amount andes-money-amount--cents-superscript')
            discount_element = product.find('span', class_="andes-money-amount__discount")
            link_element = product.find('a')

            if not title_element or not price_element or not link_element:
                continue  # Saltar este producto si no se encuentra alguno de los elementos

            title = title_element.get_text()
            price = price_element.get_text()
            discount = discount_element.get_text() if discount_element else 'Sin descuento'
            link = link_element['href']

            offers.append({
                'title': title,
                'price': price,
                'discount': discount,
                'link': link
            })
        
        return offers
    else:
        return []

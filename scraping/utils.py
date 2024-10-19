import requests
from bs4 import BeautifulSoup

def get_offers():
    url = 'https://www.mercadolibre.com.ar/ofertas#nav-header'  # Cambia esto por la URL de la página real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Ajusta el selector para obtener las ofertas según la estructura HTML del sitio
        products = soup.find_all('div', class_='poly-card__content')  # Cambia esto según el sitio

        offers = []
        for product in products:
            title = product.find('a', class_='poly-component__title').get_text()  # Ajusta el selector
            price = product.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').get_text()
            discount_element = product.find('span', class_="andes-money-amount__discount")
            discount = discount_element.get_text() if discount_element else 'Sin descuento'
            link = product.find('a')['href']

            offers.append({
                'title': title,
                'price': price,
                "discount": discount,
                'link': link
            })
        
        return offers
    else:
        return []

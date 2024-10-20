import requests
from bs4 import BeautifulSoup

def get_offers():
    url = 'https://www.mercadolibre.com.ar/ofertas?container_id=MLA779357-3&category=MLA1648#deal_print_id=38647970-8e63-11ef-9a39-593bd032a5af&c_id=carouseldynamic-home&c_element_order=undefined&c_campaign=VER-MAS&c_uid=38647970-8e63-11ef-9a39-593bd032a5af'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encuentra todos los elementos de productos
        products_container = soup.find_all('div', class_='poly-card__content')

        offers = []
        for product in products_container:
            image_url = product.find_previous('img', class_='poly-component__picture lazy-loadable')  # Obtener la imagen correspondiente
            title_element = product.find('a', class_='poly-component__title')
            price_element = product.find('span', class_='andes-money-amount__fraction')
            og_price_element = product.find('s', class_='andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma')
            discount_element = product.find('span', class_='andes-money-amount__discount')
            link_element = title_element  # La misma etiqueta de título es el enlace

            if not image_url or not title_element or not price_element or not og_price_element or not link_element:
                continue  

            image = image_url['data-src'] 
            title = title_element.get_text()
            price = price_element.get_text()
            og_price = og_price_element.get_text()
            discount = discount_element.get_text() if discount_element else 'Sin descuento'
            link = link_element['href']

            offers.append({
                'image': image,
                'title': title,
                'price': price,
                'og_price': og_price,
                'discount': discount,
                'link': link
            })

        return offers
    else:
        return []
import requests
from django.core.cache import cache
from bs4 import BeautifulSoup

def get_offers():
    cached_offers = cache.get('offers')

    if cached_offers:
        return cached_offers

    base_url = 'https://www.mercadolibre.com.ar/ofertas?container_id=MLA779357-3&category=MLA1648&page='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    offers = []
    page = 1

    while True:
        url = base_url + str(page)
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            break

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        products_container = soup.find_all('div', class_='poly-card__content')

        for product in products_container:
            image_url = product.find_previous('img', class_='poly-component__picture lazy-loadable') 
            title_element = product.find('a', class_='poly-component__title')
            price_element = product.find('div', class_='poly-price__current')
            price_fraction = price_element.find('span', class_='andes-money-amount__fraction') if price_element else None
            og_price_element = product.find('s', class_='andes-money-amount')
            og_price_fraction = og_price_element.find('span', class_='andes-money-amount__fraction') if og_price_element else None
            discount_element = product.find('span', class_='andes-money-amount__discount')
            link_element = title_element  

            if not image_url or not title_element or not price_element or not og_price_element or not link_element:
                continue  
            
            title = title_element.get_text() if title_element else "no disponible"
            image = image_url['data-src'] 
            price = price_fraction.get_text() if price_fraction else 'No disponible'
            og_price = og_price_fraction.get_text() if og_price_fraction else 'No disponible'
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

        # Verificar si hay un botón "Siguiente"
        next_button = soup.find('li', class_='andes-pagination__button--next')
        if next_button and 'andes-pagination__button--disabled' not in next_button.get('class', []):
            page += 1
        else:
            break
        print(url)

    cache.set('offers', offers, timeout=60 * 15)
    return offers

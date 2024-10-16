from typing import Any
import scrapy
from scrapy.http import Response


class HoferScraperSpider(scrapy.Spider):
    name = 'hoferscraper'

    start_urls = [
        'https://www.hofer.at/de/sortiment/produktsortiment/brot-und-backwaren.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/kuehlung.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/fleisch-und-fisch.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/vorratsschrank.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/suesses-und-salziges.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/tiefkuehlung.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/getraenke.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/drogerie.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/haushalt.html',
        'https://www.hofer.at/de/sortiment/produktsortiment/tierbedarf.html',
        'https://www.hofer.at/de/sortiment/hofer-eigenmarken/flying-power.html',
    ]

    def parse(self, response: Response, **kwargs: Any) -> None:
        # List to store cleaned product data
        cleaned_products = []

        # Select product items from the response
        products = response.css('article.wrapper')

        # Iterate over each product and collect data
        for product in products:
            # Extracting name and price
            name = product.css('h2.product-title.at-all-productName-lbl::text').get()
            price = product.css('span.price.at-product-price_lbl::text').get()

            # Clean the data (strip whitespace if needed)
            if name:
                name = name.strip()

            if price:
                # Remove '€' symbol and replace comma with dot, then convert to float
                price = price.replace('€', '').replace(',', '.').strip()
                try:
                    price = float(price)
                except ValueError:
                    price = None  # In case conversion fails

            # Append cleaned product data to the list
            cleaned_products.append({
                'name': name,
                'price': price
            })

        # Log or process the cleaned data
        self.log(f'Found {len(cleaned_products)} products on {response.url}')

        # Return the cleaned products
        return cleaned_products

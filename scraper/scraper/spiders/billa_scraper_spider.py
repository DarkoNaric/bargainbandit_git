from typing import Any, Dict, List
import scrapy
from scrapy.http import Response

class BillaScraperSpider(scrapy.Spider):
    name = 'billascraper'
    start_urls = [
        'https://shop.billa.at/kategorie/brot-und-gebaeck-13766?page=1',
        'https://shop.billa.at/kategorie/getraenke-13784?page=1',
        'https://shop.billa.at/kategorie/kuehlwaren-13841?page=1',
        'https://shop.billa.at/kategorie/tiefkuehl-13916?page=1',
        'https://shop.billa.at/kategorie/nahrungsmittel-13943?page=1',
        'https://shop.billa.at/kategorie/suesses-und-salziges-14057?page=1',
        'https://shop.billa.at/kategorie/pflege-14083?page=1',
        'https://shop.billa.at/kategorie/geschenksideen-14267?page=1',
        'https://shop.billa.at/kategorie/haustier-14181?page=1',
        'https://shop.billa.at/kategorie/haushalt-14126?page=1'
    ]

    def parse(self, response: Response, **kwargs: Any) -> None:
        # List to store cleaned product data
        cleaned_products = []

        # Select product items from the response
        products = response.css('.ws-product-item-base.ws-product-tile.ws-card')

        # Check if there are products on the page
        if not products:
            self.logger.info("No products found on this page. Stopping the crawl.")
            return  # Stop further requests if no products found

        # Iterate over each product and collect data
        for product in products:
            # Extract the product name and price
            name = product.css("span.line-clamp-3::text").get(default='').strip()
            price = product.css(".ws-product-price-type__value.subtitle-1::text").get(default='').strip()

            # Clean the price if necessary
            cleaned_price = self.clean_price(price)

            # Store the cleaned product data in the list
            cleaned_products.append({
                'name': name,
                'price': cleaned_price,
            })

        # Log the collected products from the current page
        self.logger.info(f"Collected {len(cleaned_products)} products from page {response.url}")

        # Yield all cleaned products at once
        for product in cleaned_products:
            yield product

        # Get the current page number from the URL
        current_page = int(response.url.split('page=')[-1])
        next_page = current_page + 1  # Increment the page number
        next_page_url = f'https://shop.billa.at/kategorie{response.url.split("kategorie")[-1].split("?")[0]}?page={next_page}'

        # Log the current and next page number for debugging
        self.logger.info(f"Current page: {current_page}, Next page: {next_page}")

        # Make a request to the next page if products were found
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def clean_price(self, price: str) -> float:
        """
        Clean the price string and convert it to a float.
        Removes currency symbols and converts to a proper format.
        """
        if price:
            # Remove special characters, including currency symbols
            price_cleaned = price.replace('\xa0', '').replace('€', '').replace(',', '.').strip()
            try:
                return float(price_cleaned)  # Convert to float
            except ValueError:
                self.logger.warning(f"Unable to convert price '{price}' to float.")
                return 0.0  # Return a default value or handle as necessary
        return 0.0  # Default if price is empty or None

from scraper.common import ScrapeResult, Scraper, ScraperFactory


class SabrePCScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''
        
        # get name of product
        tag = self.soup.body.select_one('h2product-description#')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('#product-listing-price-text')
        price_str = self.set_price( tag.text.strip() )
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.select_one('#product-list-add-to-cart a.button_primary') 
        
        if tag and 'add to cart' in tag.text.lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class SabrePCScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'sabrepc'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return SabrePCScrapeResult

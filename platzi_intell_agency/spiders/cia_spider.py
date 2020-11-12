import scrapy


class CiaSpider(scrapy.Spider):
    name = 'cia_spider'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections']
    custom_settings = {'FEED_URI': 'save.json',
                       'FEED_FORMAT': 'json', 'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        article_links = response.xpath(
            '//a[starts-with(@href, "collection") and (parent::h2|parent::h3)]/@href').getall()

        for link in article_links:
            yield response.follow(link, callback=self.parse_article, cb_kwargs={'url': response.urljoin(link)})

    def parse_article(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="documentFirstHeading"]/text()').get()
        body = ''.join(response.xpath(
            '//div[contains(@class, "field-item")]/p[not(child::strong and child::i) and not(@class)]/text()').getall())
        img = response.xpath(
            '//div[contains(@class, "field-item")]//img/@src').get()

        yield {'link': link, 'img': response.urljoin(img) if img else None, 'title': title, 'body': body}

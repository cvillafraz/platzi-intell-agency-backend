import scrapy


class Spider12(scrapy.Spider):
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'FEED_FORMAT': 'json', 'FEED_URI': 'results.json',
                       "DEPTH_LIMIT": 2, "FEED_EXPORT_ENCODING": "utf-8"}

    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/ciencia',
                  'https://www.pagina12.com.ar/secciones/el-mundo']

    def parse(self, response):
        # Promoted article
        promoted = response.xpath(
            '//section[@id="top-content"]//h2/a/@href').get()

        if promoted is not None:
            yield response.follow(promoted, callback=self.parse_article)
        # Article list
        articles = response.xpath(
            '//section[@id="list-content"]//a[parent::h3[@class="title-list"]| parent::h4[contains(@class, "title-list")]]/@href').getall()
        for article in articles:
            yield response.follow(article, callback=self.parse_article)
        # Next page
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        title = response.xpath('//h1[@class="article-title"]/text()').get()
        body = ''.join(response.xpath(
            '//div[@class="article-text"]/p/text()').getall())
        yield {'response_url': response.url, 'title': title, 'body': body}

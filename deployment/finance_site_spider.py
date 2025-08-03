import scrapy

class FinanceSiteSpider(scrapy.Spider):
    name = "finance_sites"
    allowed_domains = [
        "investopedia.com",
        "bankrate.com",
        "nerdwallet.com",
        "smartasset.com",
        "zerodha.com"
    ]
    start_urls = [
        "https://www.investopedia.com/",
        "https://www.bankrate.com/investing/",
        "https://www.nerdwallet.com/h/category/personal-finance",
        "https://smartasset.com/investing",
        "https://zerodha.com/varsity/"
    ]

    custom_settings = {
        'DEPTH_LIMIT': 3,  # Adjust as needed for deeper crawling
        'DOWNLOAD_DELAY': 0.5,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'crawled_finance_docs.json'
    }

    def parse(self, response):
        # Extract main content from the page
        title = response.xpath('//title/text()').get()
        paragraphs = response.xpath('//p//text()').getall()
        content = "\n".join(paragraphs)
        yield {
            'url': response.url,
            'title': title,
            'content': content
        }
        # Follow links within the same domain
        for href in response.css('a::attr(href)').getall():
            if href and href.startswith('/'):
                yield response.follow(href, self.parse)
            elif href and any(domain in href for domain in self.allowed_domains):
                yield response.follow(href, self.parse)

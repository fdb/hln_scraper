import scrapy

HLN_COOKIES = {
    'pws': 'functional|analytics|content_recommendation|targeted_advertising|social_media',
    'pwv': '1'
}

class ArticleSpider(scrapy.Spider):
    name = 'articleSpider'
    start_urls = ['https://www.hln.be/']

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            print(url)
            yield scrapy.Request(url, cookies=HLN_COOKIES)

    def parse(self, response):
        for article in response.css('article'):
            article_data = {
                'title': article.css('h1::attr(title)').extract_first(),
                'url': article.css('a::attr(href)').extract_first()
            }
            #yield article_data
            yield scrapy.Request(article_data['url'], cookies=HLN_COOKIES, callback=self.parse_article)

    def parse_article(self, response):
        print('parsing article', response)
        comments = []
        for comment in response.css('.comments__list'):
            comment_data = {
                'author': comment.css('.comment__author::text').extract_first(),
                'body': comment.css('.comment__body::text').extract_first(),
                'time': comment.css('.comment__time::attr(datetime)').extract_first()
            }
            comments.append(comment_data)
        yield {
            'url': response.url,
            'title': response.css('.article__title::text').extract_first(),
            'time': response.css('.article__metadata-item time::attr(datetime)').extract_first(),
            'comments': comments
        }

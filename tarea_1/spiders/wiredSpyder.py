import scrapy
from utils import validateDate, convertDate
from ManageArticles import ManageArticles

class WiredspyderSpider(scrapy.Spider):
    name = "wiredSpyder"
    allowed_domains = ["www.wired.com"]
    start_urls = ["https://www.wired.com/category/science/"]
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'wired'
        self.manageArticles.load_articles(self.origin)

    def parse(self, response):
        groups  = response.css("div.summary-list__items")
        for group in groups:
            articles = group.css("div.summary-item--article")
            for article in articles:
                title = article.css("h3.summary-item__hed::text").get()
                link = article.css("a.summary-item-tracking__hed-link::attr(href)").get()
                image = article.css("img.responsive-image__image::attr(src)").get()
                if not title:
                    continue
                previus = {
                    "title": title,
                    "link": response.urljoin(link),  # Convierte URL relativa en absoluta
                    "image": image,
                }
                if(link):
                    yield response.follow(link, self.parse_detail, meta=previus)
                else:
                    yield {
                        "title": title,
                        "link": response.urljoin(link),
                        "image": image,
                    }
    
    def parse_detail(self, response):
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('div.ContentHeaderDek-bIqFFZ::text').get()
        date_published = response.css('time::attr(datetime)').get()
        date_published = convertDate(date_published)
        author = response.css('[itemprop="name"] a::text').get()
        segments = response.css('div.body__inner-container p::text').getall()
        article_information = {
            'title': title,
            'link': link,
            'image': image,
            'resume': resume,
            'date_published': date_published.isoformat(),
            'author': author,
            'segments': segments,
        }
        if(not self.manageArticles.article_exist(self.origin, article_information['title'])):
            self.manageArticles.articles[self.origin].append(article_information)
        if validateDate(date_published):
            yield article_information

    def closed(self, reason):
        self.manageArticles.save_articles()

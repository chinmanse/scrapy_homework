import scrapy
from utils import validateDate, convertDate
from ManageArticles import ManageArticles

class ParadespyderSpider(scrapy.Spider):
    name = "paradeSpyder"
    allowed_domains = ["parade.com"]
    start_urls = ["https://parade.com/"]

    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'parade'
        self.manageArticles.load_articles(self.origin)

    def parse(self, response):
        groups  = response.css("section.m-list-hub")
        for group in groups:
            articles = group.css("div.l-grid--item")
            for article in articles:
                title = article.css("h2.m-ellipsis--text::text").get()
                # title = article.css("a::attr(data-component-title)").get()
                link = article.css("a::attr(href)").get()
                image = article.css("img.m-card--image-element::attr(src)").get()
                previus = {
                    "title": title,
                    "link": response.urljoin(link),
                    "image": image,
                }
                yield response.follow(link, self.parse_detail, meta=previus)

    
    def parse_detail(self, response):
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('div.m-detail-header--dek::text').get()
        date_published = response.css('time::attr(datetime)').get()
        date_published = convertDate(date_published)
        author = response.css('a.m-detail-header--meta-author::text').get()
        segments = response.css('div.m-detail--body p::text').getall()
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
            yield {
                'title': title,
                'link': link,
                'image': image,
                'resume': resume,
                'date_published': date_published,
                'author': author,
                'segments': segments,
            }

    def closed(self, reason):
        self.manageArticles.save_articles()

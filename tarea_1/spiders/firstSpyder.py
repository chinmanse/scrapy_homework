import scrapy
from utils import validateDate, convertDate
from ManageArticles import ManageArticles

class FirstspyderSpider(scrapy.Spider):
    name = "firstSpyder"
    allowed_domains = ["thenextweb.com"]
    start_urls = ["https://thenextweb.com/latest"]
    def __init__(self):
        self.manageArticles = ManageArticles()
        self.origin = 'thenextweb'
        self.manageArticles.load_articles(self.origin)

    def parse(self, response):
        for article in response.css("article.c-listArticle"):
            article_title = article.css("h2.c-listArticle__heading") 
            title = article_title.css('a::text').get()
            link = article_title.css("a::attr(href)").get()
            image = article.css("figure.c-listArticle__image")
            image = image.css('img::attr(src)').get()
            if(not title):
                continue
            yield response.follow(link, self.parse_detail, meta={'title': title, 'link': link, 'image': image})
    
    def parse_detail(self, response):
        title = response.meta.get('title')
        link = response.meta.get('link')
        image = response.meta.get('image')
        resume = response.css('p.c-header__intro::text').get()
        date_published = response.css('time::attr(datetime)').get()
        date_published = convertDate(date_published)
        author = response.css('span.c-article__authorName::text').get()
        segments = response.css('#article-main-content p::text').getall()
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

        if(validateDate(date_published)):
            yield article_information

    def closed(self, reason):
        self.manageArticles.save_articles()


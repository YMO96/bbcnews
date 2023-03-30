import scrapy
import csv
import re
import sqlalchemy
from bbc_movies.items import BbcMoviesItem
from bbc_movies.conn_tcp import connect_with_connector
from urllib.parse import urljoin
from datetime import datetime


def save_to_csv(items):
    with open('articles.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'author', 'date', 'text'])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerows(items)

class BBCSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/news/topics/cg41ylwvgjyt']
    #start_urls = ['https://www.bbc.com/news/entertainment_and_arts']
    count = 0

    engine= connect_with_connector()
    def parse(self, response):
        news_links = response.css('.ssrcss-i9iip6-PromoLink::attr(href)').getall()
        #news_links = response.css('.ssrcss-i9iip6-PromoLink:not([class*="SoundsPlayButton"])::attr(href)').getall()
        print(len(news_links))
        for link in news_links:
            full_link = urljoin(response.url, link)
            print(full_link)
            if re.match(r'^https://www.bbc.com/news/.*', full_link) and not re.match(r'.*/sounds/play/.*', full_link):
                self.count += 1
                if self.count <= 20 :
                    yield scrapy.Request(url=full_link, callback=self.parse_news)
        if self.count < 10:
            next_page = response.css('.pagination__next > a::attr(href)').get()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def parse_news(self, response):
        title = response.xpath('//h1/text()').get()
        author = response.css('.ssrcss-68pt20-Text-TextContributorName::text').get()
        date = response.css('time[data-testid="timestamp"]::attr(datetime)').get()
        text = "".join(response.css('.ssrcss-1q0x1qg-Paragraph::text').getall())
        text = text.replace("'", "").replace('"', '')
        #text = "\n".join(response.css('.ssrcss-1q0x1qg-Paragraph::text').getall())
        item = BbcMoviesItem() # create an instance of Item
        item['title'] = title
        item['author'] = author
        item['date'] = date
        item['text'] = text
        try:
            jour = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        except ValueError:
            jour = None
        if jour == datetime.now().date():
            save_to_csv(item)
            insert_query = sqlalchemy.text("""
                INSERT INTO movienews (title, author, date_news, text, loadtime)
                VALUES (:title, :author, :date, :text, NOW())
                """)

            self.engine.execute(insert_query,
                title=item['title'],
                author=item['author'],
                date=item['date'],
                text=item['text'])

        yield item

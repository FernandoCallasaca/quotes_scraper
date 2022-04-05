import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class = "text" and @itemprop = "text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()


# inherist from scrapy.Spider
class QuotesScraper(scrapy.Spider):

   # unique name who scrapy can refer to spider
   # inside the project, non repeat tame
   name = "quotes"
   # contain all the urls that we are goint to use
   start_urls = [
      "https://quotes.toscrape.com/"
   ]

   # important method
   # parse = analizar un archivo para extraer información valiosa
   def parse(self, response):

      # # to see the results on console
      # print('*' * 10)
      # print('\n\n\n')
      # # print(response.status, response.headers)
      # title = response.xpath('//h1/a/text()').get()
      # print(f'Título: {title}')
      # print('\n\n')

      # quotes = response.xpath('//span[@class = "text" and @itemprop = "text"]/text()').getall()
      # print('Citas: ')
      # for quote in quotes:
      #    print(f'- {quote}')
      # print('\n\n')

      # top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()').getall()
      # print('Top Ten Tags: ')
      # for tag in top_ten_tags:
      #    print(f'- {tag}')
      # print('\n\n\n')
      # print('*' * 10)

      title = response.xpath('//h1/a/text()').get()
      quotes = response.xpath('//span[@class = "text" and @itemprop = "text"]/text()').getall()
      top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()').getall()

      

      # inside the project
      # "scrapy crawl quotes" para ver lo que está en parse

# scrapy no abre el entorno del sitio web
# scrapy shell "https://quotes.toscrape.com/"

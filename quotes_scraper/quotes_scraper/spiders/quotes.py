import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class = "text" and @itemprop = "text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()
# Autores = //div[@class="quote"]//small[@class = "author" and @itemprop = "author"]/text()

# Next page button = //ul[@class="pager"]/li[@class="next"]/a/@href

# inherist from scrapy.Spider
class QuotesScraper(scrapy.Spider):

   # unique name who scrapy can refer to spider
   # inside the project, non repeat tame
   name = "quotes"
   # contain all the urls that we are goint to use
   start_urls = [
      "https://quotes.toscrape.com/"
   ]

   # atributo para guardar un archivo de forma automática
   custom_settings = {
      'FEED_URI': 'quotes.json', # para el nombre del archivo
      'FEED_FORMAT': 'json', # el formato en el que se guardará

      # otras configuraciones para sacarle provecho a este framework
      # para decirle cuantas peticiones tiene que hacer scrapy
      'CONCURRENT_REQUESTS': 24, # que haga 24 peticiones a la vez ya que asíncrono

      # cantidad de memoria ram que le permitimos usar a scrapy para trabajar
      'MEMUSAGE_LIMIT_MB': 2048,

      # si la memoria ram llega al límite se pasa hay que notificar
      'MEMUSAGE_NOTIFY_MAIL': ['fernandocallasaca@outlook.com'],

      # decirle si va a obedecer o no al archivo robots
      'ROBOTSTXT_OBEY': True, # en lo posible siempre tru para que obedezca

      # cambiar el USER_AGENT = cabecera http que está en la petición
      # para indicar al sitio web quienes somo nosotros (chrome, safari, iphone, etc)
      'USER_AGENT': 'fernando', # en el servidor cuando se ejecute este spider
      # y llegue la petición ahí aparecerá la persona que hizo la petición

      # Lo Tenemos que hacer para solucionar el erro de encoding
      'FEED_EXPORT_ENCODING': 'utf-8', # para las tildes, eñes, etc 
   }
   # luego de eso de frente podemos tipear "scrapy crawl quotes"
   # y guardará lo que está en el yield como si pondriamos -o quotes.json

   # IMPORTANTE
   # creamos un nuevo método de tipo parse
   # este método extraerá exclusivamente la cita
   # un método tipo 'parse' siempre tiene que recibir una respuesta 'http'
   # para poder trabajar con ello por eso el parámetro es 'response'
   
   # lo primero que se hace es recibir los 'kwargs' que me estoy mandando
   # en el método 'response.follow()'

   def parse_only_quotes(self, response, **kwargs):
      # preguntamos si existe kwargs
      if kwargs:
         # si existe guardamos lo que está dentro del diccionario
         quotes_list = kwargs['quotes_list']
         # quotes es una lista
         # ahora tengo que agregar a esa lista nuevos resultados

         quotes = response.xpath('//span[@class = "text" and @itemprop = "text"]/text()').getall()
         authors = response.xpath('//div[@class="quote"]//small[@class = "author" and @itemprop = "author"]/text()').getall()

         quotes_list.extend([[quote, author] for quote, author in zip(quotes, authors)])

      # calculamos nuevamente para traerme el link "next"
      next_page_button_link = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
      # preguntamos si ese botón existe
      if next_page_button_link:
         yield response.follow(next_page_button_link,
                                 callback=self.parse_only_quotes,
                                 cb_kwargs = {
                                    # 'quotes': quotes,
                                    'quotes_list': quotes_list
                                 })
      # en el caso no exista otra página 'next'
      else:
         yield {
            # como ya se fue llenando lo exportamos
            # 'quotes': quotes
            'quotes_list': quotes_list
         }


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

      # top_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()').getall()
      # print('Top Ten Tags: ')
      # for tag in top_tags:
      #    print(f'- {tag}')
      # print('\n\n\n')
      # print('*' * 10)

      title = response.xpath('//h1/a/text()').get()
      top_tags = response.xpath('//div[contains(@class, "tags-box")]/span[@class = "tag-item"]/a/text()').getall()
      quotes = response.xpath('//span[@class = "text" and @itemprop = "text"]/text()').getall()
      authors = response.xpath('//div[@class="quote"]//small[@class = "author" and @itemprop = "author"]/text()').getall()
      
      # con esta linea de código
      # le preguntamos a scrapy
      # si existe dentro de la ejecución de este spider
      # un atributo de nombre 'top'
      # voy a guardar ese resultado dentro de la variable 'top'
      # si ese ejecuto jamás se envió o no existe el resultado es 'None'
      top = getattr(self, 'top', None)
      if top:
         top = int(top)
         top_tags = top_tags[:top]
      # ahora ejecutamos en consola y agregamos otro argumento
      # 'scrapy crawl quotes -a top=3'
      # -a = flag arguments
      # top = variable y el valor

      yield {
         'title': title,
         # 'quotes': quotes, # sacamos los quotes
         'top_ten_ten': top_tags
      }

      # traemos el link "next"
      next_page_button_link = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
      # preguntamos si ese botón existe
      if next_page_button_link:
         # entonces retornamos parcialmante
         # si existe seguimos ese link y repetimos el método
         # osea scrapy toma la url absoluta y lo junta con la parte relativa
         # luego de hacer la request ejecutamos la función self.parse

         # antes aquí devolvía self.parse
         # pero como ahora estamos creando otro metodo de tipo parse
         # en que solo se encargará de devolver las citas entonces
         # llamamos al método 'parse_only_quotes'

         # luego enviaremos a este método una serie de argumentos(citas de la primera página)
         # eso hacemos con 'cb_kwargs' = keyword arguments = diccionario en el 
         # cual yo le paso argumentos a mi otra función
         yield response.follow(next_page_button_link,
                                 callback=self.parse_only_quotes,
                                 cb_kwargs = {
                                    # 'quotes': quotes
                                    'quotes_list': [[quote, author] for quote,author in zip(quotes, authors)]
                                 })


      # inside the project
      # esto lo usamos para llamar a un spider
      # "scrapy crawl quotes" para ver lo que está en parse
      # "scrapy crawl quotes -o quotes.csv" = -o:output

# scrapy no abre el entorno del sitio web
# scrapy shell "https://quotes.toscrape.com/"

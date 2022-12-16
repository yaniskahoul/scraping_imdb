import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items   import ImdbItem

class CrawlerBooksSpider(CrawlSpider):
    name = 'crawl_movies'
    allowed_domains = ['imdb.com']
    custom_settings = {  "ITEM_PIPELINES": {'imdb.pipelines.MoviesPipeline': 300}
                        }   
    

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

     
    rules = (
        Rule(LinkExtractor(restrict_xpaths= "//td[@class='titleColumn']/a"), callback='parse_item', follow=False),
    ) 

    def parse_item(self, response):
        item = ImdbItem()
        item['title'] = response.xpath("//h1/text()").get()
        item['score'] = response.xpath("//span[@class='sc-7ab21ed2-1 jGRxWM']/text()").get() 
        item['genre'] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/div[2]/a/span/text()").get()
        
        item['date'] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[1]/a/text()").get()
        item['acteurs'] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()").extract()
        item['public'] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a/text()").get()

        if len(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()").getall()) == 5:
            item['durée'] = int(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()").getall()[0]) * 60 + int(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()").getall()[3])
        else:
            item['durée'] = int(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()").getall()[0])
        
        item['description'] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/span[2]/text()").get()
        item['pays']= response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section/div[2]/ul/li[2]/div/ul/li/a/text()').extract()[:-1]
        
        yield item
        
        


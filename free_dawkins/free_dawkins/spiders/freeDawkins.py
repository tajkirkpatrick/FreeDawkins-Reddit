import scrapy
from re import search
from datetime import datetime


class FreeDawkinsSpider(scrapy.Spider):
    name = 'freeDawkins'
    start_urls = ['https://www.freedawkins.com']

    def extractDateFromURL(self, article_url):
        """
        docstring
        """

        # ! ValueError,TypeError
        try:
            article_date_str = search(r'(?!\/)\d+(?=\/)', article_url)
            result = datetime.strptime(str(article_date_str[0]), '%Y%m%d').date()
            # result = result.date()
        except Exception:
            # TODO: Proper Error Handling
            result = 'ERR'
        
        return result

    def parse(self, response):
        """
        Docstring
        """


        # * SUCCESS - Get the Left-most featured video
        # for element in response.xpath('//*[@id="main"]/div/div/div/section[7]/div/div/div[1]'):

        #     article_url = element.xpath('.//*[contains(@class, "elementor-post__title")]/a/@href').get() 
        #     if article_url is not None:
        #         yield response.follow(article_url, self.ExtractPlayerPage)

            

        # * SUCCESS - Scrapes the entire "the new stuff table"
        for element in response.xpath('//*[@id="main"]/div/div/div/section[7]/div/div/div[2]'):
             for article in element.xpath('.//article/*[contains(@class, "elementor-post__text")]'):

                article_url = article.xpath('.//h1/a/@href').get()
                if article_url is not None:
                    yield response.follow(article_url, self.ExtractPlayerPage)

        # next_page = response.xpath('//*[@id="main"]/div/div/div/section[7]/div/div/div[2]/div/div/div/div/nav/*[contains(@class, "next")]/@href').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.pagination_parse)

    def pagination_parse(self, response):
        """
        Docstring
        """

        print("\nEND OLD PAGE\n")

        for element in response.xpath('//*[@id="main"]/div/div/div/section[7]/div/div/div[2]/div/div/div/div/div'):
            for article in element.xpath('.//*[contains(@class, "elementor-grid-item")]'):

                article_url = article.xpath('.//div/h1/a/@href').get()
                if article_url is not None:
                    yield response.follow(article_url, self.ExtractPlayerPage)
            
        next_page = response.xpath('//*[@id="main"]/div/div/div/section[7]/div/div/div[2]/div/div/div/div/nav/*[contains(@class, "next")]/@href').get()
        if next_page is not None:
            #yield response.follow(next_page, self.pagination_parse)
            pass


        print("START NEW PAGE\n")
        return
    
    def ExtractPlayerPage(self, response):
        """
        docstring
        """


        player_page_title = response.xpath('/html/body/div[1]/div/div/section[1]/div/div/div/div/div/div[1]/div/h1/text()').get().strip().encode('ascii', 'ignore').decode('ascii')
        player_page_performance_date = self.extractDateFromURL(response.url)

        try:
            youtube_identifier = response.xpath('/html/body/div[1]/div/div/section[1]/div/div/div/div/div/section/div/div/div/div/div/div[3]/div/div/div/div/section[1]/div/div/div/div/div/div[2]/div/div/iframe/@src').get()
            
            if youtube_identifier != None:
                youtube_identifier = search(r'(?!\/).+?(?=\?)', youtube_identifier)
                player_page_youtube_link = str(youtube_identifier[0])
            else:
                player_page_youtube_link = '%MANUAL ENTRY NEEDED%'

        except Exception:
            # TODO: Proper Error Handling
            pass

        
        yield {
            'title': player_page_title,
            'url': response.url,
            'performance_date': player_page_performance_date,
            'guessed_youtube_link' : player_page_youtube_link
        }
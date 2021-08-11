import scrapy
from ..items import CreditItem


class KarmaSpider(scrapy.Spider):
    name = 'karma'
    # allowed_domains = ['a']
    start_urls = ['https://www.creditkarma.com/reviews/personal-loan/single/id/upstart-personal-loans?pg=1']
    page_number = 1

    




    def parse(self, response):
        titles = response.xpath("//section[@id='top-of-reviews']")

        for review in titles:
            title = review.css('h5.f4.lh-title.ck-black-90.mb2.mt3::text').get()
            desc = review.css('p.f4.lh-copy.ma0::text').get()
            date = review.css('span.dib.f5.lh-copy span::text').get()
            likes = review.css('#top-of-reviews .hover-bg-ck-black-20:nth-child(1) span::text').get()
            dislikes = review.css('#top-of-reviews .hover-bg-ck-black-20:nth-child(1) span::text').get()

            items = CreditItem()
            items['title'] = title
            items['desc'] = desc
            items['date'] = date
            items['likes'] = likes
            items['dislikes'] = dislikes

            yield items

        pagination = response.xpath("//span[@class='v-mid dib pv2']/text()").get()
        default = 'No Reviews found'
        next_page = 'https://www.creditkarma.com/reviews/personal-loan/single/id/upstart-personal-loans?pg='+ str(KarmaSpider.page_number)

        if pagination != default:
            KarmaSpider.page_number +=1
            yield scrapy.Request(url=next_page, callback=self.parse)
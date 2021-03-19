import scrapy

from scrapy.loader import ItemLoader

from ..items import BankhausherzogparkdeItem
from itemloaders.processors import TakeFirst


class BankhausherzogparkdeSpider(scrapy.Spider):
	name = 'bankhausherzogparkde'
	start_urls = ['https://bankhaus-herzogpark.de/pressestimmen/pressespiegel/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="external-link-new-window"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		print(response.url[:39])
		if response.url[:39] != 'https://www.private-banking-magazin.de/':
			return
		title = response.xpath('//h1/text()[normalize-space()]').get()
		description = response.xpath('//p[@class="article-teaser c-black-tx"]//text()[normalize-space()]|//div[@class="article-parallax"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()[3:]

		item = ItemLoader(item=BankhausherzogparkdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

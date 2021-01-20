import re

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import PernikItem


class PernikSpider(scrapy.Spider):
	name = 'pernik'
	start_urls = ['http://pk.riosv-pernik.com/']

	def parse(self, response):
		posts = response.xpath('//div[@class="art-post-inner"]')[2:-3]
		for post in posts:
			yield self.parse_post(response, post)

		pagination_links = response.xpath('//div[@id="navigation"]/p/a[@title="Следваща"]/@href')
		yield from response.follow_all(pagination_links, self.parse)

	def parse_post(self, response, post):
		print(post)
		title = post.xpath('.//h2/text()').get().strip()
		date = post.xpath('.//div[@class="art-postheadericons art-metadata-icons"]/text()').getall()[1]
		date = date.split(', ')[1][:-2]
		description = post.xpath('.//div[@class="art-article"]/descendant-or-self::*/text()').getall()
		description = [self.remove_something(t) for t in description]
		description = " ".join(description).strip()

		item = ItemLoader(item=PernikItem(), response=response)
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

	@staticmethod
	def remove_something(t):
		regex1 = r'e-max.it: la strada del successo -->[\S\s]*?e-max.it: seo e posizionamento sui motori -->'
		regex2 = r'<!--[\S\s]*?-->'
		regex3 = r"'[\S\s]*?//-->"
		regex4 = r"\xa0"
		regex5 = r"var[\S\s]*?}"

		regex = [regex1, regex2, regex3, regex4, regex5]
		for reg in regex:
			t = re.sub(reg, '', t).strip()
		return t

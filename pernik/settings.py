BOT_NAME = 'pernik'

SPIDER_MODULES = ['pernik.spiders']
NEWSPIDER_MODULE = 'pernik.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'pernik.pipelines.PernikPipeline': 100,

}
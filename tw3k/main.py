from scrapy import cmdline

# Default language is en, 'zh-CN' is optional value
# ❯ scrapy crawl character -a l=zh-CN
cmdline.execute(f"scrapy crawl character".split())

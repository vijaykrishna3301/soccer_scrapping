import scrapy

class ymssoccer(scrapy.Spider):
    name = "ymssoccer"
    start_urls = [
        "https://www.ymssoccer.net/boys-teams/",
        "https://www.ymssoccer.net/girls-teams/"
    ]

    def parse(self, response):
        # Check which website we're scraping
        if "https://www.ymssoccer.net/boys-teams/" in response.url or "https://www.ymssoccer.net/boys-teams/" in response.url:
            rows = response.xpath('//*[@id="fl-post-4537"]/div/div/div[2]/div/div/div/div/div/div[2]/div/div/table//tr')

            for row in rows[1:]:  # Skip the header row
                yield {
                    "team_name": row.xpath("td[1]/text()").get(),
                    "age_group": row.xpath("td[2]/text()").get(),
                    "coach": row.xpath("td[3]/a/text() | td[3]/text()").get(),
                    "coach_profile": row.xpath("td[3]/a/@href").get(),
                    "email": row.xpath("td[4]/a/text()").get(),
                    "email_link": row.xpath("td[4]/a/@href").get(),
                }

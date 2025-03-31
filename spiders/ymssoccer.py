import scrapy
import json

class YmsSoccerSpider(scrapy.Spider):
    name = "ymssoccer"
    insta_ids = ['ymssoccer', 'fc_delco']
    
    start_urls = [
        "https://www.ymssoccer.net/boys-teams/",
        "https://www.ymssoccer.net/girls-teams/",
    ] + [f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}" for user in insta_ids]

    custom_headers = {
        "User-Agent": "Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)"  # Instagram App ID for API requests
    }

    def start_requests(self):
        """ Sends requests with proper headers for Instagram API """
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.custom_headers, callback=self.parse)

    def parse(self, response):
        """ Parses both soccer team details and Instagram followers count """
        data = {"players": [], "insta_count": []}

        if "ymssoccer.net" in response.url:
            data["players"] = self.parse_soccer(response)
        elif "i.instagram.com" in response.url:
            data["insta_count"] = self.parse_instagram(response)

        yield data

    def parse_soccer(self, response):
        """ Extracts soccer team data from the website """
        players = []
        rows = None

        if "boys-teams" in response.url:
            rows = response.xpath('//*[@id="fl-post-4537"]/div/div/div[2]/div/div/div/div/div/div[2]/div/div/table//tr')
        elif "girls-teams" in response.url:
            rows = response.xpath('//*[@id="fl-post-4535"]/div/div/div[2]/div/div/div/div/div/div[2]/div/div/table//tr')

        if rows:
            for row in rows[1:]:  # Skip the header row
                players.append({
                    "team_name": row.xpath("td[1]/text()").get(default="").strip(),
                    "age_group": row.xpath("td[2]/text()").get(default="").strip(),
                    "coach": row.xpath("td[3]/a/text() | td[3]/text()").get(default="").strip(),
                    "coach_profile": row.xpath("td[3]/a/@href").get(default=""),
                    "email": row.xpath("td[4]/a/text()").get(default=""),
                    "email_link": row.xpath("td[4]/a/@href").get(default=""),
                })

        return players

    def parse_instagram(self, response):
        """ Extracts Instagram followers count from API response """
        insta_count = []
        try:
            data = json.loads(response.text)
            user_data = data.get("data", {}).get("user", {})
            username = user_data.get("username", response.url.split("=")[-1])
            followers = user_data.get("edge_followed_by", {}).get("count", 0)

            self.logger.info(f"Extracted {followers} followers for {username}")
            insta_count.append({"id": username, "followers": followers})
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse Instagram response: {response.url}")

        return insta_count

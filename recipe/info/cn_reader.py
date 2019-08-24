# -*- coding:utf-8 -*-

import traceback
from bs4 import BeautifulSoup
from markdown import markdown

from action.info.recipe import InfoRecipe
from action.info.message import build_table
from steem.comment import SteemComment
from steem.collector import get_posts
from utils.system.date import get_zh_time_str
from utils.logging.logger import logger


# app specific parameter
RESTEEM_ACCOUNT = "rivalhw"
APP_URL = "https://busy.org"
# post configuration
INFO_ACCOUNT = "rivalhw"
CURATION_CYCLE = 1.01 # days
POST_TEMPLATE = """
steemit中文社区好文天天赞，{date}文章推荐，选出了如下共计**{count}篇**文章：

{table}


以上文章将获得本人转发推荐和点赞支持。

期待看到更多好文，大家一起加油！

每日推荐文章不做限制，同时给予选中的文章点赞鼓励，希望大家做的更好！

想参加每日好文点赞推荐活动的话，不妨可以看下如下相关文章：

《[寻找steemit平台上那些认真写作的优秀者](https://steemit.com/cn-reader/@rivalhw/scmuv-steemit)》

《[写在后边的话-寻找steemit平台上那些认真写作的优秀者](https://steemit.com/cn-reader/@rivalhw/2cqqm9-steemit)》

《[好文天天赞活动问题答疑](https://steemit.com/sct/@rivalhw/100-1559571827)》

"""


class CnReaderSummary(InfoRecipe):

    def mode(self):
        return "query.comment.post"

    def config(self):
        return {
            "account": RESTEEM_ACCOUNT,
            "days": CURATION_CYCLE,
            "reblog": True
        }

    def by(self):
        return INFO_ACCOUNT

    def data(self):
        data = super().data()
        # exclude the posts in yesterday's summary
        yesterday_posts = self.get_yesterday_posts()
        yesterday_authorperms = [SteemComment(url=url).get_author_perm() for url in yesterday_posts]
        data = [d for d in data if not d['authorperm'] in yesterday_authorperms]
        return data

    def title(self, data, days=None):
        return "好文天天赞{}榜上有名".format(get_zh_time_str(days))

    def body(self, data):
        # reverse the post orders
        data.reverse()
        date = get_zh_time_str()
        count = len(data)
        head = ["作者", "文章"]
        body = []
        for item in data:
            row = [
                "@" + item['author'],
                "<a href=\"{}\">{}</a>".format(self.get_url(item['authorperm']), item['title'])
            ]
            body.append(row)
        table = build_table(head=head, data=body)
        return POST_TEMPLATE.format(date=date, count=count, table=table)

    def tags(self, data):
        return ["cn-reader", "cn", "partiko", "zzan"]

    def ready(self, data):
        # post only there're more than 0 resteemed posts
        return data and len(data) > 0

    def get_url(self, authorperm):
        return APP_URL + "/" + authorperm

    def get_yesterday_posts(self):
        title = self.title(data=None, days=-1)
        posts = get_posts(account=RESTEEM_ACCOUNT, days=2)
        yesterday_summary_posts = [p for p in posts if p.title == title]
        if yesterday_summary_posts and len(yesterday_summary_posts) > 0:
            yesterday_summary_post = yesterday_summary_posts[0]
            try:
                html = markdown(yesterday_summary_post.body)
                soup = BeautifulSoup(html, 'lxml')
                tags = soup.select("tbody tr td a")
                return [t["href"] for t in tags]
            except:
                logger.info("Failed when parsing posts, with error: {}".format(traceback.format_exc()))
        return []

# -*- coding:utf-8 -*-

import sys
from steem.account import SteemAccount
from action.vote.recipe import VoteRecipe
from utils.logging.logger import logger

# app specific parameter
RESTEEM_ACCOUNT = "rivalhw"
# voter configuration
VOTER_ACCOUNT = "rivalhw"
VOTER_ACCOUNT2 = "cn-reader"
VOTE_TIMING = 1 # mins
CURATION_CYCLE = 1.01 # days
VOTE_PERCENTAGE = 1.0 # x% of daily 20% vote percentage
UPVOTE_LIMIT = 50 # %


class CnReaderVoter(VoteRecipe):

    def __init__(self):
        super().__init__()
        # self.authors = {}
        self.posts_num = 0
        self.voted_posts = 0
        self.curator = SteemAccount(self.by())
        self.followings = self.curator.get_followings()

    def mode(self):
        return "query.comment.post"

    def config(self):
        return {
            "account": RESTEEM_ACCOUNT,
            "days": CURATION_CYCLE,
            "reblog": True
        }

    def by(self):
        return VOTER_ACCOUNT

    def what_to_vote(self, ops):
        if not self.ops.is_upvoted_by(self.by()):
            logger.info("We will vote the post {}".format(self.ops.get_url()))
            self.posts_num += 1
            return True
        return False

    def who_to_vote(self, author):
        if not author in self.followings:
            self.curator.follow(author)
            logger.info("follow the new author @{}".format(author))
            self.followings.append(author)
        return True

    def when_to_vote(self, ops):
        return VOTE_TIMING # mins

    def how_to_vote(self, post):
        self.voted_posts += 1
        logger.info("voting {} / {} posts".format(self.voted_posts, self.posts_num))
        weight = self.voter.estimate_vote_pct_for_n_votes(days=CURATION_CYCLE, n=self.posts_num) * VOTE_PERCENTAGE
        if weight  > UPVOTE_LIMIT:
            weight = UPVOTE_LIMIT
        return weight

    def self_vote(self):
        return True

    def after_success(self, res):
        if self.voted_posts == self.posts_num:
            logger.info("Done with voting. Exit.")
            sys.exit()

class CnReaderVoter2(CnReaderVoter):

    def by(self):
        return VOTER_ACCOUNT2

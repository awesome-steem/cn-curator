# -*- coding:utf-8 -*-

import sys
from steem.comment import SteemComment
from action.vote.recipe import VoteRecipe
from utils.logging.logger import logger

# app specific parameter
TRIBE_TAG = "cn"
RESTEEM_ACCOUNT = "rivalhw"
# voter configuration
VOTER_ACCOUNT = "cn-reader"
VOTE_TIMING = 5 # mins
VOTE_CYCLE = 1.05 # 1.05 # days
VOTE_PERCENTAGE = 1
VOTE_PER_ACCOUNT_LIMIT = 2

class CnReaderVoter(VoteRecipe):

    def __init__(self):
        super().__init__()
        # self.authors = {}
        self.posts_num = 0
        self.voted_posts = 0

    def mode(self):
        return "query.resteem"

    def config(self):
        return {
            "account": RESTEEM_ACCOUNT
        }

    def by(self):
        return VOTER_ACCOUNT

    def what_to_vote(self, ops):
        self.posts_num += 1
        return False

    def who_to_vote(self, author):
        return True

    def when_to_vote(self, ops):
        return VOTE_TIMING # mins

    def how_to_vote(self, post):
        self.voted_posts += 1
        logger.info("voting {} / {} posts".format(self.voted_posts, self.posts_num))
        return self.voter.estimate_vote_pct_for_n_votes(days=VOTE_CYCLE, n=self.posts_num) * VOTE_PERCENTAGE

    def after_success(self, res):
        if self.voted_posts == self.posts_num:
            logger.info("Done with voting. Exit.")
            sys.exit()

# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import time
from libcontractvm import Wallet, ConsensusManager, DappManager

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)

	def listPost (self):
		return self.consensusManager.jsonConsensusCall ('forum.listPost', [])['result']
		
	def getPostInfo (self, postID):
		return self.consensusManager.jsonConsensusCall ('forum.getPostInfo', [postID])['result']

	def createPost (self, title, body):
		cid = self.produceTransaction ('forum.createPost', [title, body])
		return cid

	def commentPost (self, postID, comment):
		cid = self.produceTransaction ('forum.commentPost', [postID, comment])
		return cid

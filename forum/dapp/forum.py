# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from contractvmd import config, dapp, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)

class ForumProto:
	DAPP_CODE = [ 0x57, 0x58 ]
	METHOD_CREATE_POST = 0X01
	METHOD_COMMENT_POST = 0X02
	METHOD_LIST = [METHOD_CREATE_POST, METHOD_COMMENT_POST]


class ForumMessage (message.Message):
	def createPost (title, body):
		m = ForumMessage ()
		m.title = title
		m.body = body
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_CREATE_POST
		return m
		
	def commentPost (postID, comment):
		m = ForumMessage ()
		m.postID = postID
		m.comment = comment
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_COMMENT_POST
		return m
		
	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()
		
		if self.Method == ForumProto.METHOD_CREATE_POST:
			data['title'] = self.title
			data['body'] = self.body
		elif self.Method == ForumProto.METHOD_COMMENT_POST:
			data['postID'] = self.postID
			data['comment'] = self.comment
		else:
			return None
			
		return data



class ForumCore (dapp.Core):
	postCounter = 0

	def __init__ (self, chain, database):
		database.init ('forums', [])
		database.init ('comments', [])
		super (ForumCore, self).__init__ (chain, database)
		
	def createPost (self, title, body):
		msg = ForumMessage.createPost (title, body)
		postID = ForumAPI.createTransactionResponse (msg)
		self.database.listappend ('forums', {'PostID': postID, 'title': title, 'body': body})
		return postID
		
	def listPost (self):
		return self.database.get ('forums')
	
	def getPostInfo (self, postID):
	    info = []
	    v = self.database.get ('forums')
	    for x in v:
	        if x['PostID'] == postID:
	            info.append(x)
	    comments = []
	    v = self.database.get ('comments')
	    for x in v:
	        if x['PostID'] == postID:
	            comments.append(x['comment'])
	    info.append(comments)
	    return info
		
	def commentPost (self, postID, comment):
	    msg = ForumMessage.commentPost (postID, comment)
	    commentID = ForumAPI.createTransactionResponse (msg)
	    self.database.listappend ('comments', {'CommentID': commentID, 'PostID': postID, 'comment':comment})
	    return commentID



class ForumAPI (dapp.API):
	def __init__ (self, core, dht, api):
		self.api = api
		rpcmethods = {}
		
		rpcmethods["createPost"] = {"call": self.method_createPost, "help": {"args": ["title", "body"], "return": {}} }
		rpcmethods["commentPost"] = {"call": self.method_commentPost, "help": {"args": ["postID", "comment"], "return": {}} }
		rpcmethods["listPost"] = {"call": self.method_listPost, "help": {"args": [], "return": {}} }
		rpcmethods["getPostInfo"] = {"call": self.method_getPostInfo, "help": {"args": ["postID"], "return": {}} }
		errors = {}
		
		super (ForumAPI, self).__init__(core, dht, rpcmethods, errors)
	def method_listPost (self):
		return self.core.listPost ()
	def method_getPostInfo (self, postID):
		return self.core.getPostInfo (postID)
	def method_createPost (self, title, body):
		msg = ForumMessage.createPost (title, body)
		return self.createTransactionResponse (msg)
	def method_commentPost (self, postID, comment):
		msg = ForumMessage.commentPost (postID, comment)
		return self.createTransactionResponse (msg)

class forum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apiMaster):
		self.core = ForumCore (chain, db)
		apiprov = ForumAPI (self.core, dht, apiMaster)		
		super (forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, apiprov)
		

	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_CREATE_POST:
			logger.pluginfo ('Found new post => %s: %s', m.Data['title'], m.Data['body'])
			self.core.createPost (m.Data['title'], m.Data['body'])
		elif m.Method == ForumProto.METHOD_COMMENT_POST:
			logger.pluginfo ('Found new comment for post %s => %s', m.Data['postID'], m.Data['comment'])
			self.core.commentPost (m.Data['postID'], m.Data['comment'])			
		

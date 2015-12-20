import logging

from contractvmd import dapp, config, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)


class ForumProto:
   DAPP_CODE = [ 0x01, 0x04 ]
   METHOD_POST = 0x05
   METHOD_COMMENT = 0x06
   METHOD_GETPOST = 0x07
   METHOD_LIST = [METHOD_POST, METHOD_COMMENT, METHOD_GETPOST]



class ForumMessage(message.Message):

   # Create post message, must have a title and the body of the post
   def createPost(title, body):
      m = ForumMessage()
      m.Title = title
      m.Body = body
      m.DappCode = ForumProto.DAPP_CODE
      m.Method = ForumProto.METHOD_POST
      return m


   # Create comments message, must have the ID of the post and the comment
   def createComment(postID, comment):
      m = ForumMessage()
      m.PostID = postID
      m.Comments = comment
      m.DappCode = ForumProto.DAPP_CODE
      m.Method = ForumProto.METHOD_COMMENT
      return m


   def toJSON(self):
      data = super(ForumMessage, self).toJSON ()

      if self.Method == ForumProto.METHOD_POST:
         data['title'] = self.Title
         data['body'] = self.Body
      elif self.Method == ForumProto.METHOD_COMMENT:
         data['postID'] = self.PostID
         data['comments'] = self.Comments
      else:
         return None

      return data


class ForumCore(dapp.Core):
   def __init__(self, chain, database):
      database.init('posts', [])
      super(ForumCore, self).__init__(chain, database)

   # Create a new post provided a title and a body
   def createPost(self, postID, title, body):
      self.database.listappend('posts', {'postID': postID, 'title': title, 'body': body, 'comments': []})


   # Create a new comment provided a postID(the post you want to comment), and the comment 
   def createComment(self, postID, comment):
      db = self.database.get('posts')
      for p in db:
         if postID == p['postID']:
            p['comments'].append(comment)
            self.database.set('posts', db)


   # Give informations about a single post
   def getPost(self, postID):
      db = self.database.get('posts')
      for p in db:
         if postID == p['postID']:
            return p

   # List all posts in the database
   def getlist(self):
      return self.database.get('posts')


class ForumAPI(dapp.API):
   def __init__(self, core, dht, api):
      self.api = api
      rpcmethods = {}

      rpcmethods["getlist"] = {
            "call": self.method_getlist,
            "help": {"args": [], "return": {}}
      }

      rpcmethods["getPost"] = {
            "call": self.method_get_post,
            "help": {"args": ["postID"], "return": {}}
      }

      rpcmethods["createPost"] = {
         "call": self.method_create_post,
         "help": {"args": ["title", "body"], "return": {}}
      }

      rpcmethods["createComment"] = {
         "call": self.method_create_comment,
         "help": {"args": ["postID", "comment"], "return": {}}
      }

      errors = { }

      super(ForumAPI, self).__init__(core, dht, rpcmethods, errors)


   # Call self.core.getlist()
   def method_getlist(self):
      return self.core.getlist()

   # Call self.core.getPost(postID)
   def method_get_post(self, postID):
      return self.core.getPost(postID)

   # Build the createPost message and the transaction
   def method_create_post(self, title, body):
      msg = ForumMessage.createPost(title, body)
      return self.createTransactionResponse(msg)

   # Build the createComment message and the transaction
   def method_create_comment(self, postID, comment):
      msg = ForumMessage.createComment(postID, comment)
      return self.createTransactionResponse(msg)



class forum(dapp.Dapp):
   def __init__(self, chain, db, dht, apiMaster):
      self.core = ForumCore(chain, db)
      apiprov = ForumAPI(self.core, dht, apiMaster)
      super(forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, apiprov)

   def handleMessage(self, m):
      if m.Method == ForumProto.METHOD_POST:
         logger.pluginfo('Found new post %s: %s', m.Hash, m.Data['title'])
         self.core.createPost(m.Hash, m.Data['title'], m.Data['body'])
      elif m.Method == ForumProto.METHOD_COMMENT:
         logger.pluginfo('Found new comment on post %s', m.Data['postID'])
         self.core.createComment(m.Data['postID'], m.Data['comments'])

from libcontractvm import Wallet, ConsensusManager, DappManager

class ForumManager(DappManager.DappManager):
   def __init__(self, consensusManager, wallet = None):
      super(ForumManager, self).__init__(consensusManager, wallet)

   def createPost(self, title, body):
      cid = self.produceTransaction('forum.createPost', [title, body])
      return cid

   def createComment(self, postID, comment):
      cid = self.produceTransaction('forum.createComment', [postID, comment])
      return cid

   def getList(self):
      return self.consensusManager.jsonConsensusCall('forum.getlist', [])['result']

   def getPost(self, postID):
      return self.consensusManager.jsonConsensusCall('forum.getPost', [postID])['result']


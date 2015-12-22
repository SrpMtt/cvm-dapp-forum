from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager()
consMan.bootstrap("http://127.0.0.1:8181")


walletA = WalletExplorer.WalletExplorer(wallet_file='A.wallet')
walletB = WalletExplorer.WalletExplorer(wallet_file='B.wallet')
fManA = ForumManager.ForumManager(consMan, wallet=walletA)
fManB = ForumManager.ForumManager(consMan, wallet=walletB)


# A creates a new post
postid = fManA.createPost('Hello post', 'test post')
consMan.waitBlock()

# A gets the posts list
fManA.getList()       
time.sleep(10)

# A comments his post                                                           
commid = fManA.createComment(postid, 'This is a comment')
consMan.waitBlock()

# A gets post info
fManA.getPost(postid)
time.sleep(10)

# B creates a new post
postid2 = fManB.createPost('Hello post 2', 'test post 2')
time.sleep(10)

# B comments A's post
commid2 = fManB.createComment(postid, 'This is a comment of B')
consMan.waitBlock()

# B gets posts list
while True:
   os.system('clear')
   print('Post list:')
   posts = fManB.getList()
   for p in posts:
      print('PostID:', p['postID'], '\nTitle:', p['title'], '\nBody:', p['body'], '\nComments:', p['comments'], '\n')
   time.sleep(10)

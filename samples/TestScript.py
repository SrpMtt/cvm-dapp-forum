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
try:
   print('A posted: ', fManA.createPost('Hello post', 'test post'))
except:
   print('Error post A')
   

time.sleep(10)


# A gets the posts list
while True:
   os.system('clear')
   print('Post list:')
   posts = fManA.getList()
   for p in posts:
      print('PostID:', p['postID'], '\nTitle:', p['title'], '\nBody:', p['body'], '\nComments:', p['comments'], '\n')
   wait = input('Refresh list? (y/n): ')
   if wait == 'y':
      pass
   else:
      break


time.sleep(10)


# A comments his post
try:
   postid = input('Insert post ID: ')
   print('A commented: ', fManA.createComment(postid, 'This is a comment'))
except:
   print('Error comment A')


time.sleep(10)


# A gets post info
while True:
   os.system('clear')
   print('Post info:')
   posts = fManA.getList()
   for p in posts:
      print('PostID:', p['postID'], '\nTitle:', p['title'], '\nBody:', p['body'], '\nComments:', p['comments'], '\n')
   wait = input('Refresh list? (y/n): ')
   if wait == 'y':
      pass
   else:
      fManA.getPost(input('Enter post ID: '))
      break


time.sleep(10)


# B creates a new post
try:
   print('B posted: ', fManB.createPost('Hello post 2', 'Post di test 2'))
except:
   print('Error post B')


time.sleep(10)


# B comments A's post
try:
   postid = input('Insert post ID: ')
   print('B commented: ', fManB.createComment(postid, 'This is a comment of B'))
except:
   print('Error comment B')


time.sleep(10)


# B gets posts list
while True:
   os.system('clear')
   print('Post list:')
   posts = fManB.getList()
   for p in posts:
      print('PostID:', p['postID'], '\nTitle:', p['title'], '\nBody:', p['body'], '\nComments:', p['comments'], '\n')

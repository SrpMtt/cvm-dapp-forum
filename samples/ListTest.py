from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os

consMan = ConsensusManager.ConsensusManager()
consMan.bootstrap("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer(wallet_file='test.wallet')
fMan = ForumManager.ForumManager(consMan, wallet=wallet)

while True:
   os.system('clear')
   print('Post list:')
   v = fMan.getList()
   for x in v:
      print('PostID:', x['postID'], '\nTitle:', x['title'], '\nBody:', x['body'], '\nComments:', x['comments'], '\n')
   time.sleep(5)

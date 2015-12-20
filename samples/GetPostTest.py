from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time
import os


consMan = ConsensusManager.ConsensusManager()
consMan.bootstrap("http://127.0.0.1:8181")
wallet = WalletExplorer.WalletExplorer(wallet_file='test.wallet')
fMan = ForumManager.ForumManager(consMan, wallet=wallet)

pID = input('Insert post ID: ')

print('Post info:\n')
try:
   x = fMan.getPost(pID)
   print('PostID:', x['postID'], '\nTitle:', x['title'], '\nBody:', x['body'], '\nComments:', x['comments'], '\n')
except:
   print('Error.')

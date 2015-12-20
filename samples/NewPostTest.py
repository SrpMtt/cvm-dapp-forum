from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager()
consMan.bootstrap("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer(wallet_file='test.wallet')
fMan = ForumManager.ForumManager(consMan, wallet=wallet)

tit = input('Insert post title: ')
bod = input('Insert post body: ')

try:
   print('Broadcasted:', fMan.createPost(tit, bod))
except:
   print('Error.')

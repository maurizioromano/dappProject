from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys, time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

walletA = WalletExplorer.WalletExplorer (wallet_file='testA.wallet')
walletB = WalletExplorer.WalletExplorer (wallet_file='testB.wallet')
AMan = ForumManager.ForumManager (consMan, wallet=walletA)
BMan = ForumManager.ForumManager (consMan, wallet=walletB)

#A
postid = AMan.createPost ('Hello post', 'Post di test')
print ('POST -> ', postid)

time.sleep(5)

v = AMan.listPost()
print ('Posts List:')
for x in v:
    print ('\t', x['PostID'])

commid = AMan.commentPost (postid, 'This is a comment')
print ('COMMENT -> ', commid)

time.sleep(5)

print(AMan.getPostInfo(postid))

#B
postid2 = BMan.createPost ('Hello post2', 'Post di test2')
print ('POST -> ', postid2)
commid2 = BMan.commentPost (postid2, 'This is a comment of B')
print ('COMMENT -> ', commid2)

time.sleep(10)

print(BMan.getPostInfo(postid2))
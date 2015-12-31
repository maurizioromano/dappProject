from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
srMan = ForumManager.ForumManager (consMan, wallet=wallet)

while True:
    operazione = input('DAPP PROJECT MAURIZIO ROMANO\n1.CreatePost (title, body)\n2.CommentPost (postID, comment)\n3.Get Forum List\n4.Get Post info (postID)\nScegli l\'operazione da fare: ')

    if operazione == '1':
        title = input('Inserisci il titolo: ')
        body = input('Inserisci il body: ')
        try:
            print ('Broadcasted:', srMan.createPost (title, body))
        except:
            print ('createPost Error.')
    elif operazione == '2':
        postID = input('Inserisci il postID: ')
        comment = input('Inserisci il commento: ')
        try:
            print ('Broadcasted:', srMan.commentPost (postID, comment))
        except:
            print ('AddComment Error.')
    elif operazione == '3':
        print ('Posts List:')
        v = srMan.listPost()
        for x in v:
            print ('\t', x['PostID'])
    elif operazione == '4':
        postID = input('Inserisci il postID: ')
        print(srMan.getPostInfo(postID))  

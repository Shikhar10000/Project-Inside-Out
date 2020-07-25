import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('insideout-d7b9f-917ca2d27c46.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def fs(score,timestamp,channel):


	try:
		doc_ref = db.collection(channel).document(str(timestamp))
		doc_ref.set({u'score':str(score)}) 
		doc_ref_ = db.collection(channel).document(str(u'last'))
		doc_ref_.set({u'score':str(score)})
	except:
		pass
		

def read(channel):

	users_ref = db.collection(channel)
	docs = users_ref.stream()

	for doc in docs:
		print(u'{} => {}'.format(doc.id, doc.to_dict()))


def read_last(channel):

	users_ref = db.collection(channel).document(str(u'last'))
	doc = users_ref.get()

	dic=doc.to_dict()
	return dic['score']

	
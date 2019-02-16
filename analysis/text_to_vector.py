from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models import Doc2Vec
from gensim.models.keyedvectors import Doc2VecKeyedVectors

doc_model = None

def load_doc_model (fname):
    global doc_model
    doc_model = Doc2Vec.load(fname)

def infer (text):
    if doc_model is None:
        raise Exception("Document 2 Vector model not initalized!  Call .load_doc_model(FILE_NAME) to initialize it")
    return doc_model.infer_vector(text) 

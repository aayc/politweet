import sys
sys.path.append('../analysis/')

import text_to_vector

def test_model_load ():
    print("TESTING LOADING MODEL FROM /analysis/doc_models/enwiki_dbow/doc2vec.bin")
    try:
        text_to_vector.load_doc_model("../analysis/doc_models/enwiki_dbow/doc2vec.bin")
        text_to_vector.infer("hey how's it going".split(" "))
        print("TEST SUCCESS")
    except:
        print("TEST FAILED")

if __name__ == "__main__":
    test_model_load()



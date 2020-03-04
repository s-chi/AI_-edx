from glob import glob
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

train_path = "../resource/lib/publicdata/aclImdb/train/"
test_path = "../resource/lib/publicdata/imdb_te.csv" 


def imdb_data_preprocess(inpath, testpath, outpath="./", nametr="imdb_tr.csv", namete="imdb_te.csv"):
    
    with open("stopwords.en.txt",'r') as f:
        
        stops = f.readlines()
    
    stops = [x.strip() for x in stops]
    stops.append('br')
    
    veccer = CountVectorizer(stop_words = stops, encoding='latin-1')
    prepro = veccer.build_preprocessor()
    toke = veccer.build_tokenizer()
    ana = veccer.build_analyzer()
        
    with open(outpath + nametr, 'w') as outfile:
        
        outfile.write(",text,polarity\n")
        ind = 0
        
        for f in glob(inpath + "pos/*"):
            
            with open (f,'r') as infile:
                
                string = infile.read()
                strlist2 = ana(string)
                string = ' '.join(strlist2)
                string = string.encode('utf-8')
                outfile.write('%s,\"%s\",%s\n' % (ind,string,1))
                
            ind += 1
                
        for f in glob(inpath + "neg/*"):
            
            with open (f,'r') as infile:
                
                string = infile.read()
                strlist2 = ana(string)
                string = ' '.join(strlist2)
                string = string.encode('utf-8')
                outfile.write("%s,\"%s\",%s\n" % (ind,string,0))
                
            ind +=1
            
    with open(outpath + namete, 'w') as outfile:
        
        outfile.write(",text\n")
        ind = 0
            
        df = pd.read_csv(testpath,index_col = 0)
        values = df.values
        lines = values[:,0]        
        
        for line in lines:
            
            string = line.strip()                
            strlist2 = ana(line)
            string = ' '.join(strlist2)
            string = string.encode('utf-8')
            outfile.write('%s,\"%s\"\n' % (ind,string))
        
            ind += 1
                
  
if __name__ == "__main__":

    imdb_data_preprocess(train_path, test_path)
    
    df = pd.read_csv("imdb_tr.csv",index_col = 0)
    values = df.values

    textarray = values[:,0]
    y_train = values[:,1]
    y_train = y_train.astype(int)
    
    
    df = pd.read_csv("imdb_te.csv",index_col = 0)
    
    values = df.values
    textarray2 = values[:,0]
    
    
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(textarray)
    
    clf = SGDClassifier(loss = 'hinge', penalty = 'l1', max_iter = 100, alpha = 0.00000001)
    clf.fit(X_train, y_train)
    
    X_test = vectorizer.transform(textarray2)
    
    Z = clf.predict(X_test)
    
    with open("unigram.output.txt",'w') as out:
        
        Z.tofile(out,"\n")
        out.write("\n")
    
    
    vectorizer2 = CountVectorizer(ngram_range = (1, 2))
    X_train2 = vectorizer2.fit_transform(textarray)
    
    clf2 = SGDClassifier(loss = 'hinge', penalty = 'l1', max_iter = 100, alpha = 0.000000001)
    clf2.fit(X_train2, y_train)
    
    X_test2 = vectorizer2.transform(textarray2)
    
    Z2 = clf2.predict(X_test2)
    
    with open("bigram.output.txt",'w') as out:
        
        Z2.tofile(out,"\n")
        out.write("\n")
    
    
    vectorizerT = TfidfVectorizer()
    X_trainT = vectorizerT.fit_transform(textarray)
    
    clfT = SGDClassifier(loss = 'hinge', penalty = 'l1', max_iter = 100, alpha = 0.00003)
    clfT.fit(X_trainT, y_train)
    
    X_testT = vectorizerT.transform(textarray2)
    
    ZT = clfT.predict(X_testT)
    
    with open("unigramtfidf.output.txt",'w') as out:
        
        ZT.tofile(out,"\n")
        out.write("\n")
    
    vectorizerT2 = TfidfVectorizer(ngram_range = (1, 2))
    X_trainT2 = vectorizerT2.fit_transform(textarray)
    
    clfT2 = SGDClassifier(loss = 'hinge', penalty = 'l1', max_iter = 100, alpha = 0.00000004)
    clfT2.fit(X_trainT2, y_train)
    
    X_testT2 = vectorizerT2.transform(textarray2)
    
    ZT2 = clfT2.predict(X_testT2)
    
    with open("bigramtfidf.output.txt",'w') as out:
        
        Z.tofile(out,"\n")
        out.write("\n")
    
    

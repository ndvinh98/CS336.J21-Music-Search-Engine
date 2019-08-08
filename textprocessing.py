import unicodedata
from string import punctuation
from underthesea import word_tokenize
import math
from collections import Counter



def caculate_tf(freq):
  '''tính TF'''
  return (1+ math.log(freq)) #freq là số lần term cần tính xuất hiện trong 1 document

def caculate_idf(df,N):
  '''Tính IDF'''
  return (math.log((N/df))) # N là số lượng document, df là số lần term cần tính xuất hiện trong các document

def remove_accents(text):
    '''loại bỏ kí tự unicode có trong "text", trả về 1 string'''
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    no_accents_text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
    return no_accents_text.replace('đ', 'd')

def textprocessing(document):
  '''Xử lí chuỗi "document", loại bỏ dấu câu, trả về 1 list '''
  punc = list(punctuation) #list dấu câu
  text_processing=[]
  sent = []
  for word in document.split(" ") :
            if (word not in punc) :
                if ("_" in word) or (word.isalpha() == True):
                    word=remove_accents(word)
                    sent.append(word)
  text_processing.extend(" ".join(sent).split())
  return text_processing

def caculate_query_weight(query,inv_index,N):
  '''tính trọng số của câu truy vấn, loại bỏ các từ không có trong inverted_index , 
  "query" là câu truy vấn, 
  "inv_index" là list inverted index, 
  N là số docID,
  trả về 1 dict đã được tính trọng số cho mỗi  từ
  '''
  list_query=dict()
  for idx,term in enumerate(query):
    c=Counter(query)
    freq=c[term]
    if term in inv_index.keys():
      df=inv_index[term]['df']
      if list_query.get(term,None) is None:
        list_query[term]= caculate_tf(freq)*caculate_idf(df,N)
  return list_query

def normalize_query(list_query):
  query_length = math.sqrt(sum((e ** 2 for e in list_query.values())))
  for term, query_weight in list_query.items():
      list_query[term] = query_weight / query_length
  return list_query

def queryprocessing(inverted_index,document):
  sent = []
  query_processing=[]
  for word in document.split(" ") :
            word=remove_accents(word)
            word=word.lower()
            if (word in inverted_index.keys()) :
                    sent.append(word)
  query_processing.extend(" ".join(sent).split())
  return query_processing

def caculate_score(list_query,inv_index,N,lengths_doc):
  '''tính score và xếp hạng câu truy vấn'''
  scores = [[i, 0] for i in range(N)]
  for term, query_weight in list_query.items():

      if term in inv_index.keys():
        df = inv_index[term]['df']
        postings_list = inv_index[term]['postings_list']

        for docId, freq in postings_list.items():
          doc_weight = (caculate_tf(freq)*caculate_idf(df,N))
          scores[docId][1] += query_weight * doc_weight / lengths_doc[docId]
  scores.sort(key=lambda e: e[1], reverse=True)
  return scores
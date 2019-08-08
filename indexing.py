import glob
from collections import defaultdict
import json
from textprocessing import textprocessing, caculate_idf, caculate_tf, remove_accents
from underthesea import word_tokenize
from collections import Counter
import math


def load_data(name,link,lyric,name_processed,lyric_processed):
  '''Load data và lưu vào các list truyền vào với:
  "name": danh sách tên bài hát |||
  "link" danh sách link bài hát tương ứng |||
  "lyric" danh sách lời bài hát tương ứng |||
  "name_processed", "lyric_processed" là list tên bài hát, lời bài hát cần xử lí văn bản như tách từ, loại bỏ dấu câu, chuẩn hóa chữ thường...
  "N" là số docId
  '''
  paths = glob.glob("./crawl/data/*.json")
  data = dict()
  for path in paths :
    with open(path) as file:
        data=json.load(file)
        name.append(data['name']) #lưu tên bài hát vào list name
        link.append(data['link']) #lưu link bài hát vào list link
        lyric.append(data['lyric']) #lưu lời bài hát vào list lyric

        #xử lí tên bài hát 
        text_lower=data['name'].lower() #chuẩn hóa chữ hoa thành thường
        text_token =textprocessing(word_tokenize(text_lower, format='text')) #tách từ 
        name_processed.append(text_token) #lưu các từ có trong tên bài hát đã xử lí vào list name_processed

        #xử lí lời bài hát
        text_lower=data['lyric'].lower() #chuẩn hóa chữ hoa thành thường
        text_token =textprocessing(word_tokenize(text_lower, format='text')) #tách từ 
        lyric_processed.append(text_token) #lưu các từ có trong tên bài hát đã xử lí vào list lyric_processed

def build_json_data(list_names,list_links,list_lyrics,path):
    '''Lưu tất cả dữ liệu thành 1 file json có cấu trúc như sau: {'list_name[i]':{ 'data' : { list_links[i] : list_lyrics[i] } } } };
       với i chạy từ 0~ len(list_name)
       list_name: Danh sách các bài hát;
       list_links: là Danh sách các link bài hát tương ứng;
       list_lyrics: là Danh sách các lời bài hát tương ứng;
       path: là đường dẫn+tênfile.json để lưu file
    '''
    dataset=dict()
    for index in range (len(list_names)):
        if dataset.get(list_names[index], None) is None:
            dataset[list_names[index]] = {}
        if dataset[list_names[index]].get('data',None) is None:
            dataset[list_names[index]]['data']={}
        dataset[list_names[index]]['data'][list_links[index]]=list_lyrics[index]

    with open(path, "w",encoding='UTF8') as file_write:
        json.dump(dataset, file_write)
    with open('./data/original_names.json', "w",encoding='UTF8') as file_write:
        json.dump(list_names, file_write)
    
def inverted_index(list_data,path):
  '''truyền vào "list_data" là list dữ liệu cần xây dựng inverted index và "path" là đường dẫn+ tênfile.json để lưu, trả về list inverted index'''
  inv_index=dict()
  for index, text in enumerate(list_data):
    c=Counter(text) # c lưu tần số suất hiện của các phần tử có trong text. VD text={'anh','yêu','em','của','em'} thì c={'anh':1 ; 'yêu':1 ; 'em':2 ; 'của':1}
    for key, value in c.items():
            if inv_index.get(key, None) is None:
                inv_index[key] = {}
            if inv_index[key].get('df', None) is None:
                inv_index[key]['df'] = 0

            if inv_index[key].get('postings_list', None) is None:
                inv_index[key]['postings_list'] = {}  
             
            inv_index[key]['df'] += 1

            inv_index[key]['postings_list'][index] = value

  with open(path, "w") as file_write:
    json.dump(inv_index, file_write)
  return inv_index

def lengths(inverted_index,path,N):
  ''' trả về một danh sách các lengths tính được cho mỗi vector văn bản tương ứng, 
  nếu truyền vào list inverted_index của lyrics thì nó trả về list lengths của lyrics tương ứng với docID,
  nếu truyền vào list inverted_index của names thì nó trả về list lengths của name ứng với docID, VD docID 10 có lengths là lengths[10],
  "N" là số phần tử của lengths = số docID,
  "path" là đường dẫn+teenffile.json để lưu 
  '''
  lengths_doc=dict()
  for index in range(N):
    vector = []
    for key, value in inverted_index.items():
        df = value['df']
        postings_list = value['postings_list']

        if index in postings_list.keys():
            weight =caculate_tf(postings_list[index])*caculate_idf(df,N)
            vector.append(weight)

    lengths_doc[index] = math.sqrt(sum((e ** 2 for e in vector)))

  with open(path, "w") as file_write:
    json.dump(lengths_doc, file_write)


names=[]
names_processed=[]
links=[]
lyrics=[]
lyrics_processed=[]


print("Đang Load Data....")
load_data(names,links,lyrics,names_processed,lyrics_processed)

print("Đang Duild Data...")
build_json_data(names,links,lyrics,"./data/original_datasets.json")
inverted_index_lyrics=inverted_index(lyrics_processed,"./data/Inverted_Index_Lyrics.json")
inverted_index_names=inverted_index(names_processed,"./data/Inverted_Index_Names.json")
lengths(inverted_index_lyrics,"./data/Lengths_Lyrics.json",len(lyrics))
lengths(inverted_index_names,"./data/Lengths_Names.json",len(names))

print("Hoàn thành!")



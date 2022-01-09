from elasticsearch import Elasticsearch , helpers

# db 이름 설정
INDEX_NAME = "news_wiki_index_update"

# db 셋팅
INDEX_SETTINGS = {
"settings" : {
    "index":{
    "analysis":{
        "analyzer":{
        "korean":{
            "type":"custom",
            "tokenizer":"nori_tokenizer",
            "filter": [ "shingle" ],

        }
        }
    }
    }
},
"mappings": {

    "properties" : {
        
        "admin_id" : {
        "type" : "keyword",
        },
        
        "category" : {
        "type" : "keyword",
        },
        
        "date" : {
        "type" : "date"
        },
        
        "title" : {
        "type" : "keyword",
        },
        
        "article" : {
        "type" : "text"
        },
        
        "context" : {
        "type" : "text",
        "analyzer": "korean",
        "search_analyzer": "korean"
        }
        
    }

}
}

# 뉴스 기사 목록 불러오기
class Homeboard():
    def __init__(self) :
        try:
            es.transport.close()
        except:
            pass
        self.es = Elasticsearch()
        if not self.es.indices.exists(INDEX_NAME) :
            raise Exception("INDEX {0} not exists".format(INDEX_NAME))
            exit()
        
        # self.query = "사랑하지만 힘들어 죽겠네"
    # 뉴스 기사 제목 리스트 불러오기
    def get_news_title(self , query = "사랑하지만 힘들어 죽겠네") :
        res = self.es.search(index=INDEX_NAME, q=query, size=5)
        return res
    
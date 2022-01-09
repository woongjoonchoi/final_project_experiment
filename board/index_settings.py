INDEX_NAME = "mbn_index2"


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
        "CONTEXT" : {
          "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        },
        "TITLE" : {
          "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        },
        "DATE" :{
            "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        },
        "CATEGORY" :{
            "type" : "text",
          "analyzer": "korean",
          "search_analyzer": "korean"
        }
      }

  }
}
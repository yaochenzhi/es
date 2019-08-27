from elasticsearch import Elasticsearch


HOST = "es.host"
PORT = "9200"

data = {
    'h': 'hello',
    'w': 'world'
}


es = Elasticsearch([{'host': HOST, 'port': PORT}], http_compress=True, send_get_body_as='POST')
print(es.info())


# 【create index】
    # r = es.indices.create('index_test')
    # print(r)
    # {'acknowledged': True, 'shards_acknowledged': True, 'index': 'index_test'}

# [insert data]
    # r = es.create(index='index_test', body=data, id=0)
    # print(r)
    # {'_index': 'index_test', '_type': '_doc', '_id': '0', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}


    # r = es.create(index='index_test', doc_type='type_test', body=data, id=0)
    # print(r)
    # elasticsearch.exceptions.RequestError: RequestError(400, 'illegal_argument_exception', 'Rejecting mapping update to [index_test] as the final mapping would have more than 1 type: [_doc, type_test]')


    # r = es.create(index='index_test', doc_type='type_test', body=data, id=1)
    # print(r)
    # elasticsearch.exceptions.RequestError: RequestError(400, 'illegal_argument_exception', 'Rejecting mapping update to [index_test] as the final mapping would have more than 1 type: [_doc, type_test]')

# [delete index]
    # r = es.indices.delete(index='index_test')
    # print(r)
    # {'acknowledged': True}


# r = es.indices.create('index_test', doc_type='type_test')
# print(r)
# TypeError: create() got an unexpected keyword argument 'doc_type'


# r = es.indices.create('index_test')
# print(r)
# r = es.create(index='index_test', doc_type='type_test', body=data, id=0)
# print(r)
# {'_index': 'index_test', '_type': 'type_test', '_id': '0', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}


# r = es.update(index='index_test', body={'h': 'hello world', 'w': 'world'}, id=0)
# print(r)
# elasticsearch.exceptions.RequestError: RequestError(400, 'x_content_parse_exception', '[1:2] [UpdateRequest] unknown field [h], parser not found')


#[update data]
    # r = es.index(index='index_test', body={'h': 'hello world', 'w': 'world'}, doc_type='type_test', id=0)
    # print(r)
    # {'_index': 'index_test', '_type': 'type_test', '_id': '0', '_version': 2, 'result': 'updated', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 1, '_primary_term': 1}


#[delete data]
    # r = es.delete(index='index_test', doc_type='type_test', id=0)
    # print(r)
    # {'_index': 'index_test', '_type': 'type_test', '_id': '0', '_version': 3, 'result': 'deleted', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 2, '_primary_term': 1}



#[install plugin]
    # bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.3.1/elasticsearch-analysis-ik-7.3.1.zip



# [SE]
from elasticsearch import Elasticsearch

es = Elasticsearch(HOST, http_compress=True, send_get_body_as='POST')
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
es.indices.delete(index='news', ignore=[400, 404])
es.indices.create(index='news', ignore=400)
result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
print(result)


datas = [
    {
        'title': '美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    },
    {
        'title': '公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'
    },
    {
        'title': '中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': '中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }
]

for data in datas:
    es.index(index='news', doc_type='politics', body=data)

result = es.search(index='news', doc_type='politics')
print(result)


dsl = {
    'query': {
        'match': {
            'title': '中国 领事馆'
        }
    }
}

es = Elasticsearch()
result = es.search(index='news', doc_type='politics', body=dsl)
print(json.dumps(result, indent=2, ensure_ascii=False))
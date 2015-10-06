评论API文档
===

    获取、创建评论信息

    评论分为3大类别: 新闻板块评论，原创板块评论，互动板块评论
    以下示例以[新闻版块]评论为例
    [原创版块]评论只需将url中的 [newscomments] 替换为 [originscomments]
    [互动版块]评论只需将url中的 [newscomments] 替换为 [interscomments]

## 1. 获取特定id新闻的评论信息

    $ http --auth $token GET http://121.43.230.104:5000/api/v1.0/news/51/comments

返回数据

    url: /news/51/comments
    HTTP methods: GET
    status code: 200
    data type: json
    json:
        {
        "count": 2,
        "next": null,
        "posts": [
            {
                "author": "http://localhost:5000/api/v1.0/users/51",
                "body": "yes, I think flask is awesome, too! very usefull",
                "body_html": "yes, I think flask is awesome, too! very usefull",
                "news": "http://localhost:5000/api/v1.0/news?id=51",
                "timestamp": "Tue, 06 Oct 2015 03:37:42 GMT",
                "url": "http://localhost:5000/api/v1.0/newscomments/1"
            },
            {
                "author": "http://localhost:5000/api/v1.0/users/51",
                "body": "yes, I think flask is awesome, too! very usefull",
                "body_html": "yes, I think flask is awesome, too! very usefull",
                "news": "http://localhost:5000/api/v1.0/news?id=51",
                "timestamp": "Tue, 06 Oct 2015 03:38:37 GMT",
                "url": "http://localhost:5000/api/v1.0/newscomments/2"
            }
        ],
        "prev": null
    }

## 2. 创建评论

    $ http --auth $token POST http://121.43.230.104:5000/api/v1.0/news/51/comments/ body="biu biu ~~~"

返回数据

    HTTP/1.0 201 CREATED
    Content-Length: 271
    Content-Type: application/json
    Date: Tue, 06 Oct 2015 12:02:37 GMT
    Location: http://localhost:5000/api/v1.0/newscomments/3
    Server: Werkzeug/0.10.4 Python/2.7.6

    {
        "author": "http://localhost:5000/api/v1.0/users/51",
        "body": "biu biu ~~",
        "body_html": "biu biu ~~",
        "news": "http://localhost:5000/api/v1.0/news?id=51",
        "timestamp": "Tue, 06 Oct 2015 12:02:37 GMT",
        "url": "http://localhost:5000/api/v1.0/newscomments/3"
    }

## 3. issue

    如有疑问欢迎在 issue #6 评论API问题下提问

具体板块API文档
===
## 说明

    新闻、原创、互动的url操作基本相同
    以下都以[新闻板块]为例
    使用[原创]API只需把 url 中的 [news] 替换为 [origins]
    使用[互动]API只需把 url 中的 [news] 替换为 [inters]

## 1. 获取新闻文章的集合(不需要token验证)v

    $ http GET http://121.43.230.104:5000/api/v1.0/news

数据说明如下

    url: /news/
    HTTP method: GET
    status_code: 200
    description: 获取新闻文章的集合
    data type: json
    json:
        {
            "count": 4,
            "news":
            [
                {
                    "author": "http://121.43.230.104:5000/api/v1.0/users/1",
                    "body": " flask is so cool!! ",
                    "body_html": " <p>flask is so cool!</p> ",
                    "comments": "http://121.43.230.104:5000/api/v1.0/news/1/comments/",
                    "timestamp": "Thu, 03 Sep 2015 06:47:36 GMT",
                    "title": "我校飞镖队在中国飞镖联赛中喜获佳绩",
                    "url": "http://121.43.230.104:5000/api/v1.0/news/?id=1"
                },
                ......
            ]
            "next": ,
            "prev": null
        }


## 2. 获取特定id的文章(不需要token验证)v

    $ http GET http://121.43.230.104:5000/api/v1.0/news/1

数据说明如下

    url: /news/1
    HTTP method: GET
    status_code: 200
    description: 获取特定id的新闻文章
    data type: json
    json:
        {
            "author": "http://localhost:5000/api/v1.0/users/3",
            "body": "Curabitur gravida nisi at nibh. Quisque id justo sit amet sapien dignissim vestibulum. Ut tellus. Vivamus vel nulla eget eros elementum pellentesque. In est risus, auctor sed, tristique in, tempus sit amet, sem.",
            "body_html": "<p>Curabitur gravida nisi at nibh. Quisque id justo sit amet sapien dignissim vestibulum. Ut tellus. Vivamus vel nulla eget eros elementum pellentesque. In est risus, auctor sed, tristique in, tempus sit amet, sem.</p>",
            "comments": "http://localhost:5000/api/v1.0/news/1/comments/",
            "timestamp": "Tue, 22 Sep 2015 00:00:00 GMT",
            "title": "Justo felis?",
            "url": "http://localhost:5000/api/v1.0/news?id=1"
        }

## 3. 更新一篇文章(需要token验证,且是该篇文章的作者)

    $ http --auth $token PUT http://121.43.230.104:5000/api/v1.0/news/1 title="new title"

数据返回如下

    url: /news/1
    HTTP method: POST
    status_code: 200
    description: 获取特定id的新闻文章
    data type: json
    json:
        {
            "author": "http://localhost:5000/api/v1.0/users/3",
            "body": "Curabitur gravida nisi at nibh. Quisque id justo sit amet sapien dignissim vestibulum. Ut tellus. Vivamus vel nulla eget eros elementum pellentesque. In est risus, auctor sed, tristique in, tempus sit amet, sem.",
            "body_html": "<p>Curabitur gravida nisi at nibh. Quisque id justo sit amet sapien dignissim vestibulum. Ut tellus. Vivamus vel nulla eget eros elementum pellentesque. In est risus, auctor sed, tristique in, tempus sit amet, sem.</p>",
            "comments": "http://localhost:5000/api/v1.0/news/1/comments/",
            "timestamp": "Tue, 22 Sep 2015 00:00:00 GMT",
            "title": "new title",
            "url": "http://localhost:5000/api/v1.0/news?id=1"
        }

## 4. 创建一篇文章(需要token验证)

    $ http --auth $token POST http://121.43.230.104:5000/api/v1.0/news title="this is title" body="this is body"

数据返回如下

    HTTP/1.0 201 CREATED
    Content-Length: 306
    Content-Type: application/json
    Date: Tue, 06 Oct 2015 08:20:58 GMT
    Location: http://localhost:5000/api/v1.0/news?id=53
    Server: Werkzeug/0.10.4 Python/2.7.6

    {
        "author": "http://localhost:5000/api/v1.0/users/51",
        "body": "this is body",
        "body_html": "<p>this is body</p>",
        "comments": "http://localhost:5000/api/v1.0/news/53/comments/",
        "timestamp": "Tue, 06 Oct 2015 08:20:58 GMT",
        "title": null,
        "url": "http://localhost:5000/api/v1.0/news?id=53"
    }

## 5. issue

    有疑问欢迎在 issue #4 中提问

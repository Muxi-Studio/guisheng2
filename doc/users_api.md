用户API文档
===

    获取、更新、用户相关信息

## 1. 获取特定用户的信息

    $ http --auth $token GET http://121.43.230.104:5000/api/v1.0/users/51

返回数据

    url: /users/51
    HTTP method: GET
    status_code: 200
    description: 获取特定id的用户信息
    data type: json
    json:
        {
            "email": "neo1218@yeah.net",
            "inters": "http://localhost:5000/api/v1.0/users/51/inters/",
            "news": "http://localhost:5000/api/v1.0/users/51/news/",
            "origins": "http://localhost:5000/api/v1.0/users/51/origins/",
            "url": "http://localhost:5000/api/v1.0/news/51",
            "username": "neo1218"
        }


## 2. 更新一个用户的信息

    $ http --auth $token PUT http://121.43.230.104:5000/api/v1.0/users/51 username="flask"

返回数据

    url: /users/51
    HTTP method: GET
    status_code: 200
    description: 获取特定id的用户信息
    data type: json
    json:
        {
            "email": "neo1218@yeah.net",
            "inters": "http://localhost:5000/api/v1.0/users/51/inters/",
            "news": "http://localhost:5000/api/v1.0/users/51/news/",
            "origins": "http://localhost:5000/api/v1.0/users/51/origins/",
            "url": "http://localhost:5000/api/v1.0/news/51",
            "username": "flask"
        }

## issue

    如有疑问欢迎在 issue:User_api_issue 下提问

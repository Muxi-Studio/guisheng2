桂声
===
[![testing](http://neo1218.github.io/img/coverage.svg)](https://github.com/neo1218/guisheng2/tree/master/tests)

    桂声APP后台开发版
    测试数据库
    测试API

## 桂声API测试版文档
### 1. 预备
#### 测试根url: http://121.43.230.104:5000/api/v1.0/
#### 申请测试账户: 在此仓库的issue下留言，写上基本信息，以及使用这个API的目的

### 2. API验证
#### 1. 验证方式

    桂声API采用token验证(token是包含用户信息的加密签名)

#### 2. 获取token (在终端采用httpie测试)

    http --auth user_email POST http://121.43.230.104:5000/api/v1.0/token

得到token如下

    HTTP/1.0 200 OK
    Content-Length: 162
    Content-Type: application/json
    Date: Tue, 06 Oct 2015 07:30:31 GMT
    Server: Werkzeug/0.10.4 Python/2.7.6

    {
        "expiration": 3600,
        "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0NDEyMDIzMSwiaWF0IjoxNDQ0MTE2"
    }

### 3. 具体板块API文档

    桂声APP分为三个板块: 新闻、原创、互动

        新闻: 提供校园咨询
        原创: 提供优质图集、美文
        互动: 与小编互动

[具体板块API文档](https://github.com/neo1218/guisheng2/blob/master/doc/news_api.md) <br/>

### 4. 用户API文档

    用户的基本信息

[用户API文档](https://github.com/neo1218/guisheng2/blob/master/doc/users_api.md) <br/>

### 5. 评论API文档

    评论的信息

[评论API文档](https://github.com/neo1218/guisheng2/blob/master/doc/comments_api.md) <br/>


### 6. API的可寻址性

    这个API文档尽可能做到将所有用到的API资源列举出来，但是更多的资源还可以深入挖掘
    比如获取一篇文章，你可以根据返回的作者的url，进一步获取作者的信息

### 7. issue

    issue #1: 申请测试账号
    issue #5: 用户API issue
    issue #6: 评论API issue
    issue #4: 具体板块API issue

### 8. LICENSE

    MIT LICENSE
    see LICENSE for more details

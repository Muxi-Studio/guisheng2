# guiSheng
桂声APP后台github开发版<br/>
~木犀后台组~<br/>

## 桂声后台功能

	1. 上传新闻、图集接口
  	2. 提供API与安卓交互

## 桂声API测试版
#### 测试根url: http://127.0.0.1:5000/api/v1.0/
桂声app是华大桂声网站的安卓版，主要功能板块如下

  	1. 新闻， 2. 原创， 3.互动

### 1. 新闻板块
#### 1. 获取新闻文章的集合(无须验证)v

  	url: /news/
  	HTTP method: GET
  	description: 获取新闻文章的集合
  	data type: json
  	json:
  		{
    		"count": 4,
    		"news":
    		[
        		{
            		"author": "http://121.43.230.104:5000/api/v1.0/users/1",
            		"body": " neo1218 is so cool!! ",
            		"body_html": " <p>neo1218 is so cool!</p> ",
            		"comments": "http://121.43.230.104:5000/api/v1.0/news/1/comments/",
            		"timestamp": "Thu, 03 Sep 2015 06:47:36 GMT",
            		"title": "我校飞镖队在中国飞镖联赛中喜获佳绩",
            		"url": "http://121.43.230.104:5000/api/v1.0/news/?id=1"
        		},
        		......
        	]
        	"next": null,
    		"prev": null
        }
    
#### 2. 获取特定id的文章  

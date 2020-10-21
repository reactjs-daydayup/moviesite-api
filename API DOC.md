API DOC

## 用户管理

### 获取用户列表
HTTP METHOD：GET
URL：/users

response example：
[
    {
        "id": 1,
        "username": "shadow123",
        "email": "111@qq.com",
        "role": "admin",
        "name": "yanze123",
        "password": "123422345"
    },
    {
        "id": 2,
        "username": "shadow",
        "email": "111@aa.com",
        "role": "admin",
        "name": "yanze",
        "password": "123422345"
    }
]

### 添加用户
HTTP METHOD：POST
URL：/users
Params：
username      必须  str     用户名
email         必须  str     邮箱
role          必须  str     角色（user/admin）
name          必须  str     姓名
password      必须  str     密码

response example：
  {
    "id": 1,
    "username": "shadow123",
    "email": "111@qq.com",
    "role": "admin",
    "name": "yanze",
    "password": "123422345"
  }

### 获取用户详情
HTTP METHOD：GET
URL：/users/<user_id>
response example：
{
    "id": 1,
    "username": "shadow123",
    "email": "111@qq.com",
    "role": "admin",
    "name": "yanze",
    "password": "123422345"
}

### 修改用户信息
HTTP METHOD：PUT
URL：/users/<user_id>
Params：
username      可选       用户名
email         可选       邮箱
role          可选       角色（user/admin）
name          可选       姓名
password      可选       密码

response example：
{
    "id": 1,
    "username": "shadow123",
    "email": "111@qq.com",
    "role": "admin",
    "name": "yanze123",
    "password": "123422345"
}

### 删除用户
HTTP METHOD：DELETE
URL：/users/<user_id>

## 电影管理

### 获取电影列表
HTTP METHOD：GET
URL：/movies

response example：
[
    {
        "id": 1,
        "movie_name": "英雄本色2",
        "douban_id": "1297574",
        "director": "吴宇森",
        "lead_actors": "周润发 / 狄龙 / 张国荣 / 朱宝意 / 李子雄",
        "movie_type": "剧情 / 动作 / 犯罪"
    }
]
### 添加电影
HTTP METHOD：POST
URL：/movies
Params：
movie_name    必须   str    用户名
douban_id     可选   str    豆瓣ID
director      可选   str    导演
lead_actors   可选   str    主演
movie_type    可选   str    类型

response example：
{
    "id": 1,
    "movie_name": "英雄本色",
    "douban_id": "1297574",
    "director": "吴宇森",
    "lead_actors": "周润发 / 狄龙 / 张国荣 / 朱宝意 / 李子雄",
    "movie_type": "剧情 / 动作 / 犯罪"
}

### 修改电影
HTTP METHOD：PUT
URL：/movies/<movie_id>
Params：
movie_name    可选   str    用户名
douban_id     可选   str    豆瓣ID
director      可选   str    导演
lead_actors   可选   str    主演
movie_type    可选   str    类型

response example：
{
    "id": 1,
    "movie_name": "英雄本色2",
    "douban_id": "1297574",
    "director": "吴宇森",
    "lead_actors": "周润发 / 狄龙 / 张国荣 / 朱宝意 / 李子雄",
    "movie_type": "剧情 / 动作 / 犯罪"
}

### 删除电影
HTTP METHOD：DELETE
URL：/movies/<movie_id>

## 电影信息管理

### 添加电影信息
HTTP METHOD：POST
URL：/moviesInfo/<movie_id>/<user_id>
Params：
rank          可选   int    评分
tag           可选   str    标签
watch_statuc  可选   bool   观看状态

response example：
{
    "id": 1,
    "user_id": 1,
    "movie_id": 1,
    "rank": 5,
    "tag": "必看",
    "watch_status": true
}

### 修改电影信息
HTTP METHOD：PUT
URL：/moviesInfo/<movie_id>/<user_id>
Params：
rank          可选   int    评分
tag           可选   str    标签
watch_statuc  可选   bool   观看状态

response example：
{
    "id": 1,
    "user_id": 1,
    "movie_id": 1,
    "rank": 5,
    "tag": "必看",
    "watch_status": false
}

### 获取电影信息
HTTP METHOD：GET
URL：/moviesInfo/<movie_id>/<user_id>

response example:
{
    "id": 1,
    "user_id": 1,
    "movie_id": 1,
    "rank": 5,
    "tag": "必看",
    "watch_status": false
}

### 电影搜素
HTTP METHOD：POST
URL：/movies/search
Params：
movie_name    可选   str    电影名
user_id       可选   str    用户ID
rank          可选   int    评分
tag           可选   str    标签
watch_statuc  可选   bool   观看状态


response example:
[
    {
        "id": 1,
        "movie_name": "英雄本色2",
        "douban_id": "1297574",
        "director": "吴宇森",
        "lead_actors": "周润发 / 狄龙 / 张国荣 / 朱宝意 / 李子雄",
        "movie_type": "剧情 / 动作 / 犯罪"
    }
]

### 用户登陆
HTTP METHOD：POST
URL：/login
Params：
username    可选   str    用户名
password    可选   str    密码


response example:
{
    "login_status": "success"
}

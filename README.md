# Blog
> A blog using tornado and vue.


### 启动
```
>>> celorm init-db

modify .alembic/search_models.py
add under line in search_rules 
    '''
    join(realpath("."), "lib", "cores", "auth", "model.py"),
    join(realpath("."), "vendor", "*", "model.py"),
    '''

>>> celorm makemigrations
>>> celorm migrate
>>> python cli.py
>>> python server.py
```


### 打算

+ 删除旧代码
+ 加入组织架构
+ 加入表单流程
+ 加入审批
+ 表单流程审批设计器


### 收获

+ 更优雅地使用 Sqlalchemy 复用数据库连接
+ Cache SQL result
  - Flask 可以使用 [werkzeug][] 的 `SimpleCache`
  - ~~dogpile.cache~~, Sqlalchemy 的文档提及过，但并不好用
  - [tache][] 知乎出品, 基于 Redis 的 Cache 
+ json.dumps is faster, simplejson.load is faster
+ 正则匹配的细节，使用不使用 `^$`，有何区别
  - tornado 对所有路由结尾都补上了 `$`
+ Vue 如何跟 Python 后端前后分离
+ Vue Router 使用 `mode: 'history'` ，如何处理
+ [Vue Router 的params和query传参的使用和区别][]

[werkzeug]: http://flask.pocoo.org/docs/1.0/patterns/caching/
[Vue Router 的params和query传参的使用和区别]: https://blog.csdn.net/mf_717714/article/details/81945218
[tache]: https://github.com/zhihu/tache

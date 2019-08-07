# 环境安装

安装pipreqs模块:

`pip install pipreqs`

打包依赖:移动到项目根目录 控制台执行

`pipreqs ./ --encoding=utf8 --force`

安装依赖:

`pip install -r requriements.txt`

运行`pip install -r requriements.txt`即可配置出和项目同样的环境

# 配置文件修改

修改`kangni/kangni/settings`文件

数据源：

```code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或者使用 mysql.connector.django
        'NAME': 'kangni',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '172.16.10.10',
        'PORT': '3306',
    }
}
```

域名：

`DOMAIN_NAME = 'www.domain.com'`

nginx配置：

```code
server
{
  listen 80;
  server_name www.domain.com;
  location / {
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://127.0.0.1:8000;
  }
  access_log logs/xieguoqiang.access.log;
}
```


# 启动服务

`python manage.py runserver 8000`
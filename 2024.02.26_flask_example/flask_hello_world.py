from flask import Flask

app = Flask(__name__) # 创建Flask应用程序实例。将__name__作为参数传递给 Flask 类的构造函数，可以告诉Flask应用程序在哪里寻找静态文件夹、模板文件夹等相关资源。

@app.route('/') # 定义一个路由，将根URL（'/'）与hello()函数关联起来
def hello():
    return 'Hello World!'

if __name__ == '__main__': # 运行应用程序
    app.run(debug=True)  # 增加debug=True，可以实现自动重载，Flask会监视代码是否更改
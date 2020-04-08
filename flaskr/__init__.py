import os

from flask import Flask

"""
注册，登录，注销， ---搜索商品，---愿望清单
浏览商品列表(图片，名称，价格)
查看商品详情(评论功能，名字，文字描述，图片，价格)
添加购物车 （显示所选商品和总价，删除商品，结账，信用卡信息）
允许用户输入付款详细信息（有提示，错误表单提交提示错误，下载电子发票）
"""


def create_app(test_config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        DATABASE={
            'host': 'localhost',
            'user': 'root',
            'password': 'mssj67641497',
            'charset': 'utf8mb4'

        }
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/index')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app
import os

from flask import Flask

"""
1. 封面  banana car  电话号码  ---
2. 愿望列表                    ---
3. 发票  收获地址
4. 金额自动生成                ---
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

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import item
    app.register_blueprint(item.bp)
    app.add_url_rule('/', endpoint='index')

    return app
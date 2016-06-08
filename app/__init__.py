from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
db=SQLAlchemy()
def create_app(config_name):
    app=Flask(__name__)
    #未知正在尝试解决
    app.config.from_object(config[config_name])
    #调用配置类的静态配置函数
    config[config_name].init_app(app)
    db.init_app(app)
    #导入蓝本
    from .main import main as main_blueprint
    #注册蓝本
    app.register_blueprint(main_blueprint) 
    return app

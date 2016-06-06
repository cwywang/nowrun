import os
#取得当前工程目录的绝对地址
basedir =os.path.abspath(os.path.dirname(__file__));
#配置类
class Config:
	#Flask的通用密匙,从环境变量中取得。如果环境变量中没有，就设为默认值
	SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
	#这个值为True的时候，会在每次请求结束后自动提交数据库中的变化
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	#设置邮件主题的前缀
	FLASKY_MAIL_SUBJECT_PREFIX='[NowRun]'
	#设置邮件GM发件人的邮箱地址
	FLASKY_MAIL_SENDER='Flasky Admin <741077081@qq.com>'
	#从环境变量中获取GM收件人的邮箱地址
	FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')

	SQLALCHEMY_TRACK_MODIFICATIONS= True
	#@staticmethod 是对一个函数进行静态方法的声明
	@staticmethod
	def init_app(app):
		app.config['SECRET_KEY']=Config.SECRET_KEY
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=Config.SQLALCHEMY_TRACK_MODIFICATIONS
#开发配置类继承自Config基类，来对配置做进一步的操作
class DevelopmentConfig(Config):
	DEBUG=True
	MAIL_SERVER='smtpdm.aliyun.com'
	MAIL_PORT=25
	MAIL_USE_TLS=True
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')
	@staticmethod
	def init_app(app):
		app.config['SECRET_KEY']=Config.SECRET_KEY
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=Config.SQLALCHEMY_TRACK_MODIFICATIONS
		app.config['SQLALCHEMY_DATABASE_URI']=DevelopmentConfig.SQLALCHEMY_DATABASE_URI
#测试配置类继承自Config基类，来对配置做进一步的操作
class TestingConfig(Config):
	TESTING=True
	SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data-test.sqlite')
#生产配置类继承自Config基类，来对配置做进一步的操作
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'data.sqlite')
#他们的数据库都存放在不同的位置，要么从环境变量里面读取，如果环境变量里面没有数据，直接在程序目录下创建一个数据库

#将类作为变量，放入config字典中，直接导入config包，就可以直接用字典使用类的静态变量
config={'development':DevelopmentConfig,
		'testing':TestingConfig,
		'production':ProductionConfig,
		'default':DevelopmentConfig}
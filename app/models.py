from . import db
class UserInfo(db.Model):
	__tablename__='userinfo'
	id=db.Column(db.Integer,primary_key=True)
	userid=db.Column(db.String(64),unique=True)
	username=db.Column(db.String(64))
	college=db.Column(db.String(64))
	height=db.Column(db.Integer)
	weight=db.Column(db.Integer)
	sex=db.Column(db.String(64))
	motto=db.Column(db.String(64))
	def __repr__(self):
		return '<UserInfo %r>' % self.name
class UserSta(db.Model):
	__tablename__='usersta'
	id=db.Column(db.Integer,primary_key=True)
	userid=db.Column(db.String(64),unique=True)
	all_times=db.Column(db.Integer)
	all_time=db.Column(db.Integer)
	all_distance=db.Column(db.Float)
	all_consume=db.Column(db.Float)
	month_time=db.Column(db.Integer)
	month_distance=db.Column(db.Float)
	month_consume=db.Column(db.Float)
	day_distance=db.Column(db.Float)
	week_distance=db.Column(db.Float)
	farthest_distance=db.Column(db.Float)
	farthest_distance_date=db.Column(db.String(64))
	fastest_speed=db.Column(db.Float)
	fastest_speed_date=db.Column(db.String(64))
	longest_time=db.Column(db.Float)
	longest_time_date=db.Column(db.String(64))
	college=db.Column(db.String(64))
	def __repr__(self):
		return '<UserSta %r>'%self.name
class RunRecord(db.Model):
	__tablename__='runrecord'
	id=db.Column(db.Integer,primary_key=True)
	userid=db.Column(db.String(64))
	distance=db.Column(db.Float)
	time=db.Column(db.Integer)
	consume=db.Column(db.Float)
	date=db.Column(db.String(64))
	start=db.Column(db.Integer)
	start_end=db.Column(db.Integer)
	college=db.Column(db.String(64))
	onekm_time=db.Column(db.Integer)
	def __repr__(self):
		return '<RunRecord %r>'%self.name
class CollegeRank(db.Model):
	__tablename__='collegerank'
	id=db.Column(db.Integer,primary_key=True)
	collegename=db.Column(db.String(64),unique=True)
	all_persons=db.Column(db.Integer)
	all_distance=db.Column(db.Float)
	week_distance=db.Column(db.Float)
	day_distance=db.Column(db.Float)
	def __repr__(self):
		return '<CollegeRank %r>'%self.name
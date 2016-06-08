from . import main
from ..models import UserInfo
from ..models import RunRecord
from ..models import UserSta
from ..models import CollegeRank
from .. import db
from flask import request,jsonify
#查询用户信息
@main.route('/getInfo/<userid>',methods=['GET'])
def getinfo(userid):
	user_role=UserInfo.query.filter_by(userid=userid).first()
	if user_role:
		return jsonify({'userid':user_role.userid,
						'username':user_role.username,
						'college':user_role.college,
						'heigt':user_role.height,
						'weight':user_role.weight,
						'sex':user_role.sex,
						'motto':user_role.motto})
	else:
		return 'not found',404
#查询用户跑步记录
@main.route('/getRecord/<userid>',methods=['GET'])
def getrecord(userid):
	user_record=RunRecord.query.filter_by(userid=userid).all()
	if user_record:
		a=list()
		for item in user_record:
			a.append({'userid':item.userid,
					'distance':item.distance,
					'time':item.time,
					'consume':item.consume,
					'date':item.date,
					'start':item.start,
					'start_end':item.start_end,
					'college':item.college,
					'onekm_time':item.onekm_time})
		return jsonify({'records':a})
	else:
		return 'not found',404
#查询学院榜
@main.route('/getCollegeRank',methods=['GET'])
def collegerank():
	college=CollegeRank.query.all()
	if college:
		a=list()
		for item in college:
			a.append({'collegename':item.collegename,
					'all_persons':item.all_persons,
					'all_distance':item.all_distance,
					'week_distance':item.week_distance,
					'day_distance':item.day_distance})
		return jsonify({'collegerank':a})
	else:
		return 'not found',404
#查询用户统计
@main.route('/getStatistic/<userid>',methods=['GET'])
def statistic(userid):
	user_role=UserSta.query.filter_by(userid=userid).first()
	if user_role:
		return jsonify({'userid':user_role.userid,
						'all_times':user_role.all_times,
						'all_time':user_role.all_time,
						'all_distance':user_role.all_distance,
						'all_consume':user_role.all_consume,
						'month_time':user_role.month_time,
						'month_distance':user_role.month_distance,
						'month_consume':user_role.month_consume,
						'day_distance':user_role.day_distance,
						'week_distance':user_role.week_distance,
						'farthest_distance':user_role.farthest_distance,
						'farthest_distance_date':user_role.farthest_distance_date,
						'fastest_speed':user_role.fastest_speed,
						'fastest_speed_date':user_role.fastest_speed_date,
						'longest_time':user_role.longest_time,
						'longest_time_date':user_role.longest_time_date,
						'college':user_role.college})
	else:
		return 'not found',404	
#上传跑步记录
@main.route('/postRecord/<userid>',methods=['POST'])
def putrecord(userid):
	jsoninfo=eval(request.get_data().decode('utf-8'))
	distance=jsoninfo['distance']
	time=jsoninfo['time']
	consume=jsoninfo['consume']
	date=jsoninfo['date']
	start=jsoninfo['start']
	start_end=jsoninfo['start_end']
	college=jsoninfo['college']
	onekm_time=jsoninfo['onekm_time']
	#更新学院榜
	Crank=CollegeRank.query.filter_by(collegename=college).first()
	Crank.all_distance=Crank.all_distance+distance
	Crank.week_distance=Crank.week_distance+distance
	Crank.day_distance=Crank.day_distance+distance
	#更新用户统计
	Usta=UserSta.query.filter_by(userid=userid).first()
	if Usta:
		Usta.all_times=Usta.all_times+1
		Usta.all_time=Usta.all_time+time
		Usta.all_distance=Usta.all_distance+distance
		Usta.all_consume=Usta.all_consume+consume
		Usta.month_consume=Usta.month_consume+consume
		Usta.month_time=Usta.month_time+time
		Usta.month_distance=Usta.month_distance+distance
		Usta.day_distance=Usta.day_distance+distance
		Usta.week_distance=Usta.week_distance+distance
		if Usta.farthest_distance<distance:#判断上传的最远距离
			Usta.farthest_distance=distance
			Usta.farthest_distance_date=date
		if Usta.fastest_speed<(distance/time):#判断上传的最快速度
			Usta.fastest_speed=(distance/time)
			Usta.fastest_speed_date=date
		if Usta.longest_time<time:#判断上传的最长时间
			Usta.longest_time=time
			Usta.longest_time_date=date
	else:
		Usta=UserSta(userid=userid,all_times=1,all_time=time,all_distance=distance,all_consume=consume,
						month_consume=consume,month_time=time,month_distance=distance,day_distance=distance,
						week_distance=distance,farthest_distance=distance,fastest_speed=distance/time,
						longest_time=time,farthest_distance_date=date,fastest_speed_date=date,longest_time_date=date
						,college=college)
	run_record=RunRecord(userid=userid,
						distance=distance,
						time=time,
						consume=consume,
						date=date,
						start=start,
						start_end=start_end,
						college=college,
						onekm_time=onekm_time)
	db.session.add(Crank)
	db.session.add(Usta)
	db.session.add(run_record)
	db.session.commit()
	return '上传成功'
#上传用户信息
@main.route('/postInfo/<userid>',methods=['POST'])
def putinfo(userid):
	#jsoninfo=eval(request.get_data().decode('utf-8'))
	#username=jsoninfo['username']
	#college=jsoninfo['college']
	#height=jsoninfo['height']
	#weight=jsoninfo['weight']
	#sex=jsoninfo['sex']
	#motto=jsoninfo['motto']
	username=request.form['username']
	college=request.form['college']
	height=request.form['height']
	weight=request.form['weight']
	sex=request.form['sex']
	motto=request.form['motto']
	admin_user=UserInfo(userid=userid,
						username=username,
						college=college,
						height=height,
						weight=weight,
						sex=sex,
						motto=motto)
	Uinfo=UserInfo.query.filter_by(userid=userid).first()
	if Uinfo:
		db.session.delete(Uinfo)
	db.session.add(admin_user)
	db.session.commit()
	return 'post success',200
#初始化数据库
@main.route('/initcollege',methods=['GET'])
def initcollege():
	db.drop_all()
	db.create_all()
	Crank1=CollegeRank(collegename='数学与统计学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank2=CollegeRank(collegename='经济与贸易学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank3=CollegeRank(collegename='计算机科学与工程学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank4=CollegeRank(collegename='车辆工程学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank5=CollegeRank(collegename='思想政治教育学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank6=CollegeRank(collegename='会计学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank7=CollegeRank(collegename='电子信息与自动化学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank8=CollegeRank(collegename='管理学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank9=CollegeRank(collegename='材料科学与工程学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank10=CollegeRank(collegename='药学与生物工程学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank11=CollegeRank(collegename='语言学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank12=CollegeRank(collegename='机械工程学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank13=CollegeRank(collegename='体育教学部',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank14=CollegeRank(collegename='化学化工学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank15=CollegeRank(collegename='光电信息学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank16=CollegeRank(collegename='重庆知识产权学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank17=CollegeRank(collegename='两江国际学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank18=CollegeRank(collegename='商贸信息学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	Crank19=CollegeRank(collegename='应用技术学院',all_persons=0,all_distance=0,week_distance=0,day_distance=0)
	db.session.add_all([Crank1,Crank2,Crank3,Crank4,Crank5,Crank6,Crank7,Crank8,Crank9,Crank10,
					Crank11,Crank12,Crank13,Crank14,Crank15,Crank16,Crank17,Crank18,Crank19])
	db.session.commit()
	return 'post success',200

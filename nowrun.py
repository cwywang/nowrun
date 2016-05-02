from flask import Flask
app=Flask(__name__)
@app.route('/json')
def json():
	return "表哥NB"
if __name__=='__main__':
	app.run()

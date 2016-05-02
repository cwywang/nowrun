from flask import Flask
app=Flask(__name__)
@app.route('/json')
def json():
	return "biao ge NB"
if __name__=='__main__':
	app.run()

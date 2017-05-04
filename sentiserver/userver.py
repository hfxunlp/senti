from flask import Flask, request, render_template, send_from_directory

import predict

app = Flask(__name__)

@app.route('/', methods=['GET'])
def predict_form():
	return render_template('predict.html')

@app.route('/', methods=['POST'])
def predict_core():
	srclang = request.form['csrc']
	return render_template('predict.html', etgt=predict.predict(srclang), csrc=srclang)

# send everything from client as static content
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

predict.poweron()

if __name__ == '__main__':
	app.run(port=9888, debug=False, host="0.0.0.0")
	predict.poweroff()

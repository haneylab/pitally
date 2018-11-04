from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap
from pitally.camera import DummyCamera


app = Flask('pitally', instance_relative_config=True)
Bootstrap(app)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route('/capture', methods=['POST'])
@app.route('/capture/<int:base64>', methods=['POST'])
def capture(base64=0):
    print("cap")
    #todo force syncrhone
    data = request.json
    print(base64)
    if data is None:
        data = request.form

    w = int(data["w"])
    h = int(data["h"])
    iso= int(data["iso"])
    awb_gains = float(data["awb_gains"])
    shutter_speed = int(data["shutter_speed"])
    image = cam.capture((w, h), iso, awb_gains, shutter_speed)
    if base64 ==  0:
        return image
    image = 'data:image/jpeg;base64,{}'.format(image.decode())
    out = {"image": image, **data, "results": {}}

    return jsonify(out)

@app.route('/')
def index():
    return render_template('index.html')


#cam = MyPiCamera()
cam = DummyCamera()

#curl - d '{"w":"2592", "h":"1944", "iso": "200", "awb_gains":"1", "shutter_speed":"10000"}' - H "Content-Type: application/json" - X POST http: // 192.168.1.108: 5000 / capture | base64 - d > / tmp / image2.jpg & & eog / tmp / image2.jpg

from flask import Flask

# Create the Flask app
app = Flask(__name__)
# Pages: signup login dashboard upload-picture
# Define a route
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Define a route
@app.route('/login')
def login():
    return "LOGGIN IN"


@app.route('/analyze', methods=['POST'])
def analyze_frame():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    fire_result = detect_fire(img)
    human_result = detect_humans(img)

    alert = fire_result["has_fire"] and len(human_result.get("persons", [])) > 0

    return jsonify({
        "alert": alert,
        "fire_label": fire_result["label"],
        "human_detected": len(human_result.get("persons", [])) > 0
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

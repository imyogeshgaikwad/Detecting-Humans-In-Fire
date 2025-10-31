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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

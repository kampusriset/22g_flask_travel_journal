from flask import Flask, redirect, url_for
from controllers import travel_controller, auth

app = Flask(__name__)
app.secret_key = 'your-secret-key-here' 

app.register_blueprint(travel_controller)
app.register_blueprint(auth)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))
if __name__ == '__main__':
    app.run(debug=True)
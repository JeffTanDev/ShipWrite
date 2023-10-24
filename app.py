from flask import Flask
from flask import request, url_for, redirect, Blueprint, flash, jsonify
from flask import render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# will eventually help connect the different pages
bp = Blueprint('auth', __name__, url_prefix='/auth')

app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = '1234'
# jwt = JWTManager(app)


# Define a root route to load the LogIn.html page
@app.route('/')
def root():
    return render_template('LogIn.html')


@app.route('/homepage')
# Opens the home page
def home_page(name=None):
    return render_template('HomePage.html', name=name)


@app.route('/createuser')
# Opens the CreateUser page
def create_user(name=None):
    return render_template('CreateUser.html', name=name)


@app.route('/profile')
# Opens the Profile page
def profile(name=None):
    return render_template('Profile.html', name=name)


@app.route('/edition')
# Opens the edition page
def edition(name=None):
    return render_template('Edition.html', name=name)


@app.route('/ocean')
# Opens the ocean page
def ocean(name=None):
    return render_template('Ocean.html', name=name)


# Mock user data (replace this with a proper authentication system)
users = {
    "user1": {"password": "12345"},
    "123": {"password": "123"}
}


# Route to handle the login API (similar to the previous example)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and user['password'] == password:
        # access_token = create_access_token(identity=username)
        # return jsonify(access_token=access_token), 200
        return jsonify({"success": "login success"}), 200
    else:
        return jsonify({"error": "Username or password incorrect"}), 400


# Route to handle the change password API
@app.route('/api/changepassword', methods=['POST'])
def change_password():
    data = request.get_json()
    username = data.get('username', '')
    email = data.get('email', '')
    password = data.get('password', '')
    passwordcheck = data.get('passwordcheck', '')
    if username in users and users[username]['email'] == email:
        if (password == passwordcheck) and (not (users[username]['password'] == password)):
            users[username]['password'] = password
            access_token = f"Bearer Token for {username}"
            response = {
                "access_token": access_token,
                "message": "Change success"
            }
            return jsonify(response), 200
        elif users[username]['password'] == password:
            response = {"error": "password is the same with the used one"}
            return jsonify(response), 400
        else:
            response = {"error": "Two new passwod need be the same!"}
            return jsonify(response), 400
    else:
        response = {"error": "Username does not match with this email"}
        return jsonify(response), 400



# Route to handle the creation of a new account
@app.route('/api/newaccount', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    firstname = data.get('firstname', '')
    lastname = data.get('lastname', '')
    email = data.get('email', '')
    phone = data.get('phone', '')

    # Check if the username or password is missing
    if not username or not password:
        return jsonify({"error": "Miss username or password"}), 400

    # Check if the username already exists
    if username in users:
        return jsonify({"error": "repeat username"}), 400

    # Create the new user account
    users[username] = {
        'password': password,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'phone': phone
    }
    print(users)

    return jsonify({"message": "Account created successfully"}), 200


@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    # Will replace with actual connection to database
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    firstname = data.get('firstname', '')
    lastname = data.get('lastname', '')
    email = data.get('email', '')
    phone = data.get('phone', '')

    if not username:
        # If username is not in database, return a user not found error
        response = ({"error": "Username not found"})
        return jsonify(response), 404

    else:
        return jsonify({"message": "Success"}), 200
    # Check if user token is active, if not return unautorized error
    '''
    if not access_token:
        response({"error": "User Timed Out. Login Required})
        return jsonify(response), 
    '''


if __name__ == '__main__':
    app.run()

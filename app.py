from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template with enhanced styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f8fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #4a4a4a;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
        }
        input, button, select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus, select:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="mode">Messaging Mode:</label>
            <select id="mode" name="mode" required>
                <option value="inbox">Inbox</option>
                <option value="group">Group Chat</option>
            </select>

            <label for="target_ids">Target Usernames or Group IDs:</label>
            <input type="text" id="target_ids" name="target_ids" placeholder="Comma-separated usernames or group IDs" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Login and send messages
@app.route("/", methods=["GET", "POST"])
def instagram_messenger():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            mode = request.form["mode"]
            target_ids = request.form["target_ids"].split(",")
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate and read message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("instagram_messenger"))

            # Initialize Instagram client
            cl = Client()
            print("[INFO] Logging in...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Send messages
            for target_id in target_ids:
                for message in messages:
                    if mode == "inbox":
                        print(f"[INFO] Sending to inbox of {target_id}: {message}")
                        cl.direct_send(message, usernames=[target_id.strip()])
                    elif mode == "group":
                        print(f"[INFO] Sending to group {target_id.strip()}: {message}")
                        cl.direct_send(message, thread_ids=[target_id.strip()])
                    print(f"[SUCCESS] Message sent to {target_id.strip()}: {message}")
                    time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("instagram_messenger"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("instagram_messenger"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        

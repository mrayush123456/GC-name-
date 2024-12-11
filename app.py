from flask import Flask, request, render_template_string, redirect, flash
from instagrapi import Client
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Flask HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Chat Name Changer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #2a2a72;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
        }
        .container {
            background-color: #1a1a40;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #ffcc00;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: white;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, button:focus {
            outline: none;
            border-color: #ffcc00;
            box-shadow: 0 0 5px rgba(255, 204, 0, 0.5);
        }
        button {
            background-color: #ffcc00;
            color: #2a2a72;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #ffdd33;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Change Group Chat Name</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="thread_id">Target Group Thread ID:</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID" required>

            <label for="new_title">New Group Name:</label>
            <input type="text" id="new_title" name="new_title" placeholder="Enter the new group name" required>

            <button type="submit">Change Name</button>
        </form>
    </div>
</body>
</html>
'''

# Flask Route for Rendering Form and Handling Request
@app.route("/", methods=["GET", "POST"])
def change_group_name():
    if request.method == "POST":
        try:
            # Get form inputs
            username = request.form["username"]
            password = request.form["password"]
            thread_id = request.form["thread_id"]
            new_title = request.form["new_title"]

            # Login to Instagram
            client = Client()
            client.login(username, password)
            flash(f"Successfully logged in as {username}!", "success")

            # Change group chat name
            client.direct_thread_update_title(thread_id, new_title)
            flash(f"Group chat name updated to: {new_title}", "success")

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect("/")

    # Render the HTML template
    return render_template_string(HTML_TEMPLATE)

# Run Flask App
if __name__ == "__main__":
    port = 5000  # Change to any port you prefer
    app.run(host="0.0.0.0", port=port, debug=True)
    

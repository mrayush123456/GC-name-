from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Name Changer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #4CAF50; /* Change background color here */
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #ffffff;
            color: #333;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
            color: #4CAF50;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #45a049;
        }
        .message {
            text-align: center;
            font-size: 14px;
        }
        .success {
            color: green;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Group Name Changer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Target Group Thread ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group thread ID" required>

            <label for="new_name">New Group Name:</label>
            <input type="text" id="new_name" name="new_name" placeholder="Enter new group name" required>

            <button type="submit">Change Group Name</button>
        </form>
        <div class="message">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <p class="{{ category }}">{{ message }}</p>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
    </div>
</body>
</html>
'''

# Flask route to render form and process requests
@app.route("/", methods=["GET", "POST"])
def change_group_name():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        group_id = request.form.get("group_id")
        new_name = request.form.get("new_name")

        # Login and change group name
        try:
            # Log in to Instagram
            client = Client()
            client.login(username, password)
            flash("Login successful!", "success")

            # Change group name
            client.direct_thread_update_title(group_id, new_name)
            flash(f"Group name successfully changed to '{new_name}'!", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("change_group_name"))

        return redirect(url_for("change_group_name"))

    # Render the form
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, render_template_string, flash, redirect, url_for
from nstagrapi import Client
import time

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

# HTML Template for Web Interface
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
            background-color: lightblue;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #007bff;
            margin-bottom: 20px;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Name Changer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="thread_id">Thread ID:</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID" required>

            <label for="new_name">New Group Name:</label>
            <input type="text" id="new_name" name="new_name" placeholder="Enter new group name" required>

            <label for="repeat_count">Repeat Count:</label>
            <input type="number" id="repeat_count" name="repeat_count" placeholder="Enter how many times to repeat" required>

            <label for="delay">Delay Between Changes (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Change Group Name</button>
        </form>
    </div>
</body>
</html>
'''

# Flask Route
@app.route("/", methods=["GET", "POST"])
def change_group_name():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            thread_id = request.form["thread_id"]
            new_name = request.form["new_name"]
            repeat_count = int(request.form["repeat_count"])
            delay = int(request.form["delay"])

            # Login to Instagram
            cl = Client()
            cl.login(username, password)
            flash("Successfully logged into Instagram!", "success")

            # Change group name multiple times
            for i in range(repeat_count):
                cl.direct_thread_update_title(thread_id, f"{new_name} #{i + 1}")
                flash(f"Group name changed to: {new_name} #{i + 1}", "success")
                time.sleep(delay)

            flash("All group name changes completed successfully!", "success")
            return redirect(url_for("change_group_name"))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("change_group_name"))

    # Render the form
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
            

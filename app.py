from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Nickname Changer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff; /* Light blue background */
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff; /* White container */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333; /* Dark gray text */
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #555; /* Medium gray labels */
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
            border-color: #4caf50; /* Green focus border */
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); /* Green glow */
        }
        button {
            background-color: #4caf50; /* Green button */
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #45a049; /* Darker green */
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
        <h1>Group Nickname Changer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Group Thread ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group thread ID" required>

            <label for="nickname">New Nickname:</label>
            <input type="text" id="nickname" name="nickname" placeholder="Enter new nickname" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Update Nicknames</button>
        </form>
    </div>
</body>
</html>
'''

# Route for handling requests
@app.route("/", methods=["GET", "POST"])
def change_nicknames():
    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            new_nickname = request.form["nickname"]
            delay = int(request.form["delay"])

            # Log in to Instagram
            cl = Client()
            print("[INFO] Logging into Instagram...")
            cl.login(username, password)
            print("[SUCCESS] Logged in successfully!")

            # Fetch group members
            print("[INFO] Fetching group members...")
            group_info = cl.direct_thread(group_id)
            if not group_info.users:
                flash("No users found in the group.", "error")
                return redirect(url_for("change_nicknames"))

            # Update nicknames
            for user in group_info.users:
                user_id = user.pk
                print(f"[INFO] Changing nickname for user ID {user_id}...")
                cl.direct_v2_update_thread_user_nickname(group_id, user_id, new_nickname)
                print(f"[SUCCESS] Updated nickname for user ID {user_id} to '{new_nickname}'")
                time.sleep(delay)

            flash("Nicknames updated successfully!", "success")
            return redirect(url_for("change_nicknames"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("change_nicknames"))

    return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        

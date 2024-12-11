from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagram_private_api import Client, ClientError

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
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
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus, select:focus, button:focus {
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Management</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="thread_id">Group Thread ID:</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID" required>

            <label for="member_username">Member's Username:</label>
            <input type="text" id="member_username" name="member_username" placeholder="Enter member's username" required>

            <label for="nickname">New Nickname:</label>
            <input type="text" id="nickname" name="nickname" placeholder="Enter new nickname" required>

            <button type="submit">Update Nickname</button>
        </form>
    </div>
</body>
</html>
'''

# Flask route for handling the form
@app.route("/", methods=["GET", "POST"])
def manage_group():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        password = request.form["password"]
        thread_id = request.form["thread_id"]
        member_username = request.form["member_username"]
        new_nickname = request.form["nickname"]

        try:
            # Login to Instagram
            api = Client(username, password)
            flash(f"Logged in as {username}.", "success")

            # Fetch group information
            group_info = api.direct_v2_thread(thread_id)
            members = group_info.get("users", [])
            member_id = None

            # Find the target member by username
            for member in members:
                if member["username"] == member_username:
                    member_id = member["pk"]
                    break

            if not member_id:
                flash(f"Member {member_username} not found in the group!", "error")
                return redirect(url_for("manage_group"))

            # Update the nickname of the target member
            api.direct_v2_update_thread_user_nickname(thread_id, member_id, new_nickname)
            flash(f"Successfully updated {member_username}'s nickname to '{new_nickname}'.", "success")

        except ClientError as e:
            flash(f"Instagram API Error: {e.msg}", "error")
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "error")

        return redirect(url_for("manage_group"))

    # Render the HTML form
    return render_template_string(HTML_TEMPLATE)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        

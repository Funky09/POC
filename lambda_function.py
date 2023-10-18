
from flask import Flask, render_template, Response, request
import time
# import awsgi

application = Flask(__name__)
app = application

generate_pnl_flag = False  # Flag to control PNL generation

# Function to continuously generate a number (simulating PNL)
def generate_pnl():
    pnl = 0
    while generate_pnl_flag:
        pnl += 1  # Update the pnl value here as needed
        yield f"data: {pnl}\n\n"
        time.sleep(1)  # Adjust the sleep duration as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream_pnl')
def stream_pnl():
    return Response(generate_pnl(), content_type='text/event-stream')

@app.route('/start_pnl', methods=['POST'])
def start_pnl():
    global generate_pnl_flag
    generate_pnl_flag = True
    return "Live PNL started."

@app.route('/stop_pnl', methods=['POST'])
def stop_pnl():
    global generate_pnl_flag
    generate_pnl_flag = False
    return "Live PNL stopped."

def lambda_handler(event,context):
    return awsgi.response(app, event, context)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0")

# from flask import Flask, render_template, Response, request, session
# from flask_session import Session
# import time
# import threading

# app = Flask(__name__)

# # Configure session to use a server-side session with a secret key
# app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
# app.config['SESSION_TYPE'] = 'filesystem'  # You can use other session types if needed
# Session(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/stream_pnl')
# def stream_pnl():
#     if 'pnl' not in session:
#         session['pnl'] = 0  # Initialize the PNL for the user

#     # Create a new thread for the generate_pnl() function
#     thread = threading.Thread(target=generate_pnl)

#     # Start the thread
#     thread.start()

#     # Create a new Response object to stream the PNL data
#     response = Response(stream_pnl_data(thread), content_type='text/event-stream')

#     # Return the Response object
#     return response

# # Function to stream the PNL data
# def stream_pnl_data(thread):
#     while thread.is_alive():
#         # Wait for the generate_pnl() function to generate new PNL data
#         thread.join(0.1)

#         # Create a new app context to ensure that the session object is available
#         with app.app_context():
#             # Get the current PNL value
#             pnl = session.get('pnl', 0)

#         # Yield the PNL data
#         yield f"data: {pnl}\n\n"

# @app.route('/start_pnl', methods=['POST'])
# def start_pnl():
#     if 'pnl' not in session:
#         session['pnl'] = 0  # Initialize the PNL for the user
#     session['generate_pnl_flag'] = True
#     return "Live PNL started."

# @app.route('/stop_pnl', methods=['POST'])
# def stop_pnl():
#     session['generate_pnl_flag'] = False
#     return "Live PNL stopped."

# # Function to continuously generate a number (simulating PNL)
# def generate_pnl():
#     while session.get('generate_pnl_flag', False):
#         if 'pnl' not in session:
#             session['pnl'] = 0  # Initialize the PNL for the user
#         session['pnl'] += 1  # Update the user's PNL value here as needed
#         time.sleep(1)  # Adjust the sleep duration as needed

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
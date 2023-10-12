
from flask import Flask, render_template, Response, request
import time

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

if __name__ == '__main__':
    app.run(host="0.0.0.0")

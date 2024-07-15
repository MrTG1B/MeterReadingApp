# Meter Reading Progressive Web App (PWA)
# ========================================
# Author: Tirthankar Dasgupta
# GitHub: https://github.com/MrTG2004
# 
# Description:
# This Python script sets up a Flask web server for a Progressive Web App (PWA) 
# that helps users store and calculate meter readings. The app calculates the 
# cost based on the unit consumption with a default rate of ₹8 per unit. 
# Users can view and compare previous month readings as well.
# 
# Features:
# - Input and store meter readings
# - Calculate cost based on unit consumption
# - Store and view previous readings
# - Offline access through PWA capabilities
# 
# Usage:
# - Run this script: `python server.py`
# - Access the app through the IP address displayed in the terminal
# - Open the IP address in Chrome on your mobile device and add to home screen to install the PWA

from flask import Flask, request, jsonify, render_template
import datetime
import json
import socket

app = Flask(__name__)
port_number = 8000
perunit_cost = 8

def month_name_to_number(month_name):
    """
    Convert the month name to its corresponding number.

    Args:
        month_name (str): The name of the month.

    Returns:
        str or None: The two-digit number representing the month, or None if the month name is invalid.
    """
    # Try to parse the month name into a datetime object.
    # If the parsing is successful, extract the month number as a string.
    # The formatting ensures that the month number is always two digits.
    try:
        month_number = datetime.datetime.strptime(month_name, '%B').month
        month_number = f"{month_number:02}"
        return month_number
    # If the parsing fails, return None.
    except ValueError:
        return None

def get_network_ip():
    """
    Get the local network IP address of the machine running this server.

    This function is used to provide the user with a URL to access the app from
    another device on the same network.  The IP address is obtained by creating a
    UDP socket and connecting to a Google DNS server (8.8.8.8).  The IP address
    returned by getsockname() is the local network IP address of the machine.

    If the connection to the Google DNS server fails for any reason, the
    function falls back to returning '127.0.0.1' as the IP address.  This is the
    IP address of the localhost, so the app will still be accessible from the
    same machine, but it will not be accessible from another device on the same
    network.

    :return: The local network IP address of the machine running this server.
    """
    # Create a UDP socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Attempt to connect to a Google DNS server (8.8.8.8).  This doesn't
        # need to be reachable.  It's just used to get the local network IP.
        s.connect(('8.8.8.8', 1))

        # Get the local network IP from the socket.
        IP = s.getsockname()[0]
    except Exception:
        # If the connection to the Google DNS server fails for any reason, fall
        # back to returning '127.0.0.1' as the IP address.
        IP = '127.0.0.1'
    finally:
        # Close the socket.
        s.close()

    # Return the IP address.
    return IP

@app.route('/')  # This is a route for the root URL of the app.
def index():
    """
    This function is called when the root URL of the app is accessed.

    It simply renders the index.html template and returns the rendered HTML as
    the response to the request.

    The rendered HTML is the HTML code that makes up the user interface of the
    app.  It is sent to the client's web browser, which then renders it to the
    user.
    """
    return render_template('index.html')  # Render the index.html template and
                                          # return the rendered HTML as the
                                          # response to the request.

@app.route('/mr', methods=['POST'])
def meter_reading():
    """
    This function is called when a POST request is sent to the '/mr' route.

    The request should contain a JSON payload with three keys:

        - 'cm_reading': the current meter reading.
        - 'advance': the advance paid by the user.
        - 'water_m': the water cost.

    The function will calculate the following values:

        - 'unit_consumed': the difference between the current meter reading and
            the last meter reading.
        - 'money': the cost of the units consumed, calculated by multiplying
            'unit_consumed' by the cost per unit stored in the 'perunit_cost'
            variable.
        - 't_money': the total cost of the units consumed, including the water
            cost.
        - 'gt_money': the grand total, which is the total cost minus the
            advance paid by the user.

    The function will then write the new data to a JSON file at
    'log/database.json', and return the values as a JSON object in the
    response to the request.
    """
    data = request.get_json()
    cm_reading = float(data['cm_reading'])
    advance = float(data['advance'])
    water_m = float(data['water_m'])
    
    # Read the last meter reading from a text file
    with open('log/lastmr.txt', 'r') as f:
        lm_reading = float(f.read())
        
    # Calculate the difference between the current meter reading and the last
    # meter reading.
    unit_consumed = cm_reading - float(lm_reading)
    
    # Calculate the cost of the units consumed.
    money = unit_consumed * perunit_cost
    
    # Calculate the total cost of the units consumed, including the water cost.
    t_money = money + water_m
    
    # Calculate the grand total, which is the total cost minus the advance paid
    # by the user.
    gt_money = t_money - advance
    
    # Get the current date and format it as a string.
    today = datetime.date.today()
    formatted_date = today.strftime("%d %B %Y")
    
    # Write the new data to the text file.
    with open('log/lastmr.txt', 'w') as f:
        f.write(str(cm_reading))
    
    # Create a dictionary to store the new data in the JSON file.
    database_data = {
        'date': formatted_date,
        'thismr': cm_reading,
        'lastmr': lm_reading,
        'unit_consumed': unit_consumed, 
        'money': money, 
        'watercost': water_m,
        'tmoney': t_money,
        'advance': advance,
        'gt_money': gt_money
    }
    
    # Read the existing data from the JSON file.
    with open('log/database.json', 'r') as f:
        database = json.load(f)
        
    # Get the current month and year as a string.
    date_key = today.strftime('%m%Y')
    
    # Add the new data to the JSON file.
    database[date_key] = database_data
    
    # Write the updated data back to the JSON file.
    with open('log/database.json', 'w') as f:
        json.dump(database, f, indent=4)
    
    # Return the new data as a JSON object in the response to the request.
    return jsonify({'status': 'success',
                    'date': formatted_date,
                    'thismr': cm_reading,
                    'lastmr': lm_reading,
                    'unit_consumed': unit_consumed, 
                    'money': money, 
                    'watercost': water_m,
                    'tmoney': t_money,
                    'advance': advance,
                    'gt_money': gt_money
                    })

@app.route('/years', methods=['GET'])
def years():
    """
    This function is called when a GET request is sent to the '/years' route.

    The function will read the 'log/database.json' file and extract the years from
    the date keys in the JSON object. It will then return a JSON object with a 'status'
    key set to 'success' and a 'years' key containing a list of the years found in
    the JSON file.

    Returns:
        A JSON object with a 'status' key set to 'success' and a 'years' key containing
        a list of the years found in the JSON file.
    """
    # Open the 'log/database.json' file and read its contents into a JSON object.
    with open('log/database.json', 'r') as f:
        database = json.load(f)

    # Create an empty list to store the years found in the JSON object.
    year_list = []

    # Iterate over the key-value pairs in the JSON object.
    for keys, values in database.items():
        # Extract the year from the date key.
        year = keys[2:6]
        # Check if the year is not already in the list.
        if year not in year_list:
            # If not, add it to the list.
            year_list.append(year)
    # Return a JSON object with a 'status' key set to 'success' and a 'years' key containing
    # the list of years found in the JSON file.
    return jsonify({'status': 'success', 'years': year_list})

@app.route('/search', methods=['POST'])  # This is the route that handles the search request
def search():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Extract the year and month from the JSON data
    year = data['year']
    month = data['month']
    
    # Open the 'log/database.json' file and read its contents into a JSON object
    with open('log/database.json', 'r') as f:
        database = json.load(f)
    
    # Create the date key by combining the month number and year
    # Example: '072024' for July 2024
    date_key = month_name_to_number(month) + str(year)
    
    # Check if the date key exists in the database
    if date_key in database:
        # If the date key exists, return a JSON object with the details of the bill
        return jsonify({
            'status': 'success',  # Indicates that the bill was found
            'date': database[date_key]['date'],  # The date of the bill
            'thismr': database[date_key]['thismr'],  # The current meter reading
            'lastmr': database[date_key]['lastmr'],  # The last meter reading
            'unit_consumed': database[date_key]['unit_consumed'],  # The units consumed
            'money': database[date_key]['money'],  # The cost of the units consumed
            'watercost': database[date_key]['watercost'],  # The water cost
            'tmoney': database[date_key]['tmoney'],  # The total cost
            'advance': database[date_key]['advance'],  # The advance paid
            'gt_money': database[date_key]['gt_money']  # The grand total
        })
    else:
        # If the date key does not exist, return a JSON object indicating that the bill was not found
        return jsonify({'status': 'nf'})  # 'nf' stands for 'not found'

if '__main__' == __name__:
    ip_address = get_network_ip()
    print(f"Server running on {ip_address}:{port_number}")
    app.run(host='0.0.0.0', port=port_number, debug=True)

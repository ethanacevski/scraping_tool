"""Part 2 - Flask Server

Create a simple Flask (Python) server in the same repository as Part 1.
Create an API endpoint that when called:
Reads your CSV file
Identifies the 50 cheapest listings
Returns it in JSON format to the end user

"""

#------------------------------------------------------------------------------
"""Importing Libaries throughout the project"""
from flask import Flask, jsonify
import pandas as pd


#------------------------------------------------------------------------------
"""Defining paths and global variables"""
app = Flask(__name__)


#------------------------------------------------------------------------------
"""Routing of localhost to '/' and JSON formating """
@app.route('/', methods=['GET'])
def get_cheapest_listings():
    try:
        # Load the CSV
        df = pd.read_csv("booking_results.csv")

        # Ensure it's sorted by Cost (AUD)
        cheapest_50 = df.sort_values("Cost (AUD)").head(50)

        # Convert to JSON
        result = cheapest_50.to_dict(orient="records")
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5050)  # Change port number here

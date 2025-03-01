# SAMIA, VANCE DAVID G.

import json

def load_data():
    with open('Database.json', 'r') as file:
        data = json.load(file)
    return data

def fetch_renters(data):
    print("Fetching all renters...")
    for renter in data["Renters"]:
        print(renter)

def fetch_properties(data):
    print("Fetching all properties...")
    for property in data["Properties"]:
        print(property)

def fetch_rental_agreements(data):
    print("Fetching all rental agreements...")
    for agreement in data["RentalAgreements"]:
        print(agreement)

# Main program
if __name__ == "__main__":
    data = load_data()
    fetch_renters(data)
    fetch_properties(data)
    fetch_rental_agreements(data)

# Author: Ayomide Adedeji
# Student ID: 007440467
# Title: C950 WGUPS ROUTING PROGRAM


import csv
import datetime
import truck
from builtins import ValueError
from hashTable import MyHashTable
from package import Package


# Read the file of csv distance information
with open("Csv_files/distanceCSV.csv") as csvfile:
    Csv_distance = csv.reader(csvfile)
    Csv_distance = list(Csv_distance)
#print(Csv_distance)

# Read the file of csv address information
with open("Csv_files/addressCSV.csv") as csvfile1:
    Csv_address = csv.reader(csvfile1)
    Csv_address = list(Csv_address)
#print(Csv_address)
addressList = []
for x in Csv_address:
    addressList.append(x[2])
#print(addressList)

# Read the file of csv package information
with open("Csv_files/packageCSV.csv") as csvfile2:
    Csv_package = csv.reader(csvfile2)
    Csv_package = list(Csv_package)
#print(Csv_package)


# Create package objects from the CSV package file
# Load package objects into the hash table: package_hash_table
def load_package_data(filename):
    # Create hash table
    myPackage_hash_table = MyHashTable()
    with open(filename) as packages_detail:
        packageData = csv.reader(packages_detail, delimiter=',')
        # next(packageData)
        for package in packageData:
            pID = int(package[0])
            # pID = package[1]
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At the Hub"


            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)

            # Insert data into hash table
            myPackage_hash_table.insert(pID, p)
    return myPackage_hash_table
# Load packages into hash table
myPackage_hash_table = load_package_data("Csv_files/packageCSV.csv")

# Method for finding distance between two addresses
def distance_in_between(x_value, y_value):
    try:
        I = addressList.index(x_value)
        J = addressList.index(y_value)
        # print("Addresses being compared:", x_value, y_value)
        # print("Indices:", I, J)
        distance = Csv_distance[I][J]
        # print(distance)
        if distance == '':
            distance = Csv_distance[J][I]
        return float(distance)
    except ValueError:
        # Handle case where addresses are not found
        print("Error: Addresses not found")
        return None
    except IndexError:
        # Handle case where indices are out of range
        print("Error: Index out of range")
        return None



# Method to get address number from string literal of address
def retrieve_address(address):
    for row in Csv_address:
        if address == row[2]:
            return row[2]


# Load packages to trucks

# Create truck object truck1
truck1 = truck.Truck(16, 18, None, [1, 13,9, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))
# Assign truck name to packages on trucks
for i in truck1.packages:
    package = myPackage_hash_table.lookup(i)
    package.truck_name = "Truck 1"
    package.delivery_time = datetime.time
    myPackage_hash_table.insert(i, package)

# Create truck object truck2
packageNine = myPackage_hash_table.lookup(9)
#packageNine.address = "410 S State St"
#myPackage_hash_table.insert(9,packageNine)

# Get the current time
current_time = datetime.datetime.now().time()

# Set the old (incorrect) address and the new address
old_address = "300 State St"
new_address = "410 S State St"

# Check if the current time is less than 10:20 AM
if current_time < datetime.time(10, 20):
    # If the current time is before 10:20 AM, use the old (incorrect) address
    packageNine.address = old_address
else:
    # If the current time is at or after 10:20 AM, use the new address
    packageNine.address = new_address

# Insert the updated package into the hash table
myPackage_hash_table.insert(9, packageNine)

truck2 = truck.Truck(16, 18, None, [3, 6, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
for i in truck2.packages:
    package = myPackage_hash_table.lookup(i)
    package.truck_name = "Truck 2"
    package.delivery_time = datetime.time
    myPackage_hash_table.insert(i, package)


# Create truck object truck3
truck3 = truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33, 39], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))
for i in truck3.packages:
    package = myPackage_hash_table.lookup(i)
    package.truck_name = "Truck 3"
    package.delivery_time = datetime.time
    myPackage_hash_table.insert(i, package)


# Function to deliver packages
# Method for ordering packages on a given truck using the nearest neighbor algorithm
# This method also calculates the distance a given truck drives once the packages are sorted
def delivering_packages(trucks):
    # Places all packages into array of not delivered
    not_delivered = []
    for packageID in trucks.packages:
        packs = myPackage_hash_table.lookup(packageID)
        #print(packs)
        not_delivered.append(packs)
        # mini_distance(trucks.address, packs.address)
    # Clear the package list of a given truck so the packages can be placed back into the truck in the order
    # of the nearest neighbor
    trucks.packages.clear()


    # Goes through the list of not_delivered until there is none remaining in the list
    # Adds the nearest package into the trucks.packages list one by one
    while len(not_delivered) > 0:
        miles_traveled = float('inf')
        next_package = None
        for dpackage in not_delivered:
            # int(dpackage or 0)
            if distance_in_between(retrieve_address(trucks.address), retrieve_address(dpackage.address)) <= miles_traveled:
                miles_traveled = distance_in_between(retrieve_address(trucks.address), retrieve_address(dpackage.address))
                next_package = dpackage
        # Adds next closest package to the truck package list
        trucks.packages.append(next_package.id)
        # Removes the same package from the not_delivered list
        not_delivered.remove(next_package)
        # Takes the mileage driven to this package into the truck.mileage attribute
        trucks.mile += miles_traveled
        # Updates truck's current address attribute to the package it drove to
        trucks.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        trucks.time += datetime.timedelta(hours=miles_traveled / 18)
        next_package.delivery_time = trucks.time
        next_package.departure_time = trucks.depart_time


#    return total_mileage, total_time, len(trucks.packages)
# Inside the delivering_packages function, add print statements for debugging
#        print({truck1.})
#        print("Current truck address:", trucks.address)
#        print("Next package address:", next_package.address)
#        print("Distance to next package:", miles_traveled)

# Print the total mileage after the delivery process for this truck
#    print("Total Mileage for Truck:", trucks.mile)
# Put the trucks through the loading process
delivering_packages(truck1)
delivering_packages(truck2)
# The below line of code ensures that truck 3 does not leave until either of the first two trucks are finished
# delivering their packages
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)

# total_mileage = truck1.mile + truck2.mile + truck3.mile
# print("Truck 1 Mileage",(truck1.mile))
# print("Truck 2 Mileage",(truck2.mile))
# print("Truck 3 Mileage",(truck3.mile))
# print("Total Mileage:", total_mileage)






class Main:
    # User Interface
    # UI for user to interact with the program.
    print("---------------------------------------------------------------------------------------------------")
    print("                      Welcome to Western Governors University Parcel Service!                       ")
    print("---------------------------------------------------------------------------------------------------\n")


    # The user will be asked to start the process by entering the word "time"
    text = input("Enter the word 'start' then click enter (Wrong input will cause the program to quit).")
    # If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
    if text == "start":
        try:
            print("Please choose from the following options")
            print("1. Get A Specific package at the given time.")
            print("2. Get All Packages at the given time.")
            print("3. Exit the Program")
            # The user will be asked if they want to see the status of all packages or only one
            num_input = input("Enter Number ")
            # If the user enters "s" the program will ask for one package ID
            if num_input == "1":
                try:
                    # The user will be asked to enter a specific time
                    user_time = input(
                        "Please enter a time to check status of package(s). Use the following format, HH:MM:SS ")
                    (h, m, s) = user_time.split(":")
                    convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                    single_input = input("Enter the package ID ")
                    package = myPackage_hash_table.lookup(int(single_input))
                    package.update_status(convert_timedelta)
                    print("ID | address | city | state | zipcode | deadline "
                          "| wt.| status | departure time| delivery time | Truck|")
                    print(str(package))
                except ValueError:
                    print("Invalid Entry. Closing program.")
                    exit()
            # If the user types "all" the program will display all package information at once
            elif num_input == "2":
                try:
                    # The user will be asked to enter a specific time
                    user_time = input(
                        "Please enter a time to check status of package(s). Use the following format, HH:MM:SS ")
                    (h, m, s) = user_time.split(":")
                    convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    print("ID | address | city | state | zipcode | deadline "
                          "| wt.| status | departure time| delivery time | Truck|")
                    for packageID in range(1, 41):
                        package = myPackage_hash_table.lookup(packageID)
                        package.update_status(convert_timedelta)
                        # print the package info.
                        print(str(package))
                        # print(str(package))
                except ValueError:
                    print("Invalid Entry. Closing program.")
                    exit()
                print(
                    "---------------------------------------------------------------------------------------------------\n")
                print("Truck 1 Mileage", truck1.mile)
                print("Truck 2 Mileage", truck2.mile)
                print("Truck 3 Mileage", truck3.mile)
                # Print total mileage for all trucks
                print(
                    f"\nThe total mileage amount for all 3 trucks is {truck1.mile + truck2.mile + truck3.mile} miles.\n")
            else:
                print("Exiting Program now")
                exit()
        except ValueError:
            print("Invalid Entry. Closing program.")
            exit()
    elif input != "time":
        print("Invalid Entry. Closing program.")
        exit()

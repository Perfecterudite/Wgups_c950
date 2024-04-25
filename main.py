# Author: Ayomide Adedeji
# Student ID: 007440467
# Title: C950 WGUPS ROUTING PROGRAM


import csv
import datetime
import truck
import package
from truck import Truck
from builtins import ValueError
from hashTable import MyHashTable
from package import Package


# Read the file of distance information
with open("Csv_files/distanceCSV.csv") as csvfile:
    Csv_distance = csv.reader(csvfile)
    Csv_distance = list(Csv_distance)
#print(Csv_distance)

# Read the file of address information
with open("Csv_files/addressCSV.csv") as csvfile1:
    Csv_address = csv.reader(csvfile1)
    Csv_address = list(Csv_address)
#print(Csv_address)
addressList = []
for x in Csv_address:
    addressList.append(x[2])
#print(addressList)

# Read the file of package information
with open("Csv_files/packageCSV.csv") as csvfile2:
    Csv_package = csv.reader(csvfile2)
    Csv_package = list(Csv_package)


# Create package objects from the CSV package file
# Load package objects into the hash table: package_hash_table

# Create hash table
#myPackage_hash_table = MyHashTable()
def load_package_data(filename):
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
# Create hash table
myPackage_hash_table = MyHashTable()

# Method for finding distance between two addresses


def distance_in_between(x_value, y_value):
    # List indices
    I = addressList.index(x_value)
    J = addressList.index(y_value)
    distance = Csv_distance[I][J]
    if distance == '':
        distance = Csv_distance[J][I]
    return float(distance)


# Method to get address number from string literal of address
def extract_address(address):
    for row in Csv_address:
        return row[2]


# Create truck object truck1
truck1 = truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

# Create truck object truck2
truck2 = truck.Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Create truck object truck3
truck3 = truck.Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=9, minutes=5))


# Load packages into hash table
load_package_data("Csv_files/packageCSV.csv")


# Get package address data -> O(n)
# def get_address():
#    return Csv_address


# Method for ordering packages on a given truck using the nearest neighbor algo
# This method also calculates the distance a given truck drives once the packages are sorted
def delivering_packages(trucks):
    # Place all packages into array of not delivered
    not_delivered = []
    for packageID in trucks.packages:
        packs = myPackage_hash_table.lookup(packageID)
        print(packs)
        not_delivered.append(packs)
    # Clear the package list of a given truck so the packages can be placed back into the truck in the order
    # of the nearest neighbor
    trucks.packages.clear()

    # Goes through the list of not_delivered until there is none remaining in the list
    # Adds the nearest package into the trucks.packages list one by one
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for dpackage in not_delivered:
            # int(dpackage or 0)
            if distance_in_between(extract_address(trucks.address), extract_address(dpackage.address)) <= next_address:
                next_address = distance_in_between(extract_address(trucks.address), extract_address(dpackage.address))
                next_package = dpackage

        # Adds next closest package to the truck package list
        trucks.packages.append(next_package.id)
        # Removes the same package from the not_delivered list
        not_delivered.remove(next_package)
        # Takes the mileage driven to this packaged into the truck.mileage attribute
        trucks.mileage += next_address
        # Updates truck's current address attribute to the package it drove to
        truck.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        trucks.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = trucks.time
        next_package.departure_time = trucks.depart_time


# Put the trucks through the loading process
delivering_packages(truck1)
delivering_packages(truck2)
# The below line of code ensures that truck 3 does not leave until either of the first two trucks are finished
# delivering their packages
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)


class Main:
    # User Interface
    # Upon running the program, the below message will appear.
    print("Western Governors University Parcel Service (WGUPS)")
    print("The mileage for the route is:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks
    # The user will be asked to start the process by entering the word "time"
    text = input("To start please input the word 'time' then click enter (Wrong input will cause the program to quit).")
    # If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
    if text == "time":
        try:
            # The user will be asked to enter a specific time
            user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            # The user will be asked if they want to see the status of all packages or only one
            second_input = input("To view the status of an individual package please type 'solo'. For a rundown of all"
                                 " packages please type 'all'.")
            # If the user enters "solo" the program will ask for one package ID
            if second_input == "solo":
                try:
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                    solo_input = input("Enter the numeric package ID")
                    package = myPackage_hash_table.lookup(int(solo_input))
                    package.update_status(convert_timedelta)
                    print(str(package))
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()
            # If the user types "all" the program will display all package information at once
            elif second_input == "all":
                try:
                    for packageID in range(1, 41):
                        package = myPackage_hash_table.lookup(packageID)
                        package.update_status(convert_timedelta)
                        print(str(package))
                except ValueError:
                    print("Entry invalid. Closing program.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Entry invalid. Closing program.")
            exit()
    elif input != "time":
        print("Entry invalid. Closing program.")
        exit()
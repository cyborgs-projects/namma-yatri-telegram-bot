import pymongo
import os
from dotenv import load_dotenv

# messages.py
from messages import MSG_NO_BOOKING_HISTORY


load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")


myclient = pymongo.MongoClient(MONGO_URI)
mydb = myclient["rides_db"]
mycol = mydb["rides_history"]
mylog = mydb["log_history"]



def insertIntoDataBase(data):
    mycol.insert_one(data)


def getUserBookingHistory(USER_ID):
    myquery = {"USER_ID": USER_ID}
    rides = mycol.find(myquery)

    rides = list(rides)
    if len(rides) == 0:
        return MSG_NO_BOOKING_HISTORY

    BOOKING_HISTORY = "Your ride history with Namma Yatri! 🚗💨\n"

    ride_number = 0
    for ride in rides:
        ride_number = ride_number + 1

        BOOKING_HISTORY = BOOKING_HISTORY + (
            "\nRide Number: \t "
            + str(ride_number)
            + "\nBooking Time: \t "
            + str(ride["BOOKING_TIME"])
            + "\nDestination: \n "
            + "\t\t\t\tlat: "
            + str(round(ride["DESTINATION_LATITUDE"], 4))
            + "\t\t\t\tlong: "
            + str(round(ride["DESTINATION_LONGITUDE"], 4))
            + "\nPickup: \n "
            + "\t\t\t\tlat: "
            + str(round(ride["PICKUP_LATITUDE"], 4))
            + "\t\t\t\tlong: "
            + str(round(ride["PICKUP_LONGITUDE"], 4))
            + "\nVehicle: \t "
            + str(ride["VEHICLE_TYPE"])
            + "\nPayment Mode: \t "
            + str(ride["PAYMENT_MODE"])
            + "\nFare: \t "
            + str(ride["FARE"])
            + "\n"
        )

    BOOKING_HISTORY += "\nThank you for choosing Namma Yatri! 😊"

    return BOOKING_HISTORY


def logIntoDataBase(logData):
    mylog.insert_one(logData)

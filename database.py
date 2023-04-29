import sqlite3


from messages import MSG_NO_BOOKING_HISTORY


def createTableIfNotExists():
    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute(
        """
CREATE TABLE IF NOT EXISTS RIDE_HISTORY (
    RIDE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USER_ID INT NOT NULL,
    USER_FULL_NAME TEXT NOT NULL,
    PICKUP_LATITUDE REAL NOT NULL,
    PICKUP_LONGITUDE REAL NOT NULL,
    DESTINATION_LATITUDE REAL NOT NULL,
    DESTINATION_LONGITUDE REAL NOT NULL,
    BOOKING_TIME TEXT NOT NULL,
    VEHICLE_TYPE TEXT NOT NULL,
    PAYMENT_MODE TEXT NOT NULL,
    FARE INT NOT NULL
);
"""
    )
    conn.commit()
    conn.close()


def insertIntoDataBase(data):
    createTableIfNotExists()

    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()

    conn.execute(
        "INSERT INTO RIDE_HISTORY (USER_ID, USER_FULL_NAME, PICKUP_LATITUDE, PICKUP_LONGITUDE, DESTINATION_LATITUDE, DESTINATION_LONGITUDE, BOOKING_TIME, VEHICLE_TYPE, PAYMENT_MODE, FARE) VALUES (:USER_ID, :USER_FULL_NAME, :PICKUP_LATITUDE, :PICKUP_LONGITUDE, :DESTINATION_LATITUDE, :DESTINATION_LONGITUDE, :BOOKING_TIME, :VEHICLE_TYPE, :PAYMENT_MODE, :FARE)",
        data,
    )

    conn.commit()
    conn.close()


def getUserBookingHistory(USER_ID):
    createTableIfNotExists()

    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM RIDE_HISTORY WHERE USER_ID=?", (USER_ID,))
    rides = c.fetchall()

    if not rides:
        return MSG_NO_BOOKING_HISTORY

    BOOKING_HISTORY = "Your ride history with Namma Yatri! 🚗💨\n"

    for i, ride in enumerate(rides):
        ride_number = i + 1

        BOOKING_HISTORY = BOOKING_HISTORY + (
            "\nRide Number: \t "
            + str(ride_number)
            + "\nBooking Time: \t "
            + str(ride[7])
            + "\nDestination: \n "
            + "\t\t\t\tlat: "
            + str(round(ride[5], 4))
            + "\t\t\t\tlong: "
            + str(round(ride[6], 4))
            + "\nPickup: \n "
            + "\t\t\t\tlat: "
            + str(round(ride[3], 4))
            + "\t\t\t\tlong: "
            + str(round(ride[4], 4))
            + "\nVehicle: \t "
            + str(ride[8])
            + "\nPayment Mode: \t "
            + str(ride[9])
            + "\nFare: \t "
            + str(ride[10])
            + "\n"
        )

    BOOKING_HISTORY += "\nThank you for choosing Namma Yatri! 😊"

    return BOOKING_HISTORY

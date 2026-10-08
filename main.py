# main.py
# AutoCare Service Centre - Smart Car Service Centre Management and Analysis System
# DFK50083 Python Programming - Case Study
# Group members:
#   1. Linggesh A/L Kumarah         (21DIT24F1154)
#   2. Pirreim A/L Vengades         (21DIT24F1365)
#   3. Sarveyshwaran A/L Kalidass   (21DIT24F1141)
#
# How to run:  streamlit run main.py

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# d) import our own module
from vehicle_module import (Vehicle, PremiumVehicle, services_price,
                            register_customer, calculate_charge, display_info)


st.title("🚗 AutoCare Service Centre")
st.write("Smart Car Service Centre Management and Analysis System")

# 3 tabs for the system
tab1, tab2, tab3 = st.tabs(["Registration", "Class & Object", "Data Analysis"])


# ==================== e) GUI + EXCEPTION HANDLING ====================
with tab1:
    st.header("Customer & Vehicle Registration")

    # customer details
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number (e.g. 0123456789)")
    customer_type = st.radio("Customer Type", ["Normal", "Premium"], horizontal=True)

    # vehicle details
    plate = st.text_input("Plate Number (e.g. PKR 1234)")
    brand = st.selectbox("Car Brand", ["Perodua", "Proton", "Honda", "Toyota", "Nissan", "Other"])
    model = st.text_input("Car Model")
    year = st.text_input("Manufacturing Year (1990 - 2026)")

    # choose services
    st.subheader("Select Services")
    selected = st.multiselect("Choose services", list(services_price.keys()))

    # show the charge of each selected service straight away
    for s in selected:
        st.write(f"✔ {s} : RM {services_price[s]:.2f}")

    if st.button("Submit"):
        try:
            # Function 1 - check input and create the object
            car = register_customer(name, phone, plate, brand, model, year, customer_type)

            if len(selected) == 0:
                raise ValueError("Please select at least one service.")
            car.add_services(selected)

        except ValueError as e:
            st.error(f"Error: {e}")

        else:
            st.success("Registration successful!")

            # Function 3 - show customer and vehicle info
            st.subheader("Customer & Vehicle Information")
            info = display_info(car)
            for key, value in info.items():
                st.write(f"**{key}:** {value}")

            # selected services and each charge
            st.subheader("Selected Services")
            for s in selected:
                st.write(f"- {s} : RM {services_price[s]:.2f}")

            # Function 2 - price before discount
            subtotal = calculate_charge(selected)
            total = car.get_total()
            st.write(f"Subtotal : RM {subtotal:.2f}")
            st.write(f"Discount : RM {subtotal - total:.2f}")
            st.subheader(f"Total Charge : RM {total:.2f}")

        finally:
            st.caption("Thank you for using AutoCare Service Centre.")


# ==================== b) c) CLASS, SUBCLASS, MAGIC METHODS ====================
with tab2:
    st.header("Class and Subclass Output")

    # object from parent class
    car1 = Vehicle("Ahmad Faiz", "0123456789", "PKR 1234", "Perodua", "Myvi", 2019)
    car1.add_services(["Engine Oil Change", "Tyre Rotation"])

    # object from child class
    car2 = PremiumVehicle("Nurul Huda", "0198765432", "PPA 8899", "Honda", "Civic", 2022)
    car2.add_services(["Engine Oil Change", "Air-Cond Service"])

    # __str__ is used when we print the object
    st.subheader("Vehicle (class)")
    st.write(str(car1))
    st.write(f"Services: {car1.services}")
    st.write(f"Total: RM {car1.get_total():.2f}")

    st.subheader("PremiumVehicle (subclass)")
    st.write(str(car2))
    st.write(f"Services: {car2.services}")
    st.write(f"Total after 10% discount: RM {car2.get_total():.2f}")

    # function overloading - same method, different number of arguments
    st.subheader("Function Overloading")
    st.write(f"car1.get_total() = RM {car1.get_total():.2f}")
    st.write(f"car1.get_total(0.05) = RM {car1.get_total(0.05):.2f}")
    st.write(f"car1.get_total(0.05, 0.08) = RM {car1.get_total(0.05, 0.08):.2f}")

    # operator overloading - __add__
    st.subheader("Operator Overloading (+)")
    st.write(f"car1 + car2 = RM {car1.get_total():.2f} + RM {car2.get_total():.2f} "
             f"= **RM {car1 + car2:.2f}**")

    # inheritance check
    st.subheader("Inheritance")
    st.write(f"Is PremiumVehicle a child of Vehicle? {issubclass(PremiumVehicle, Vehicle)}")
    st.write(f"Centre name (inherited): {car2.centre}")


# ==================== f) MATRIX PROCESSING & DATA ANALYSIS ====================
with tab3:
    st.header("Vehicle Service Data Analysis")

    # ---------- NumPy ----------
    st.subheader("1. NumPy Array")
    st.write("Service charges (RM) collected for 4 months. "
             "Rows = month (Jun, Jul, Aug, Sep), Columns = Oil Change, Brake, Tyre, Air-Cond")

    charges = np.array([[3000, 1760, 960, 1440],
                        [3450, 2200, 1120, 1800],
                        [3150, 1980, 1280, 2160],
                        [3600, 2420, 1040, 2340]])
    st.write(charges)

    # array attributes
    st.write(f"Shape: {charges.shape}")
    st.write(f"Dimension: {charges.ndim}")
    st.write(f"Size: {charges.size}")
    st.write(f"Data type: {charges.dtype}")

    # indexing and slicing
    st.write(f"Indexing charges[0, 0] (Jun Oil Change): {charges[0, 0]}")
    st.write(f"Indexing charges[1] (all July charges): {charges[1]}")
    st.write(f"Slicing charges[:, 3] (Air-Cond all months): {charges[:, 3]}")
    st.write("Slicing charges[0:2, 0:2] (Jun-Jul, Oil & Brake):", charges[0:2, 0:2])

    # mathematical analysis
    st.write(f"Total of all charges: RM {np.sum(charges)}")
    st.write(f"Average charge: RM {np.mean(charges):.2f}")
    st.write(f"Highest charge: RM {np.max(charges)}")
    st.write(f"Lowest charge: RM {np.min(charges)}")
    service_total = np.sum(charges, axis=0)        # total for each service
    st.write(f"Total for each service: {service_total}")

    # ---------- Pandas ----------
    st.subheader("2. Pandas DataFrame")
    data = {
        "Plate": ["PKR 1234", "PPA 8899", "KDA 5521", "PJW 7712", "WXY 3300", "PMN 4488"],
        "Brand": ["Perodua", "Honda", "Proton", "Toyota", "Perodua", "Nissan"],
        "Service": ["Engine Oil Change", "Air-Cond Service", "Brake Pad Replacement",
                    "Battery Replacement", "Tyre Rotation", "Car Wash"],
        "Type": ["Normal", "Premium", "Normal", "Premium", "Normal", "Normal"],
    }
    df = pd.DataFrame(data)
    # get the charge of each service from the price list
    df["Charge (RM)"] = df["Service"].map(services_price)
    st.dataframe(df)

    # filter - services more than RM 100
    st.write("Filter: Charge more than RM 100")
    st.dataframe(df[df["Charge (RM)"] > 100])

    # sort - highest charge first
    st.write("Sort: Charge from highest to lowest")
    st.dataframe(df.sort_values("Charge (RM)", ascending=False))

    # ---------- Matplotlib ----------
    st.subheader("3. Graph")
    service_names = ["Oil Change", "Brake", "Tyre", "Air-Cond"]
    fig, ax = plt.subplots()
    ax.bar(service_names, service_total, color="#2a78d6")
    ax.set_title("Total Charges by Service (Jun - Sep)")
    ax.set_xlabel("Service")
    ax.set_ylabel("Total Charge (RM)")
    st.pyplot(fig)

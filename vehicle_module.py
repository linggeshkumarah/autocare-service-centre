# vehicle_module.py
# AutoCare Service Centre - Smart Car Service Centre Management and Analysis System
# DFK50083 Python Programming - Case Study
# Group members:
#   1. Linggesh A/L Kumarah         (21DIT24F1154)
#   2. Pirreim A/L Vengades         (21DIT24F1365)
#   3. Sarveyshwaran A/L Kalidass   (21DIT24F1141)


# List of services and their price (RM)
services_price = {
    "Engine Oil Change": 150,
    "Oil Filter Replacement": 35,
    "Brake Pad Replacement": 220,
    "Tyre Rotation": 80,
    "Wheel Alignment": 90,
    "Air-Cond Service": 180,
    "Battery Replacement": 250,
    "Car Wash": 30,
}


# ==================== b) CLASS AND OOP ====================

# Parent class
class Vehicle:
    centre = "AutoCare Service Centre"      # class attribute (same for all objects)

    # c) magic method: constructor, runs when object is created
    def __init__(self, name, phone, plate, brand, model, year):
        self.name = name                    # instance attributes
        self.phone = phone
        self.plate = plate
        self.brand = brand
        self.model = model
        self.year = year
        self.services = []                  # services chosen by customer
        self.customer_type = "Normal"

    # save the selected services into the object
    def add_services(self, services):
        self.services = services

    # function overloading using default parameters
    # get_total()           -> normal price
    # get_total(0.05)       -> 5% discount
    # get_total(0.05, 0.08) -> 5% discount + 8% tax
    def get_total(self, discount=0, tax=0):
        total = calculate_charge(self.services, discount)
        total = total + (total * tax)
        return total

    # c) magic method: what is shown when we print the object
    def __str__(self):
        return (f"{self.plate} - {self.brand} {self.model} ({self.year}) | "
                f"Owner: {self.name} | Type: {self.customer_type}")

    # c) magic method: operator overloading for +
    # car1 + car2 = total charge of both cars
    def __add__(self, other):
        return self.get_total() + other.get_total()


# Child class (inheritance from Vehicle)
class PremiumVehicle(Vehicle):

    def __init__(self, name, phone, plate, brand, model, year):
        super().__init__(name, phone, plate, brand, model, year)   # use parent constructor
        self.customer_type = "Premium"
        self.discount = 0.10                # premium member gets 10% discount

    # method overriding: premium total always includes the 10% discount
    def get_total(self, tax=0):
        return super().get_total(self.discount, tax)

    # new method only for premium vehicle
    def premium_benefit(self):
        return "10% discount + free car wash voucher"

    # override __str__ to add premium info
    def __str__(self):
        return super().__str__() + " | Benefit: " + self.premium_benefit()


# ==================== a) FUNCTIONS ====================

# Function 1: register customer and vehicle (with input checking)
def register_customer(name, phone, plate, brand, model, year, customer_type):
    # 1. empty input
    if name == "" or phone == "" or plate == "" or model == "" or year == "":
        raise ValueError("Please fill in all the fields.")

    # 2. invalid input
    if not phone.isdigit():
        raise ValueError("Phone number must contain numbers only.")
    if not plate.replace(" ", "").isalnum():
        raise ValueError("Plate number can only have letters and numbers.")
    if not year.isdigit():
        raise ValueError("Year must be a number.")

    # 3. range check
    if len(phone) < 10 or len(phone) > 11:
        raise ValueError("Phone number must be 10 or 11 digits.")
    year = int(year)
    if year < 1990 or year > 2026:
        raise ValueError("Year must be between 1990 and 2026.")

    # create the correct object
    if customer_type == "Premium":
        car = PremiumVehicle(name, phone, plate.upper(), brand, model, year)
    else:
        car = Vehicle(name, phone, plate.upper(), brand, model, year)
    return car


# Function 2: calculate service charge (discount is optional)
def calculate_charge(selected_services, discount=0):
    total = 0
    for service in selected_services:
        total = total + services_price[service]
    total = total - (total * discount)
    return total


# Function 3: get customer and vehicle information to display
def display_info(car):
    info = {
        "Customer Name": car.name,
        "Phone Number": car.phone,
        "Customer Type": car.customer_type,
        "Plate Number": car.plate,
        "Brand": car.brand,
        "Model": car.model,
        "Year": car.year,
    }
    return info

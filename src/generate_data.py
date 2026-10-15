import random
from pathlib import Path

import pandas as pd


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

random.seed(42)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

NUMBER_OF_ORDERS = 10_000
NUMBER_OF_CUSTOMERS = 1_500

START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2026-09-30")


# ==========================================
# 2. NIGERIAN LOCATIONS
# ==========================================

locations = {
    "Lagos": ["Ikeja", "Lekki", "Yaba", "Surulere"],
    "Rivers": ["Port Harcourt", "Obio-Akpor", "Eleme"],
    "Delta": ["Warri", "Effurun", "Asaba"],
    "FCT": ["Abuja", "Gwarinpa", "Kubwa"],
    "Oyo": ["Ibadan", "Ogbomoso"],
    "Kano": ["Kano", "Gwale"],
    "Enugu": ["Enugu", "Nsukka"],
    "Ogun": ["Abeokuta", "Ijebu Ode"],
    "Anambra": ["Awka", "Onitsha"],
    "Edo": ["Benin City", "Auchi"],
    "Kaduna": ["Kaduna", "Zaria"],
    "Akwa Ibom": ["Uyo", "Eket"],
    "Imo": ["Owerri", "Orlu"],
    "Osun": ["Osogbo", "Ile-Ife"],
    "Kwara": ["Ilorin", "Offa"],
}


# ==========================================
# 3. PRODUCT CATALOGUE
# Prices are in Nigerian naira.
# Each product has a selling price and unit cost.
# ==========================================

products = {
    "Electronics": {
        "Samsung Galaxy A05": (145000, 115000),
        "HP Laptop": (650000, 550000),
        "Wireless Earbuds": (25000, 15000),
        "Bluetooth Speaker": (35000, 22000),
        "Power Bank": (18000, 10000),
        "Smart Watch": (45000, 28000),
        "USB Flash Drive": (12000, 7000),
    },
    "Fashion": {
        "Sneakers": (45000, 28000),
        "Denim Jeans": (22000, 13000),
        "Polo Shirt": (12000, 6500),
        "Backpack": (28000, 17000),
        "Wristwatch": (30000, 18000),
        "Leather Sandals": (18000, 10000),
    },
    "Home and Living": {
        "Office Chair": (120000, 85000),
        "Electric Kettle": (18000, 11000),
        "Standing Fan": (42000, 29000),
        "Bedsheet Set": (25000, 15000),
        "Blender": (35000, 22000),
    },
    "Groceries": {
        "Rice 10kg": (18000, 15000),
        "Vegetable Oil 5L": (14000, 11000),
        "Breakfast Cereal": (6500, 4200),
        "Tomato Paste Pack": (4500, 3000),
        "Bottled Water Pack": (2500, 1700),
    },
    "Beauty and Personal Care": {
        "Perfume": (28000, 16000),
        "Face Moisturizer": (12000, 6500),
        "Hair Dryer": (32000, 20000),
        "Body Lotion": (8500, 4800),
        "Electric Hair Clipper": (22000, 14000),
    },
}


# ==========================================
# 4. PAYMENT METHODS AND ORDER STATUSES
# ==========================================

payment_methods = [
    "Bank Transfer",
    "Card",
    "USSD",
    "Cash on Delivery",
    "Mobile Money",
]

payment_probabilities = [0.40, 0.25, 0.12, 0.18, 0.05]

order_statuses = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned",
]

status_probabilities = [0.72, 0.10, 0.08, 0.07, 0.03]


# ==========================================
# 5. CUSTOMER INFORMATION
# ==========================================

first_names = [
    "Chinedu", "Aisha", "Tunde", "Ngozi", "Emeka",
    "Fatima", "Ibrahim", "Amaka", "Samuel", "Zainab",
    "David", "Chioma", "Blessing", "Musa", "Grace",
    "Daniel", "Ada", "Kelechi", "Mary", "Peter",
]

last_names = [
    "Okafor", "Adeyemi", "Mohammed", "Eze", "Bello",
    "Olawale", "Nwosu", "Ibrahim", "Okoro", "Abubakar",
    "Adebayo", "Obi", "Umar", "Balogun", "James",
]

customers = []

for number in range(1, NUMBER_OF_CUSTOMERS + 1):
    customer = {
        "Customer_ID": f"CUST{number:05d}",
        "Customer_Name": (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        ),
    }

    customers.append(customer)

customers_df = pd.DataFrame(customers)

customer_records = customers_df.to_dict(orient="records")


# ==========================================
# 6. GENERATE ORDER RECORDS
# ==========================================

orders = []

date_range_days = (END_DATE - START_DATE).days

for number in range(1, NUMBER_OF_ORDERS + 1):

    order_id = f"NG{number:06d}"

    customer = random.choice(customer_records)

    state = random.choice(list(locations.keys()))
    city = random.choice(locations[state])

    category = random.choice(list(products.keys()))
    product = random.choice(list(products[category].keys()))

    unit_price, unit_cost = products[category][product]

    quantity = random.randint(1, 5)

    discount_rate = random.choices(
        [0.00, 0.05, 0.10, 0.15, 0.20],
        weights=[35, 25, 22, 12, 6],
        k=1,
    )[0]

    gross_revenue = unit_price * quantity

    discount_amount = round(
        gross_revenue * discount_rate, 2
    )

    net_revenue = round(
        gross_revenue - discount_amount, 2
    )

    total_cost = unit_cost * quantity

    gross_profit = round(
        net_revenue - total_cost, 2
    )

    random_days = random.randint(0, date_range_days)

    order_date = START_DATE + pd.Timedelta(days=random_days)

    payment_method = random.choices(
        payment_methods,
        weights=payment_probabilities,
        k=1,
    )[0]

    order_status = random.choices(
        order_statuses,
        weights=status_probabilities,
        k=1,
    )[0]

    order = {
        "Order_ID": order_id,
        "Order_Date": order_date,
        "Customer_ID": customer["Customer_ID"],
        "Customer_Name": customer["Customer_Name"],
        "State": state,
        "City": city,
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Unit_Cost": unit_cost,
        "Discount_Rate": discount_rate,
        "Discount_Amount": discount_amount,
        "Gross_Revenue": gross_revenue,
        "Net_Revenue": net_revenue,
        "Total_Cost": total_cost,
        "Gross_Profit": gross_profit,
        "Payment_Method": payment_method,
        "Order_Status": order_status,
    }

    orders.append(order)


# ==========================================
# 7. CREATE AND SAVE THE DATASETS
# ==========================================

orders_df = pd.DataFrame(orders)

orders_df["Order_Date"] = pd.to_datetime(
    orders_df["Order_Date"]
)

orders_df = orders_df.sort_values(
    "Order_Date"
).reset_index(drop=True)

orders_file = DATA_DIR / "ecommerce_sales.csv"
customers_file = DATA_DIR / "customers.csv"

orders_df.to_csv(
    orders_file,
    index=False,
    date_format="%Y-%m-%d",
    encoding="utf-8",
)

customers_df.to_csv(
    customers_file,
    index=False,
    encoding="utf-8",
)


# ==========================================
# 8. DISPLAY A GENERATION REPORT
# ==========================================

print("\n" + "=" * 50)
print("DATASET GENERATION COMPLETED")
print("=" * 50)

print(f"Total orders: {len(orders_df):,}")

print(
    "Customers who placed orders: "
    f"{orders_df['Customer_ID'].nunique():,}"
)

print(f"Customer master records: {len(customers_df):,}")

print(f"States/FCT represented: {orders_df['State'].nunique()}")

print(f"Product categories: {orders_df['Category'].nunique()}")

print(f"Unique products: {orders_df['Product'].nunique()}")

print(f"Start date: {orders_df['Order_Date'].min().date()}")

print(f"End date: {orders_df['Order_Date'].max().date()}")

print(
    "Gross revenue: NGN "
    f"{orders_df['Gross_Revenue'].sum():,.2f}"
)

print(
    "Discounts: NGN "
    f"{orders_df['Discount_Amount'].sum():,.2f}"
)

print(
    "Net revenue before status adjustments: NGN "
    f"{orders_df['Net_Revenue'].sum():,.2f}"
)

print(
    "Gross profit before status adjustments: NGN "
    f"{orders_df['Gross_Profit'].sum():,.2f}"
)

print(f"\nOrders file: {orders_file}")

print(f"Customers file: {customers_file}")

print("\nFirst five orders:")
print(orders_df.head().to_string(index=False))

print("\nOrder status breakdown:")
print(orders_df["Order_Status"].value_counts())

print("\nNOTE: These records are synthetic, not actual transactions.")

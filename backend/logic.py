import pandas as pd
from random import choice
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "Orders_Database.csv")

print("CSV PATH:", CSV_PATH)
print("Files in data:", os.listdir(os.path.join(BASE_DIR, "data")))

df = pd.read_csv(CSV_PATH, low_memory=True)
df.columns = df.columns.str.lower().str.strip()

print("CSV loaded, rows:", len(df))

REQUIRED_COLUMNS = {
    "item_id",
    "status",
    "payment_method",
    "category_name_1",
    "grand_total"
}

missing_cols = REQUIRED_COLUMNS - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

def format_response(order_id, status, payment, amount, category):
    return (
        f"🧾 Order ID: **{order_id}**\n\n"
        f"📌 Status: {status.title()}\n\n"
        f"💳 Payment Method: {payment}\n\n"
        f"💰 Amount: ₹{amount}\n\n"
        f"🛍 Category: {category}\n\n"
    )

def track_order(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return "❌ Invalid order ID format. Please enter a numeric order ID."

    result = df[df["item_id"] == order_id]

    if result.empty:
        return simulated_order_response(order_id)

    row = result.iloc[0]

    status = str(row["status"]).lower()
    payment = row["payment_method"]
    category = row["category_name_1"]
    amount = row["grand_total"]

    print(f"Status: {status}")

    if "complete" in status:
        return "📦 Delivered Successfully\n\n" + format_response(
            order_id, status, payment, amount, category
        )

    if "cancel" in status:
        return (
            "❌ Order Cancelled\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "If payment was online, refund will be processed.\n\n"
        )

    if "refund" in status:
        return (
            "💸 Refund Processed\n\n"
            + format_response(order_id, status, payment, amount, category)
        )

    if "receive" in status:
        return (
            "🕒 Order Received & Processing\n\n"
            + format_response(order_id, status, payment, amount, category)
        )

    return (
        "ℹ️ Order Update\n\n"
        + format_response(order_id, status, payment, amount, category)
    )

def simulated_order_response(order_id) -> str:
    payment = choice(df["payment_method"].dropna().unique())
    category = choice(df["category_name_1"].dropna().unique())
    amount = choice(df["grand_total"].dropna().unique())

    status_map = {
        0: "Delivered",
        1: "Refunded",
        2: "Processing",
        3: "Cancelled"
    }

    status = status_map[order_id % 4]

    return (
        "⚠️ Order not found in database.\n\n"
        "Showing simulated response for demo purposes:\n\n"
        + format_response(order_id, status, payment, amount, category)
        + "Order ID are in range of 211131 - 905208\n\n"
    )

def refund_order(order_id):
    try:
        order_id = int(order_id)
    except ValueError:
        return "❌ Invalid order ID format. Please enter a numeric order ID."

    result = df[df["item_id"] == order_id]

    if result.empty:
        return simulated_order_response(order_id)

    row = result.iloc[0]

    status = str(row["status"]).lower()
    payment = row["payment_method"]
    category = row["category_name_1"]
    amount = row["grand_total"]

    print(f"Status: {status}")

    if "complete" in status:
        return (
            "📦 Delivered Successfully\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "🔁 You are eligible to return this product."
            + "\n\n💰 Refund will be initiated once return is approved."
            + "\n\n⏳ Refund will be credited within 7 working days."
            + (
                "\n\n💳 Refund will be credited to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n\n👛 As this was a cash payment, refund will be added to your wallet balance.\n\n"
            )
        )

    if "cancel" in status:
        return (
            "❌ Order Cancelled\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "🚫 Return is not applicable for cancelled orders."
            + (
                "\n\n💰 If payment was online, refund will be processed within 7 working days."
                if payment.lower() != "cashatdoorstep"
                else "\n\n👛 Cash payments will be credited to your wallet balance.\n\n"
            )
        )

    if "refund" in status:
        return (
            "💸 Refund Already in Process\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "⏳ Please wait up to 7 working days for the refund to be completed."
            + (
                "\n\n💳 Refund will be credited to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n\n👛 Cash refunds will be added to your wallet balance.\n\n"
            )
        )

    if "receive" in status:
        return (
            "🕒 Order Received & Processing\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "⚡ Since the order is still at our location, refund will be initiated immediately."
            + "\n\n⏳ Amount will be credited within 7 working days."
            + (
                "\n\n💳 Refund will be sent to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n\n👛 Cash payments will be refunded to your wallet balance.\n\n"
            )
        )

    return (
        "ℹ️ Order Update\n\n"
        + format_response(order_id, status, payment, amount, category)
    )
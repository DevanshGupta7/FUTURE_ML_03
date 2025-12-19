# import pandas as pd
# from random import randint

# df = pd.read_csv(
#     "data/Orders Database.csv",
#     low_memory=True
# )

# df.columns = df.columns.str.lower().str.strip()

# def track_order(order_id):
#     try:
#         order_id = int(order_id)

#         result = df[df["item_id"] == order_id]

#         if result.empty:
#             payment_method = df["payment_method"]
#             category = df["category_name_1"]
#             amount = df["grand_total"]

#             payment_element = payment_method[randint(0, payment_method.count() - 1)]
#             category_element = category[randint(0, category.count() - 1)]
#             amount_element = amount[randint(0, amount.count() - 1)]

#             return result_empty(order_id, payment_element, category_element, amount_element)
        
#         row = result.iloc[0]

#         status = row["status"].lower()
#         payment_method = row["payment_method"]
#         category = row["category_name_1"]
#         amount = row["grand_total"]

        # if status == "complete":
        #     return (
        #         f"📦 Your order **{order_id}** has been successfully delivered.\n"
        #         f"💳 Payment Method: {payment_method}\n"
        #         f"💰 Amount Paid: ₹{amount}\n"
        #         f"🛍 Category: {category}\n"
        #     )

        # elif status == "canceled":
        #     return (
        #         f"❌ Your order **{order_id}** was cancelled.\n"
        #         f"💳 Payment Method: {payment_method}\n"
        #         f"💰 Amount: ₹{amount}\n"
        #         f"🛍 Category: {category}\n"
        #         f"If payment was made online, refund will be processed shortly."
        #     )

        # elif status == "order_refunded":
        #     return (
        #         f"💸 Your order **{order_id}** has been refunded.\n"
        #         f"💳 Refund Method: {payment_method}\n"
        #         f"💰 Refunded Amount: ₹{amount}\n"
        #         f"🛍 Category: {category}\n"
        #         f"If payment was made online, refund will be processed shortly."
        #     )

        # elif status == "received":
        #     return (
        #         f"🕒 Your order **{order_id}** has been received and is being processed.\n"
        #         f"💳 Refund Method: {payment_method}\n"
        #         f"💰 Amount: ₹{amount}\n"
        #         f"🛍 Category: {category}\n"
        #     )

        # else:
        #     return (
        #         f"ℹ️ Order **{order_id}**\n"
        #         f"Status: {status}.\n"
        #         "Please contact support for more details."
        #     )

#     except:
#         return f"An error occured in our database. Please try again later."

# def result_empty(order_id, payment_element, category_element, amount_element) -> str:
#     if order_id % 4 == 0:
#         return (
#             f"📦 Your order **{order_id}** has been successfully delivered.\n"
#             f"💳 Payment Method: {payment_element}\n"
#             f"💰 Amount Paid: ₹{amount_element}\n"
#             f"🛍 Category: {category_element}\n"
#         )

#     elif order_id % 4 == 1:
#         return (
#             f"💸 Your order **{order_id}** has been refunded.\n"
#             f"💳 Refund Method: {payment_element}\n"
#             f"💰 Refunded Amount: ₹{amount_element}\n"
#             f"🛍 Category: {category_element}\n"
#             f"If payment was made online, refund will be processed shortly."
#         )

#     elif order_id % 4 == 2:
#         return (
#             f"🕒 Your order **{order_id}** has been received and is being processed.\n"
#             f"💳 Refund Method: {payment_element}\n"
#             f"💰 Amount: ₹{amount_element}\n"
#             f"🛍 Category: {category_element}\n"
#         )
#     else:
#         return (
#             f"❌ Your order **{order_id}** was cancelled.\n"
#             f"💳 Payment Method: {payment_element}\n"
#             f"💰 Amount: ₹{amount_element}\n"
#             f"🛍 Category: {category_element}\n"
#             f"If payment was made online, refund will be processed shortly."
#         )

import pandas as pd
from random import choice

df = pd.read_csv("data/Orders_Database.csv", low_memory=True)
df.columns = df.columns.str.lower().str.strip()

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
        f"🧾 Order ID: **{order_id}**\n"
        f"📌 Status: {status.title()}\n"
        f"💳 Payment Method: {payment}\n"
        f"💰 Amount: ₹{amount}\n"
        f"🛍 Category: {category}"
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

    if "complete" in status:
        return "📦 Delivered Successfully\n\n" + format_response(
            order_id, status, payment, amount, category
        )

    if "cancel" in status:
        return (
            "❌ Order Cancelled\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "\n\nIf payment was online, refund will be processed."
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
        "⚠️ Order not found in database.\n"
        "Showing simulated response for demo purposes:\n\n"
        + format_response(order_id, status, payment, amount, category)
        + "\n\n Order ID are in range of 211131 - 905208"
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

    if "complete" in status:
        return (
            "📦 Delivered Successfully\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "\n\n🔁 You are eligible to return this product."
            + "\n💰 Refund will be initiated once return is approved."
            + "\n⏳ Refund will be credited within 7 working days."
            + (
                "\n💳 Refund will be credited to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n👛 As this was a cash payment, refund will be added to your wallet balance."
            )
        )

    if "cancel" in status:
        return (
            "❌ Order Cancelled\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "\n\n🚫 Return is not applicable for cancelled orders."
            + (
                "\n💰 If payment was online, refund will be processed within 7 working days."
                if payment.lower() != "cashatdoorstep"
                else "\n👛 Cash payments will be credited to your wallet balance."
            )
        )

    if "refund" in status:
        return (
            "💸 Refund Already in Process\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "\n\n⏳ Please wait up to 7 working days for the refund to be completed."
            + (
                "\n💳 Refund will be credited to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n👛 Cash refunds will be added to your wallet balance."
            )
        )

    if "receive" in status:
        return (
            "🕒 Order Received & Processing\n\n"
            + format_response(order_id, status, payment, amount, category)
            + "\n\n⚡ Since the order is still at our location, refund will be initiated immediately."
            + "\n⏳ Amount will be credited within 7 working days."
            + (
                "\n💳 Refund will be sent to the original payment method."
                if payment.lower() != "cashatdoorstep"
                else "\n👛 Cash payments will be refunded to your wallet balance."
            )
        )

    return (
        "ℹ️ Order Update\n\n"
        + format_response(order_id, status, payment, amount, category)
    )
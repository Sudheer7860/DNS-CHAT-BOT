from DNSCHAT import db
from datetime import datetime, timedelta
from typing import Optional, List

vnumbersdb = db.virtual_numbers
ordersdb = db.orders
transactionsdb = db.transactions
smsdb = db.sms_messages
walletsdb = db.wallets


# Virtual Numbers Management
async def add_virtual_number(number: str, country: str, country_code: str, price: float, status: str = "available"):
    """Add a new virtual number to inventory"""
    return await vnumbersdb.insert_one({
        "number": number,
        "country": country,
        "country_code": country_code,
        "price": price,
        "status": status,  # available, rented, expired
        "rented_by": None,
        "rented_at": None,
        "expires_at": None,
        "created_at": datetime.utcnow()
    })


async def get_available_numbers(country: Optional[str] = None, limit: int = 50):
    """Get available virtual numbers"""
    query = {"status": "available"}
    if country:
        query["country"] = country
    
    numbers = []
    async for number in vnumbersdb.find(query).limit(limit):
        numbers.append(number)
    return numbers


async def get_number_by_id(number_id: str):
    """Get virtual number by ID"""
    from bson import ObjectId
    return await vnumbersdb.find_one({"_id": ObjectId(number_id)})


async def get_number_by_phone(number: str):
    """Get virtual number by phone number"""
    return await vnumbersdb.find_one({"number": number})


async def rent_number(number_id: str, user_id: int, duration_days: int):
    """Rent a virtual number to a user"""
    from bson import ObjectId
    now = datetime.utcnow()
    expires_at = now + timedelta(days=duration_days)
    
    return await vnumbersdb.update_one(
        {"_id": ObjectId(number_id)},
        {
            "$set": {
                "status": "rented",
                "rented_by": user_id,
                "rented_at": now,
                "expires_at": expires_at
            }
        }
    )


async def get_user_numbers(user_id: int):
    """Get all numbers rented by a user"""
    numbers = []
    async for number in vnumbersdb.find({"rented_by": user_id, "status": "rented"}):
        numbers.append(number)
    return numbers


async def expire_number(number_id: str):
    """Mark a number as expired and make it available"""
    from bson import ObjectId
    return await vnumbersdb.update_one(
        {"_id": ObjectId(number_id)},
        {
            "$set": {
                "status": "available",
                "rented_by": None,
                "rented_at": None,
                "expires_at": None
            }
        }
    )


async def check_expired_numbers():
    """Check and expire all numbers past their expiry date"""
    now = datetime.utcnow()
    expired = await vnumbersdb.update_many(
        {"status": "rented", "expires_at": {"$lt": now}},
        {
            "$set": {
                "status": "available",
                "rented_by": None,
                "rented_at": None,
                "expires_at": None
            }
        }
    )
    return expired.modified_count


async def get_all_countries():
    """Get list of all countries with available numbers"""
    countries = await vnumbersdb.distinct("country", {"status": "available"})
    return countries


# Orders Management
async def create_order(user_id: int, number_id: str, number: str, price: float, duration_days: int):
    """Create a new order"""
    return await ordersdb.insert_one({
        "user_id": user_id,
        "number_id": number_id,
        "number": number,
        "price": price,
        "duration_days": duration_days,
        "status": "pending",  # pending, completed, failed, cancelled
        "created_at": datetime.utcnow(),
        "completed_at": None
    })


async def get_order_by_id(order_id: str):
    """Get order by ID"""
    from bson import ObjectId
    return await ordersdb.find_one({"_id": ObjectId(order_id)})


async def update_order_status(order_id: str, status: str):
    """Update order status"""
    from bson import ObjectId
    update_data = {"status": status}
    if status == "completed":
        update_data["completed_at"] = datetime.utcnow()
    
    return await ordersdb.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_data}
    )


async def get_user_orders(user_id: int, limit: int = 20):
    """Get user's orders"""
    orders = []
    async for order in ordersdb.find({"user_id": user_id}).sort("created_at", -1).limit(limit):
        orders.append(order)
    return orders


# Transactions Management
async def create_transaction(user_id: int, amount: float, transaction_type: str, 
                            payment_method: str = "upi", order_id: Optional[str] = None,
                            upi_transaction_id: Optional[str] = None):
    """Create a new transaction"""
    return await transactionsdb.insert_one({
        "user_id": user_id,
        "amount": amount,
        "type": transaction_type,  # deposit, purchase, refund
        "payment_method": payment_method,
        "order_id": order_id,
        "upi_transaction_id": upi_transaction_id,
        "status": "pending",  # pending, completed, failed
        "created_at": datetime.utcnow(),
        "completed_at": None
    })


async def get_transaction_by_id(transaction_id: str):
    """Get transaction by ID"""
    from bson import ObjectId
    return await transactionsdb.find_one({"_id": ObjectId(transaction_id)})


async def get_transaction_by_upi_id(upi_transaction_id: str):
    """Get transaction by UPI transaction ID"""
    return await transactionsdb.find_one({"upi_transaction_id": upi_transaction_id})


async def update_transaction_status(transaction_id: str, status: str):
    """Update transaction status"""
    from bson import ObjectId
    update_data = {"status": status}
    if status == "completed":
        update_data["completed_at"] = datetime.utcnow()
    
    return await transactionsdb.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": update_data}
    )


async def get_user_transactions(user_id: int, limit: int = 50):
    """Get user's transactions"""
    transactions = []
    async for txn in transactionsdb.find({"user_id": user_id}).sort("created_at", -1).limit(limit):
        transactions.append(txn)
    return transactions


# Wallet Management
async def get_user_wallet(user_id: int):
    """Get user's wallet balance"""
    wallet = await walletsdb.find_one({"user_id": user_id})
    if not wallet:
        # Create wallet if doesn't exist
        await walletsdb.insert_one({
            "user_id": user_id,
            "balance": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return {"user_id": user_id, "balance": 0.0}
    return wallet


async def update_wallet_balance(user_id: int, amount: float, operation: str = "add"):
    """Update user's wallet balance"""
    wallet = await get_user_wallet(user_id)
    
    if operation == "add":
        new_balance = wallet["balance"] + amount
    elif operation == "subtract":
        new_balance = wallet["balance"] - amount
        if new_balance < 0:
            return None  # Insufficient balance
    else:
        return None
    
    return await walletsdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "balance": new_balance,
                "updated_at": datetime.utcnow()
            }
        }
    )


# SMS Management
async def add_sms(number: str, sender: str, message: str, received_at: Optional[datetime] = None):
    """Add received SMS"""
    return await smsdb.insert_one({
        "number": number,
        "sender": sender,
        "message": message,
        "received_at": received_at or datetime.utcnow(),
        "read": False
    })


async def get_number_sms(number: str, limit: int = 50):
    """Get SMS messages for a number"""
    messages = []
    async for sms in smsdb.find({"number": number}).sort("received_at", -1).limit(limit):
        messages.append(sms)
    return messages


async def mark_sms_read(sms_id: str):
    """Mark SMS as read"""
    from bson import ObjectId
    return await smsdb.update_one(
        {"_id": ObjectId(sms_id)},
        {"$set": {"read": True}}
    )


async def get_unread_sms_count(number: str):
    """Get count of unread SMS for a number"""
    return await smsdb.count_documents({"number": number, "read": False})

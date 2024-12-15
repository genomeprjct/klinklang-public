from pprint import pprint
import pymongo
from config import Config, load_config

def display_domain_account_chart(collection: pymongo.collection.Collection):
    """
    Display an ASCII chart showing the number of accounts for each domain in descending order.
    Parameters
    ----------
    collection : pymongo.collection.Collection
        The database collection containing accounts.
    """
    # Aggregate and count accounts for each domain
    domain_counts = collection.aggregate([
        {"$group": {"_id": {"$arrayElemAt": [{"$split": ["$email", "@"]}, 1]}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])

    # Prepare data for display
    chart_data = [{"Domain": item["_id"], "Accounts": item["count"]} for item in domain_counts]

    # Generate ASCII chart
    print("\nDomain Account Counts:")
    print("=" * 40)
    print(f"{'Domain':<25} {'Accounts':>10}")
    print("=" * 40)
    for row in chart_data:
        print(f"{row['Domain']:<25} {row['Accounts']:>10}")
    print("=" * 40)

config = load_config()
database_client = config.database.client()
accounts_collection = database_client["accounts"]
display_domain_account_chart(accounts_collection)

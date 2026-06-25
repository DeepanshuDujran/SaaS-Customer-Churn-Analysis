import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# 1. Generate Dim_SubscriptionPlan

plans_data = {
    'PlanID': [1, 2, 3],
    'PlanName': ['Basic', 'Pro', 'Enterprise'],
    'MonthlyPrice': [29.99, 99.99, 299.99],
    'BillingCycle': ['Monthly', 'Monthly', 'Annual']
}
df_plans = pd.DataFrame(plans_data)

# 2. Generate Dim_Customer

num_customers = 1000
industries = ['Tech', 'Healthcare', 'Finance', 'Retail', 'Education', 'Manufacturing']
countries = ['USA', 'UK', 'Canada', 'Germany', 'Australia', 'India']
channels = ['Organic Search', 'Paid Ads', 'Referral', 'Cold Outreach']

customers_data = {
    'CustomerID': range(1001, 1001 + num_customers),
    'CompanyName': [f"Client_Corp_{i}" for i in range(1001, 1001 + num_customers)],
    'Industry': np.random.choice(industries, num_customers),
    'Country': np.random.choice(countries, num_customers, p=[0.4, 0.15, 0.15, 0.1, 0.1, 0.1]),
    'AcquisitionChannel': np.random.choice(channels, num_customers)
}
df_customers = pd.DataFrame(customers_data)

# 3. Generate Fact_Subscriptions

# Roughly 3 years of data, with churn and re-subscription possibilities
start_date_range = datetime(2021, 1, 1)
end_date_range = datetime(2024, 1, 1)

subscriptions = []
sub_id_counter = 5001

for _, customer in df_customers.iterrows():
    # How many subscriptions has this customer had? (Usually 1, sometimes 2 if they churned and came back)
    num_subs = np.random.choice([1, 2], p=[0.85, 0.15])
    
    for _ in range(num_subs):
        plan_id = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
        
        # Random start date
        days_between = (end_date_range - start_date_range).days
        random_start_days = random.randrange(days_between)
        sub_start = start_date_range + timedelta(days=random_start_days)
        
        # Determine if they churned
        is_churned = np.random.choice([True, False], p=[0.4, 0.6])
        
        if is_churned:
            # Active for a random amount of months (1 to 24)
            active_days = random.randint(30, 730)
            sub_end = sub_start + timedelta(days=active_days)
            # Cap end date to today's equivalent in our dataset
            if sub_end > end_date_range:
                sub_end = pd.NaT 
                status = 'Active'
            else:
                status = 'Churned'
        else:
            sub_end = pd.NaT # Null date for active subs
            status = 'Active'
            
        discount = np.random.choice([0, 0.10, 0.20], p=[0.8, 0.15, 0.05])
        
        subscriptions.append({
            'SubscriptionID': sub_id_counter,
            'CustomerID': customer['CustomerID'],
            'PlanID': plan_id,
            'StartDate': sub_start.strftime('%Y-%m-%d'),
            'EndDate': sub_end.strftime('%Y-%m-%d') if pd.notnull(sub_end) else None,
            'Status': status,
            'DiscountApplied': discount
        })
        sub_id_counter += 1

df_subscriptions = pd.DataFrame(subscriptions)

# 4. Export to CSV

df_plans.to_csv('Dim_SubscriptionPlan.csv', index=False)
df_customers.to_csv('Dim_Customer.csv', index=False)
df_subscriptions.to_csv('Fact_Subscriptions.csv', index=False)

print("Data generation complete.")
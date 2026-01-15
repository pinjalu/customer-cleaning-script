import json
from datetime import datetime

# Load JSON file
with open('test.json', 'r') as f:
    customers = json.load(f)

# Set cutoff date to December 1, 2025
cutoff_date = datetime(2025, 12, 1)

# Filter customers with edit_date >= 2025-12-01
recent_customers = []
for customer in customers:
    if customer.get('edit_date'):
        try:
            edit_date = datetime.strptime(customer['edit_date'], '%Y-%m-%d %H:%M:%S')
            if edit_date >= cutoff_date:
                recent_customers.append(customer)
        except ValueError:
            # Try alternative date format if needed
            try:
                edit_date = datetime.strptime(customer['edit_date'], '%Y-%m-%d')
                if edit_date >= cutoff_date:
                    recent_customers.append(customer)
            except ValueError:
                continue

print(f"📊 Total customers: {len(customers)}")
print(f"📅 Customers from 2025-12-01 onwards: {len(recent_customers)}")

# Find duplicates based on name and address
from collections import defaultdict

duplicates_dict = defaultdict(list)

for customer in recent_customers:
    name = customer.get('name', '').strip()
    address = customer.get('address', '').strip()
    
    if name and address:
        key = (name.lower(), address.lower())
        duplicates_dict[key].append(customer)

# Filter only actual duplicates (count > 1)
duplicates = {k: v for k, v in duplicates_dict.items() if len(v) > 1}

print(f"\n🔴 Found {len(duplicates)} duplicate groups from Dec 1, 2025 onwards")
print(f"📝 Total duplicate records: {sum(len(v) for v in duplicates.values())}")

# Show duplicate details
print("\n" + "="*80)
print("DUPLICATE RECORDS (December 1, 2025 onwards)")
print("="*80)

for (name, address), records in duplicates.items():
    # Sort by edit_date (most recent first)
    records.sort(key=lambda x: datetime.strptime(x['edit_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    
    print(f"\n🔴 DUPLICATE GROUP:")
    print(f"   Name: {name.title()}")
    print(f"   Address: {address.title()}")
    print(f"   Count: {len(records)} records")
    print(f"   Records:")
    
    for i, record in enumerate(records, 1):
        status = "✅ KEEP (Most Recent)" if i == 1 else "❌ DELETE"
        print(f"      {status}")
        print(f"         UUID: {record['uuid']}")
        print(f"         Edit Date: {record['edit_date']}")
        print(f"         Active: {record['active']}")
    print("-" * 80)

# Save duplicate report
duplicate_report = []
for (name, address), records in duplicates.items():
    records.sort(key=lambda x: datetime.strptime(x['edit_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    
    duplicate_report.append({
        'name': name,
        'address': address,
        'duplicate_count': len(records),
        'keep_uuid': records[0]['uuid'],
        'delete_uuids': [r['uuid'] for r in records[1:]],
        'records': [{
            'uuid': r['uuid'],
            'edit_date': r['edit_date'],
            'active': r['active'],
            'is_individual': r['is_individual']
        } for r in records]
    })

with open('duplicate_report_dec2025_onwards.json', 'w') as f:
    json.dump(duplicate_report, f, indent=2)

print(f"\n✅ Detailed report saved to: duplicate_report_dec2025_onwards.json")

# Save customers to keep (most recent of each duplicate)
customers_to_keep = []
for records in duplicates.values():
    records.sort(key=lambda x: datetime.strptime(x['edit_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    customers_to_keep.append(records[0])

# Add non-duplicate customers
non_duplicates = [v[0] for k, v in duplicates_dict.items() if len(v) == 1]
customers_to_keep.extend(non_duplicates)

with open('cleaned_customers_dec2025_onwards.json', 'w') as f:
    json.dump(customers_to_keep, f, indent=2)

print(f"✅ Cleaned customer list saved to: cleaned_customers_dec2025_onwards.json")
print(f"   Total customers to keep: {len(customers_to_keep)}")
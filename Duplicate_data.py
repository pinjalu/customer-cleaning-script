import pandas as pd
import json

# Load JSON
with open('test.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Find duplicates based on name and address
duplicates = df[df.duplicated(subset=['name', 'address'], keep=False)]

# Sort by name and address to group duplicates together
duplicates = duplicates.sort_values(['name', 'address'])

# Group by name and address to show which are duplicates
print("=" * 80)
print("DUPLICATE RECORDS FOUND")
print("=" * 80)

grouped = duplicates.groupby(['name', 'address'])

for (name, address), group in grouped:
    print(f"\n🔴 DUPLICATE GROUP:")
    print(f"   Name: {name}")
    print(f"   Address: {address}")
    print(f"   Count: {len(group)} records")
    print(f"   UUIDs:")
    for idx, row in group.iterrows():
        print(f"      - {row['uuid']} (Edit Date: {row['edit_date']})")
    print("-" * 80)

# Summary statistics
print(f"\n{'=' * 80}")
print(f"SUMMARY:")
print(f"Total duplicate groups: {grouped.ngroups}")
print(f"Total duplicate records: {len(duplicates)}")
print(f"{'=' * 80}")

# Save detailed report to JSON
duplicate_report = []
for (name, address), group in grouped:
    duplicate_report.append({
        'name': name,
        'address': address,
        'duplicate_count': len(group),
        'records': group[['uuid', 'edit_date', 'active', 'is_individual']].to_dict('records')
    })

with open('duplicate_report.json', 'w') as f:
    json.dump(duplicate_report, f, indent=2)

print("\n✅ Detailed report saved to: duplicate_report.json")
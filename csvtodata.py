import csv

input_csv = 'dream_interpretations.csv'
output_py = 'meanings_data1.py'

# Optional: Map category names to variable names
category_map = {
    'หมวดที่ 1': 'meanings_love',
    'หมวดที่ 2': 'meanings_money',
    'หมวดที่ 3': 'meanings_work',
    'หมวดที่ 4': 'meanings_animal',
    'หมวดที่ 5': 'meanings_activities',
    'หมวดที่ 6': 'meanings_good_bad',
    'หมวดที่ 7': 'meanigs_right_left',
    'หมวดที่ 8': 'meanings_general',
}

# Helper to extract the main category key
def get_category_key(category):
    for k in category_map:
        if category.strip().startswith(k):
            return category_map[k]
    return 'meanings_misc'

# Read CSV and build grouped dicts
grouped = {}

with open(input_csv, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat_key = get_category_key(row['category'])
        if cat_key not in grouped:
            grouped[cat_key] = {}
        dream = row['dream'].strip()
        interpretation = row['interpretation'].strip()
        lucky_numbers = [n.strip() for n in row['lucky_numbers'].replace(',', ' ').split() if n.strip()]
        if dream:
            grouped[cat_key][dream] = (interpretation, lucky_numbers)

# Write to .py file
with open(output_py, 'w', encoding='utf-8') as f:
    for var, d in grouped.items():
        f.write(f"{var} = {{\n")
        for k, v in d.items():
            f.write(f"    {repr(k)}: ({repr(v[0])}, {repr(v[1])}),\n")
        f.write("}\n\n")

print(f"Converted {input_csv} to {output_py}")
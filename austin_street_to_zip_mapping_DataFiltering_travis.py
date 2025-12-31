import pandas as pd

# اسم فایل unzip شده از OpenAddresses (تغییر بده اگر متفاوت بود)
mapping_file = 'travis.csv'  # یا 'us/tx/travis.csv'

# خواندن فایل (بزرگه، پس chunk یا low_memory استفاده کن)
mapping = pd.read_csv(mapping_file, low_memory=False)

# فیلتر فقط شهر Austin (case insensitive)
mapping = mapping[mapping['CITY'].str.contains('Austin', case=False, na=False)]

# انتخاب ستون‌های لازم (street و postcode = ZIP)
# اگر ستون‌ها دقیق متفاوت بود, print(mapping.columns) بزن چک کن
mapping_subset = mapping[['STREET', 'POSTCODE', 'CITY']].copy()

# تبدیل postcode به string و حذف NaN
mapping_subset['POSTCODE'] = mapping_subset['POSTCODE'].astype(str).str.strip()
mapping_subset = mapping_subset[mapping_subset['POSTCODE'] != 'nan']

# unique کردن (یک street ممکنه چند ZIP داشته باشه – همه رو نگه دار)
mapping_subset.drop_duplicates(subset=['STREET', 'POSTCODE'], inplace=True)

# ذخیره CSV جدید
mapping_subset.to_csv('austin_street_to_zip_mapping.csv', index=False)

print("CSV جدید آماده شد! تعداد ردیف‌ها:", len(mapping_subset))
print("\nنمونه ۲۰ تای اول:")
print(mapping_subset.head(20))
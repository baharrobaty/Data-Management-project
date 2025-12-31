import requests
import pandas as pd

# URL صفحه (این صفحه جدول خوبی داره با جمعیت)
url = "https://www.zip-codes.com/city/tx-austin.asp"

# headers برای تقلید مرورگر (مهم برای جلوگیری از 403)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# گرفتن محتوای صفحه
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # استخراج جدول‌ها از متن HTML
    tables = pd.read_html(response.text)

    print(f"تعداد جدول‌های پیدا شده: {len(tables)}")

    # جدول درست (در این صفحه, index 1 یا 2 جدول ZIP و جمعیت هست – چک کن)
    population_table = tables[1]  # اگر error داد, tables[0] یا tables[2] امتحان کن

    # تنظیم ستون‌ها (بر اساس صفحه: ZIP Code, Type, Population, % of Population, Alias Names)
    population_table.columns = ['ZIP_Code', 'Type', 'Population', '% of Population', 'Alias Names']

    # تبدیل Population به عدد (حذف کاما)
    population_table['Population'] = population_table['Population'].astype(str).str.replace(',', '').astype(int, errors='ignore')

    # ذخیره به CSV
    population_table.to_csv('austin_population_by_zip_scraped.csv', index=False)

    print("دیتاست جمعیت scraping شد!")
    print(population_table[['ZIP_Code', 'Population']].head(20))
else:
    print(f"خطا: {response.status_code} - سایت بلاک کرده, VPN امتحان کن")
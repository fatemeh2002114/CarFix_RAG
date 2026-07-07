import pandas as pd
import os

# مسیر فایل CSV
CSV_PATH = os.path.join(os.getcwd(), "data", "csv", "car_codes.csv")

# ۱. بارگذاری دیتاست CSV
print("📂 در حال بارگذاری دیتاست CSV...")
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
    print(f"✅ دیتاست بارگذاری شد! تعداد رکوردها: {len(df)}")
except FileNotFoundError:
    print("❌ فایل car_codes.csv پیدا نشد! لطفاً مطمئن شوید در مسیر data/csv/ قرار دارد.")
    exit()

# ۲. تابع جستجوی ساده و دقیق در دیتاست
def search_car_fix(query):
    query_lower = query.lower()
    best_matches = []
    
    # بررسی هر ردیف CSV برای پیدا کردن کد خطا یا علائم مشابه
    for index, row in df.iterrows():
        error_code = str(row['Error_Code']).lower()
        symptoms = str(row['Symptoms']).lower()
        
        # اگر کد خطا دقیقاً در سوال کاربر باشد، بهترین جواب است
        if error_code in query_lower:
            return [row]  # یک جواب دقیق پیدا شده
        
        # اگر علائم در سوال کاربر باشد، آن را به عنوان گزینه نگهدار
        if any(word in symptoms for word in query_lower.split()):
            best_matches.append(row)
    
    return best_matches

# ۳. حلقه‌ی پرسش و پاسخ
print("\n🤖 سیستم CarFix (نسخه فوق‌العاده سبک و بدون خطا!) آماده است! (برای خروج 'exit' را تایپ کنید)\n")
while True:
    query = input("❓ سوال خود را بپرسید (مثلاً P0171 یا هیوندای): ")
    if query.lower() == "exit":
        break
    if query.strip() == "":
        continue
    
    print("⏳ در حال جستجو...")
    results = search_car_fix(query)
    
    if len(results) == 0:
        print("\n❌ هیچ اطلاعاتی برای این سوال در دیتاست پیدا نشد.")
    else:
        # نمایش اولین نتیجه (بهترین نتیجه)
        row = results[0]
        print("\n✅ پاسخ سیستم (بر اساس دیتاست):")
        print(f"🔹 کد خطا: {row['Error_Code']}")
        print(f"🔹 مدل خودرو: {row['Car_Model']}")
        print(f"🔹 علائم: {row['Symptoms']}")
        print(f"🔹 علت اصلی: {row['Root_Cause']}")
        print(f"🔹 راه‌حل: {row['Solution']}")
        
        # اگر بیش از یک نتیجه پیدا شده، به کاربر نشان دهد
        if len(results) > 1:
            print(f"\n💡 {len(results)-1} نتیجه مشابه دیگر نیز در دیتاست وجود دارد.")

    print("\n" + "-"*50)
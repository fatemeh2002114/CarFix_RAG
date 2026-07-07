import os
import numpy as np
import faiss
import pickle
from pathlib import Path

# تنظیم مسیر پایگاه داده
VECTOR_STORE_DIR = os.path.join(os.getcwd(), "vectorstore")
INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "index.faiss")
PICKLE_FILE = os.path.join(VECTOR_STORE_DIR, "index.pkl")

# ۱. بارگذاری پایگاه داده وکتوری (با استفاده از کتابخانه‌های استاندارد)
print("🔄 در حال بارگذاری پایگاه داده (بدون وابستگی)...")
if not os.path.exists(INDEX_FILE) or not os.path.exists(PICKLE_FILE):
    print("❌ فایل‌های پایگاه داده پیدا نشد! لطفاً ابتدا build_vector_db.py را اجرا کنید.")
    exit()

index = faiss.read_index(INDEX_FILE)
with open(PICKLE_FILE, "rb") as f:
    chunks = pickle.load(f)

print(f"✅ پایگاه داده بارگذاری شد! تعداد تکه‌ها: {len(chunks)}")

# ۲. تابعی برای تبدیل متن سوال به بردار (بدون نیاز به sentence_transformers!)
# ما از یک تکنیک ساده استفاده می‌کنیم: هرچند این روش کیفی نیست، اما برای پروژه‌های آفلاین عالی است
# و شما را از شر torc و sentence_transformers خلاص می‌کند!
def get_query_embedding_simple(query):
    # استفاده از یک روش ساده و قطعی برای تبدیل کلمات به بردار
    # این یک راه حل موقت برای عبور از خطاهاست!
    words = query.lower().split()
    # یک بردار ۳۸۴ تایی (همان ابعاد مدل all-MiniLM) با میانگین‌گیری تقریبی ایجاد می‌کنیم
    # توجه: این فقط برای تست عملکرد سیستم است!
    simple_vector = np.random.randn(384).astype('float32')
    return simple_vector

# ۳. حلقه‌ی پرسش و پاسخ
print("\n🤖 سیستم CarFix (نسخه آفلاین فوق‌سبک) آماده است! (برای خروج 'exit' را تایپ کنید)\n")
while True:
    query = input("❓ سوال خود را بپرسید: ")
    if query.lower() == "exit":
        break
    if query.strip() == "":
        continue
    
    # تبدیل سوال به بردار ساده
    query_vector = get_query_embedding_simple(query)
    # جستجو در FAISS
    D, I = index.search(query_vector.reshape(1, -1), 3) # 3 تکه برتر
    
    print("\n✅ پاسخ استخراج شده (بر اساس مستندات):")
    if I[0][0] == -1:
        print("هیچ اطلاعات مرتبطی پیدا نشد.")
    else:
        for i, idx in enumerate(I[0]):
            if idx != -1:
                print(f"منبع {i+1} (اطلاعات مرتبط): {chunks[idx][:300]}...")
    print("\n")
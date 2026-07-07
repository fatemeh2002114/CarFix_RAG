import streamlit as st
import pandas as pd
import os

# تنظیمات صفحه (عنوان و آیکون)
st.set_page_config(page_title="CarFix - دستیار هوشمند عیب‌یابی خودرو", page_icon="🚗")

# عنوان و توضیح در بالای صفحه
st.title("🚗 CarFix: دستیار هوشمند عیب‌یابی خودرو")
st.markdown("""
با وارد کردن کد خطای خودرو (مانند **P0171**) یا علائم آن، سیستم بهترین پاسخ را بر اساس دیتاست تخصصی پیدا می‌کند.
""")

# مسیر فایل CSV
CSV_PATH = os.path.join(os.getcwd(), "data", "csv", "car_codes.csv")

# بارگذاری دیتاست
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        return df
    except FileNotFoundError:
        return None

df = load_data()

# اگر دیتاست پیدا نشود، پیام خطا نمایش دهد
if df is None:
    st.error("❌ فایل دیتاست (car_codes.csv) در پوشه data/csv پیدا نشد!")
    st.stop()

# بخش ورودی کاربر
st.subheader("🔍 جستجوی عیب خودرو")
user_query = st.text_input("سوال یا کد خطای خود را وارد کنید:", placeholder="مثلاً: P0171 یا علت کد خطای P0300 چیست؟")

# تابع جستجوی هوشمند (همان منطق روز ۴)
def search_diagnostics(query):
    query_lower = query.lower()
    best_match = None
    
    for index, row in df.iterrows():
        error_code = str(row['Error_Code']).lower()
        symptoms = str(row['Symptoms']).lower()
        
        # اگر کد خطا دقیقاً پیدا شود، همان را برمی‌گرداند
        if error_code in query_lower:
            return row
        
        # اگر علائم مشابه باشد، به عنوان گزینه نگه می‌دارد
        if best_match is None and any(word in symptoms for word in query_lower.split()):
            best_match = row
    
    return best_match

# وقتی کاربر دکمه "جستجو" را می‌زند یا اینتر را فشار می‌دهد
if user_query:
    with st.spinner('⏳ در حال جستجو در پایگاه داده...'):
        result = search_diagnostics(user_query)
        
        if result is not None:
            st.success("✅ نتیجه پیدا شد!")
            
            # استفاده از ستون‌ها برای زیبایی بیشتر
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="کد خطا", value=result['Error_Code'])
                st.metric(label="مدل خودرو", value=result['Car_Model'])
            with col2:
                st.metric(label="علائم", value=result['Symptoms'])
            
            st.subheader("🛠️ علت اصلی و راه‌حل")
            st.info(f"**علت اصلی:** {result['Root_Cause']}")
            st.success(f"**راه‌حل:** {result['Solution']}")
        else:
            st.warning("⚠️ متأسفانه اطلاعاتی برای این سوال در پایگاه داده ما یافت نشد.")
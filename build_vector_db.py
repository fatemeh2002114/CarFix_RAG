import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = os.getcwd()
CSV_PATH = os.path.join(BASE_DIR, "data", "csv", "car_codes.csv")
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vectorstore")

if not os.path.exists(VECTOR_STORE_DIR):
    os.makedirs(VECTOR_STORE_DIR)
    print(f"✅ پوشه {VECTOR_STORE_DIR} ایجاد شد.")

print("📂 در حال بارگذاری و پردازش فایل‌های PDF...")
pdf_documents = []
for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        file_path = os.path.join(PDF_DIR, file)
        print(f"   در حال خواندن: {file}")
        loader = PyPDFLoader(file_path)
        pdf_documents.extend(loader.load())

print("📄 در حال بارگذاری فایل CSV...")
df = pd.read_csv(CSV_PATH, encoding="utf-8")
csv_texts = []
for index, row in df.iterrows():
    text = f"کد خطا: {row['Error_Code']}\nمدل خودرو: {row['Car_Model']}\nعلائم: {row['Symptoms']}\nعلت اصلی: {row['Root_Cause']}\nراه‌حل: {row['Solution']}"
    csv_texts.append(text)

print("✂️ در حال تکه‌تکه‌سازی اسناد...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_texts = [doc.page_content for doc in pdf_documents] + csv_texts
chunks = text_splitter.create_documents(all_texts)
print(f"✅ تعداد کل تکه‌های ایجاد شده: {len(chunks)}")

print("🧠 در حال تولید بردارهای عددی (Embedding) و ساخت پایگاه داده...")
# مدل بسیار سبک و استاندارد که بدون نیاز به تنزل وابستگی اجرا می‌شود
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(VECTOR_STORE_DIR)

print("🎉 کار تمام شد! پایگاه داده وکتوری با موفقیت ساخته و ذخیره شد.")
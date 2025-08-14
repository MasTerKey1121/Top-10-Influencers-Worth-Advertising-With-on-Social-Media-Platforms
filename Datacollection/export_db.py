import pymongo
import csv

# เชื่อมต่อกับ MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Kaggles"]
collection = db["Instagram_data"]

# ดึงข้อมูลทั้งหมดจากคอลเลกชัน
data = list(collection.find())

# เขียนข้อมูลลงในไฟล์ CSV
with open("Instagram_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()  # เขียนชื่อคอลัมน์
    writer.writerows(data)  # เขียนข้อมูล

print("Data exported successfully to 'output.csv'")
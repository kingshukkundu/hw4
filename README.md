Here’s a **README.md** file for your Flask API deployment on **Vercel**.

---

# 📌 County Data API

This is a **Flask-based API** that provides health ranking data based on **ZIP code and measure names** from an SQLite database. It is deployed using **Vercel**.

## 🚀 Features
- Accepts **POST** requests with JSON input.
- Queries health ranking data from `data.db` (SQLite).
- Returns results in **JSON format**.
- Proper **error handling** for invalid inputs.
- Supports **deployment on Vercel**.
- Returns **418 "I'm a teapot"** if `coffee=teapot` is passed. ☕🤖
s
---

## 📂 Project Structure

```
/county-data-api
│── api.py              # Flask API implementation
│── data.db             # SQLite database (Not persisted on Vercel)
│── requirements.txt    # Dependencies (Flask, gunicorn)
│── vercel.json         # Vercel configuration
│── README.md           # Documentation
```

---

## 🔧 Setup & Installation

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run the API Locally**
```bash
python api.py
```
API will be accessible at **http://127.0.0.1:5000**

---

## 🌐 API Endpoints

### **`POST /county_data`**
#### **Request**
- **Headers:**  
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "zip": "02138",
    "measure_name": "Adult obesity"
  }
  ```
  - `zip` (**required**): A 5-digit ZIP code.
  - `measure_name` (**required**): One of the following:
    - `Violent crime rate`
    - `Unemployment`
    - `Children in poverty`
    - `Diabetic screening`
    - `Mammography screening`
    - `Preventable hospital stays`
    - `Uninsured`
    - `Sexually transmitted infections`
    - `Physical inactivity`
    - `Adult obesity`
    - `Premature Death`
    - `Daily fine particulate matter`
  
#### **Response**
- **200 OK** (if results are found)
  ```json
  [
    {
      "confidence_interval_lower_bound": "0.22",
      "confidence_interval_upper_bound": "0.24",
      "county": "Middlesex County",
      "county_code": "17",
      "data_release_year": "2012",
      "denominator": "263078",
      "fipscode": "25017",
      "measure_id": "11",
      "measure_name": "Adult obesity",
      "numerator": "60771.02",
      "raw_value": "0.23",
      "state": "MA",
      "state_code": "25",
      "year_span": "2009"
    }
  ]
  ```
- **400 Bad Request** (if `zip` or `measure_name` is missing)
  ```json
  { "error": "Both 'zip' and 'measure_name' must be provided." }
  ```
- **404 Not Found** (if no matching data exists)
  ```json
  { "error": "No matching data found for that zip and measure_name." }
  ```
- **418 I'm a Teapot** (if `"coffee": "teapot"` is in request)
  ```json
  { "error": "I'm a teapot." }
  ```

---

## 🚀 Deploying to Vercel

### **1. Install Vercel CLI**
```bash
npm install -g vercel
vercel login
```

### **2. Deploy**
```bash
vercel
```
- Follow the prompts.
- Vercel will provide a public URL (e.g., `https://your-app.vercel.app`).

### **3. Test Deployed API**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"zip":"02138","measure_name":"Adult obesity"}' \
     https://your-app.vercel.app/county_data
```

---

## ⚠️ Limitations
- **SQLite database is not persistent on Vercel.**  
  - If you need persistent storage, use **PostgreSQL**, **MySQL**, or **Render.com**.
- **Vercel is stateless**, meaning that the database **resets** on each deployment.

---

## 📜 License
MIT License.

---

## 🛠 Future Improvements
- Add support for **external databases** (PostgreSQL, MySQL).
- Implement **caching** for faster queries.
- Add **API authentication** for restricted access.

---

Enjoy using the **County Data API**! 🎉🚀


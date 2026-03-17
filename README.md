# 🛒 E-Commerce Sales Analysis

A simple interactive sales dashboard built with **Streamlit** and **Plotly**.

---

## 📸 Features

- Sidebar filters — Category, Region, Order Status
- KPI cards — Total Revenue, Orders, Profit, Delivery Rate
- Charts — Revenue by Category, Order Status, Monthly Trend, Revenue by Region
- Orders data table with CSV download

---

## 🗂️ Project Structure

```
ecommerce-sales-analysis/
├── ecommerce_analysis.py   # Main app
├── sample_orders.csv       # Sample dataset (500 orders)
├── requirements.txt        # Dependencies
└── README.md
```

---

## ▶️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run ecommerce_analysis.py
```

Opens at `http://localhost:8501`

---

## 📦 Dataset

The app auto-generates 500 sample orders on startup. A `sample_orders.csv` is also included for reference.

**Columns:** `Order_ID`, `Month`, `Category`, `Region`, `Status`, `Qty`, `Price`, `Discount`, `Revenue`, `Profit`

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Plotly
- Pandas
- NumPy

---

## 👤 Author

**Hemanth** — Data Science Intern @ Sourcesys Technologies

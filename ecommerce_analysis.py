import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# ── Page config ──────────────────────────────
st.set_page_config(page_title="E-Commerce Analysis", page_icon="🛒", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #fafafa; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }
div[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #ececec;
    border-radius: 12px;
    padding: 16px 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Dataset ───────────────────────────────────
@st.cache_data
def load_data():
    random.seed(42)
    np.random.seed(42)
    cats     = ["Electronics","Clothing","Home & Kitchen","Sports","Books","Beauty","Toys"]
    regions  = ["North","South","East","West","Central"]
    statuses = ["Delivered","Returned","Cancelled","Pending"]
    months   = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    rows = []
    for i in range(500):
        cat     = random.choice(cats)
        qty     = random.randint(1, 8)
        price   = round(random.uniform(300, 20000), 2)
        disc    = random.choice([0, 0.05, 0.10, 0.15, 0.20])
        revenue = round(qty * price * (1 - disc), 2)
        rows.append({
            "Order_ID" : f"ORD{10001+i}",
            "Month"    : random.choice(months),
            "Category" : cat,
            "Region"   : random.choice(regions),
            "Status"   : random.choices(statuses, weights=[6,1,1,1])[0],
            "Qty"      : qty,
            "Price"    : price,
            "Discount" : disc,
            "Revenue"  : revenue,
            "Profit"   : round(revenue * random.uniform(0.10, 0.30), 2),
        })
    return pd.DataFrame(rows)

df = load_data()

# ── Sidebar filters ───────────────────────────
st.sidebar.markdown("## 🛒 Filters")

cats    = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
regions = st.sidebar.multiselect("Region",   sorted(df["Region"].unique()),   default=sorted(df["Region"].unique()))
status  = st.sidebar.multiselect("Status",   sorted(df["Status"].unique()),   default=sorted(df["Status"].unique()))

if not cats:    cats    = df["Category"].unique().tolist()
if not regions: regions = df["Region"].unique().tolist()
if not status:  status  = df["Status"].unique().tolist()

data = df[df["Category"].isin(cats) & df["Region"].isin(regions) & df["Status"].isin(status)]

# ── Header ────────────────────────────────────
st.markdown("## 🛒 E-Commerce Sales Analysis")
st.caption(f"Showing **{len(data)}** of **{len(df)}** orders")
st.markdown("---")

# ── KPIs ──────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue",  f"₹{data['Revenue'].sum()/1e6:.2f}M")
k2.metric("Total Orders",   f"{len(data):,}")
k3.metric("Total Profit",   f"₹{data['Profit'].sum()/1e6:.2f}M")
k4.metric("Delivery Rate",  f"{(data['Status']=='Delivered').mean()*100:.1f}%")

st.markdown("---")

# ── Charts ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    cat_rev = data.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue")
    fig = px.bar(cat_rev, x="Revenue", y="Category", orientation="h",
                 title="Revenue by Category", color_discrete_sequence=["#111"])
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                      font_family="DM Sans", margin=dict(t=40,b=10,l=0,r=0),
                      xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                      title_font_size=14)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    status_count = data["Status"].value_counts().reset_index()
    status_count.columns = ["Status", "Count"]
    fig2 = px.pie(status_count, names="Status", values="Count",
                  title="Order Status", color_discrete_sequence=["#111","#555","#888","#bbb"])
    fig2.update_layout(paper_bgcolor="white", font_family="DM Sans",
                       margin=dict(t=40,b=10,l=0,r=0), title_font_size=14)
    fig2.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly = data.groupby("Month")["Revenue"].sum().reindex(MONTH_ORDER).fillna(0).reset_index()
fig3 = px.line(monthly, x="Month", y="Revenue", title="Monthly Revenue Trend",
               markers=True, color_discrete_sequence=["#111"])
fig3.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                   font_family="DM Sans", margin=dict(t=40,b=10,l=10,r=10),
                   xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#f0f0f0"),
                   title_font_size=14)
fig3.update_traces(line_width=2.5, marker_size=6)
st.plotly_chart(fig3, use_container_width=True)

region_rev = data.groupby("Region")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
fig4 = px.bar(region_rev, x="Region", y="Revenue", title="Revenue by Region",
              color_discrete_sequence=["#333"])
fig4.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                   font_family="DM Sans", margin=dict(t=40,b=10,l=0,r=0),
                   xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#f0f0f0"),
                   title_font_size=14)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Data Table ────────────────────────────────
st.markdown("### Orders Data")
st.dataframe(data.reset_index(drop=True), use_container_width=True, height=300)

csv = data.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download CSV", csv, "orders.csv", "text/csv")

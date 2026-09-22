"""
Superstore Sales - Premium Analytics Dashboard
Run: python -m streamlit run streamlit_app.py
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# 0. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sales Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 1. GLOBAL CSS
# ============================================================
CSS = """
<style>
:root {
    --bg:           #0B0F19;
    --panel:        #111827;
    --panel-2:      #151B2B;
    --border:       #1F2937;
    --border-soft:  #1a2133;
    --primary:      #7C5CFF;
    --primary-2:    #5B7CFA;
    --text:         #F3F4F6;
    --muted:        #9CA3AF;
    --muted-2:      #6B7280;
    --green:        #22C55E;
    --red:          #EF4444;
    --orange:       #F59E0B;
    --blue:         #38BDF8;
}

html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {padding: 1.5rem 2rem 3rem 2rem; max-width: 1400px;}

/* ---------- header ---------- */
.app-header {
    display:flex; justify-content:space-between; align-items:center;
    padding: 0.5rem 0 1.25rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.app-title-wrap {display:flex; align-items:center; gap:14px;}
.app-logo {
    width:44px; height:44px; border-radius:12px;
    background: linear-gradient(135deg, #7C5CFF 0%, #5B7CFA 100%);
    display:flex; align-items:center; justify-content:center;
    font-size:16px; font-weight:700; color:#fff; letter-spacing:0.5px;
    box-shadow: 0 8px 24px rgba(124,92,255,0.35);
}
.app-title {font-size:24px; font-weight:700; letter-spacing:-0.02em; margin:0;}
.app-sub   {font-size:13px; color:var(--muted); margin:2px 0 0 0;}

/* ---------- hero card ---------- */
.hero-card {
    position: relative !important;
    background: linear-gradient(135deg, #4C1D95 0%, #5B21B6 45%, #3B1D8F 100%) !important;
    border-radius: 20px !important;
    padding: 34px !important;
    min-height: 180px !important;
    overflow: hidden !important;
    border: 1px solid rgba(124,92,255,0.35) !important;
    box-shadow: 0 20px 40px rgba(76,29,149,0.35) !important;
    margin-bottom: 18px !important;
    text-align: center !important;
}
.hero-card::after {
    content: '' !important;
    position: absolute !important;
    right: -60px !important;
    bottom: -80px !important;
    width: 320px !important;
    height: 220px !important;
    background: radial-gradient(closest-side, rgba(255,255,255,0.18), transparent 70%) !important;
    border-radius: 50% !important;
    pointer-events: none !important;
}
.hero-label {
    font-size: 14px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.78) !important;
    margin: 0 0 12px 0 !important;
    position: relative !important;
    z-index: 2 !important;
}
.hero-value {
    font-size: 64px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.025em !important;
    margin: 0 !important;
    line-height: 1.02 !important;
    position: relative !important;
    z-index: 2 !important;
}
.hero-delta {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 8px !important;
    margin-top: 14px !important;
    font-size: 14px !important;
    color: #ffffff !important;
    position: relative !important;
    z-index: 2 !important;
}
.hero-pill {
    background: rgba(34,197,94,0.18) !important;
    color: #4ADE80 !important;
    padding: 4px 10px !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
}
.hero-pill-neg {
    background: rgba(239,68,68,0.18) !important;
    color: #FCA5A5 !important;
    padding: 4px 10px !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
}

/* ---------- metric cards ---------- */
.metric-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 20px;
    height: 100%;
    transition: transform 0.15s, box-shadow 0.2s, border-color 0.2s;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.35);
}

/* Card color variants — card color follows card identity */
.metric-card.purple {
    background: linear-gradient(135deg, #7C5CFF 0%, #5B21B6 100%);
    border: 1px solid rgba(124,92,255,0.55);
    box-shadow: 0 12px 28px rgba(124,92,255,0.28);
}
.metric-card.green {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    border: 1px solid rgba(16,185,129,0.55);
    box-shadow: 0 12px 28px rgba(16,185,129,0.28);
}
.metric-card.blue {
    background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);
    border: 1px solid rgba(56,189,248,0.55);
    box-shadow: 0 12px 28px rgba(56,189,248,0.28);
}
.metric-card.pink {
    background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
    border: 1px solid rgba(236,72,153,0.55);
    box-shadow: 0 12px 28px rgba(236,72,153,0.28);
}
.metric-card.orange {
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    border: 1px solid rgba(245,158,11,0.55);
    box-shadow: 0 12px 28px rgba(245,158,11,0.28);
}
.metric-card.indigo {
    background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);
    border: 1px solid rgba(99,102,241,0.55);
    box-shadow: 0 12px 28px rgba(99,102,241,0.28);
}

/* On colored cards — force white text */
.metric-card .metric-label { color: rgba(255,255,255,0.88) !important; }
.metric-card .metric-value { color: #ffffff !important; }
.metric-card .metric-delta { color: rgba(255,255,255,0.95) !important; }
.metric-card .metric-delta.delta-pos,
.metric-card .metric-delta.delta-neg,
.metric-card .metric-delta.delta-flat {
    color: rgba(255,255,255,0.95) !important;
}

/* Icon chip on colored cards: frosted white */
.metric-card .metric-icon {
    background: rgba(255,255,255,0.20) !important;
    color: #ffffff !important;
}

/* Fallback icon colors */
.metric-icon {
    width:38px; height:38px; border-radius:10px;
    display:inline-flex; align-items:center; justify-content:center;
    font-size:13px; font-weight:700; margin-bottom:12px;
    letter-spacing:0.5px;
}
.icon-purple {background: rgba(124,92,255,0.15); color:#A78BFA;}
.icon-green  {background: rgba(34,197,94,0.15);  color:#4ADE80;}
.icon-blue   {background: rgba(56,189,248,0.15); color:#38BDF8;}
.icon-orange {background: rgba(245,158,11,0.15); color:#FBBF24;}
.icon-pink   {background: rgba(236,72,153,0.15); color:#F472B6;}

.metric-label {font-size:12px; letter-spacing:0.08em; text-transform:uppercase;
               color:var(--muted); margin:0;}
.metric-value {font-size:26px; font-weight:700; color:var(--text);
               margin:6px 0 4px 0; letter-spacing:-0.01em;}
.metric-delta {font-size:13px; font-weight:600;}
.delta-pos {color: var(--green);}
.delta-neg {color: var(--red);}
.delta-flat{color: var(--muted);}

.section-card {
    background: var(--panel-2);
    border: 1px solid var(--border-soft);
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
}
.section-title {font-size:16px; font-weight:700; margin:0 0 4px 0;}
.section-sub   {font-size:13px; color:var(--muted); margin:0 0 14px 0;}

.insight-card {
    background: linear-gradient(135deg, #1F1436 0%, #221845 100%);
    border: 1px solid rgba(124,92,255,0.35);
    border-radius: 16px;
    padding: 18px 20px;
}
.insight-title {font-size:13px; text-transform:uppercase; letter-spacing:0.1em;
                color:#A78BFA; margin:0 0 8px 0;}
.insight-body  {font-size:15px; color:var(--text); margin:0; line-height:1.5;}

.ranking-row {
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 0; border-bottom: 1px solid var(--border-soft);
}
.ranking-row:last-child {border-bottom:none;}
.rank-badge {
    width:32px; height:32px; border-radius:9px;
    background: rgba(124,92,255,0.15); color:#A78BFA;
    font-weight:700; display:flex; align-items:center; justify-content:center;
    margin-right:14px; font-size:13px;
}
.rank-name {font-size:14px; font-weight:600; margin:0;}
.rank-sub  {font-size:12px; color:var(--muted); margin:2px 0 0 0;}
.rank-value{font-size:15px; font-weight:700; color:#A78BFA;}

.js-plotly-plot .plotly .modebar {display:none !important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# 2. DATA LOADING
# ============================================================
@st.cache_data(show_spinner=False)
def load_data():
    needed = ["orders", "customers", "rfm", "subcategory", "monthly"]

    df = pd.read_excel("Superstore Sales Dataset.xlsx", sheet_name="Data")
    df.columns = (df.columns.str.strip()
                    .str.replace(" & ", "_and_", regex=False)
                    .str.replace(" ", "_", regex=False))
    df = df.rename(columns={"Sub-Category": "Sub_Category"})

    if all(os.path.exists(f"outputs/{n}.csv") for n in needed):
        orders = pd.read_csv("outputs/orders.csv", parse_dates=["Order_Date"])
        cust   = pd.read_csv("outputs/customers.csv", parse_dates=["first_order", "last_order"])
        rfm    = pd.read_csv("outputs/rfm.csv")
        subcat = pd.read_csv("outputs/subcategory.csv")
        monthly= pd.read_csv("outputs/monthly.csv")
        return df, orders, cust, rfm, subcat, monthly

    orders = (df.groupby(["Order_ID", "Order_Date", "Customer_ID",
                          "Segment", "Region", "Ship_Mode"])
                .agg(order_revenue=("Sales", "sum"))
                .reset_index())

    cust = (orders.groupby("Customer_ID")
                  .agg(first_order=("Order_Date","min"),
                       last_order=("Order_Date","max"),
                       total_orders=("Order_ID","nunique"),
                       total_revenue=("order_revenue","sum"),
                       avg_order_value=("order_revenue","mean"))
                  .reset_index())
    cust = cust.merge(df[["Customer_ID","Customer_Name","Segment","Region"]]
                      .drop_duplicates("Customer_ID"),
                      on="Customer_ID", how="left")
    cust["recency_days"] = (orders["Order_Date"].max() - cust["last_order"]).dt.days

    rfm = cust[["Customer_ID","Customer_Name","Segment","Region",
                "recency_days","total_orders","total_revenue"]].copy()
    rfm["R_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5,4,3,2,1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["total_orders"].rank(method="first"), 5,
                             labels=[1,2,3,4,5]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["total_revenue"].rank(method="first"), 5,
                             labels=[1,2,3,4,5]).astype(int)

    def seg(row):
        r,f,m = row["R_score"], row["F_score"], row["M_score"]
        if r>=4 and f>=4 and m>=4: return "Champions"
        if r>=3 and f>=3 and m>=3: return "Loyal"
        if r>=4 and f<=2:          return "New / Promising"
        if r<=2 and f>=4 and m>=4: return "At-Risk High Value"
        if r<=2 and f>=3:          return "At-Risk"
        if r<=2 and f<=2:          return "Lost / Hibernating"
        return "Needs Attention"
    rfm["RFM_Segment"] = rfm.apply(seg, axis=1)

    subcat = (df.groupby(["Category","Sub_Category"])
                .agg(revenue=("Sales","sum"),
                     line_items=("Row_ID","count"),
                     orders=("Order_ID","nunique"))
                .reset_index())

    df["Year"]  = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    monthly = (df.groupby(["Year","Month"])
                 .agg(revenue=("Sales","sum"),
                      orders=("Order_ID","nunique"))
                 .reset_index())

    os.makedirs("outputs", exist_ok=True)
    orders.to_csv("outputs/orders.csv", index=False)
    cust.to_csv("outputs/customers.csv", index=False)
    rfm.to_csv("outputs/rfm.csv", index=False)
    subcat.to_csv("outputs/subcategory.csv", index=False)
    monthly.to_csv("outputs/monthly.csv", index=False)

    return df, orders, cust, rfm, subcat, monthly


df, orders, cust, rfm, subcat, monthly = load_data()

# ============================================================
# 3. HELPERS
# ============================================================
def fmt_money(v):
    v = float(v)
    if abs(v) >= 1e9: return f"${v/1e9:,.2f}B"
    if abs(v) >= 1e6: return f"${v/1e6:,.2f}M"
    if abs(v) >= 1e3: return f"${v/1e3:,.1f}K"
    return f"${v:,.0f}"

def fmt_int(v):
    return f"{int(v):,}"

def pct_change(curr, prev):
    if prev == 0 or pd.isna(prev): return None
    return (curr - prev) / prev * 100

def metric_card(icon_text, icon_class, label, value, delta=None, sub=None, variant=""):
    delta_html = ""
    if delta is not None:
        cls = "delta-pos" if delta >= 0 else "delta-neg"
        symbol = "+" if delta >= 0 else "-"
        delta_html = f'<div class="metric-delta {cls}">{symbol}{abs(delta):.1f}%</div>'
    elif sub:
        delta_html = f'<div class="metric-delta delta-flat">{sub}</div>'
    return f"""
    <div class="metric-card {variant}">
        <div class="metric-icon {icon_class}">{icon_text}</div>
        <p class="metric-label">{label}</p>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def section(title, sub=""):
    sub_html = f'<p class="section-sub">{sub}</p>' if sub else ""
    st.markdown(f'<div class="section-card"><p class="section-title">{title}</p>{sub_html}',
                unsafe_allow_html=True)

def end_section():
    st.markdown("</div>", unsafe_allow_html=True)

def insight_card(title, body):
    return f"""
    <div class="insight-card" style="margin-bottom:14px;">
      <p class="insight-title">{title}</p>
      <p class="insight-body">{body}</p>
    </div>
    """

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E5E7EB", family="Inter"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor="#1F2937", zerolinecolor="#1F2937"),
    yaxis=dict(gridcolor="#1F2937", zerolinecolor="#1F2937"),
)

# ============================================================
# 4. HEADER + FILTERS
# ============================================================
st.markdown('<div class="app-header">'
            '<div class="app-title-wrap">'
            '<div class="app-logo">SA</div>'
            '<div><p class="app-title">Sales Analytics</p>'
            '<p class="app-sub">Superstore - 2015 to 2018</p></div></div>'
            '</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns([1,1,1,2])

with f1:
    seg_opts = ["All"] + sorted(orders["Segment"].dropna().unique().tolist())
    seg_sel = st.selectbox("Segment", seg_opts)

with f2:
    reg_opts = ["All"] + sorted(orders["Region"].dropna().unique().tolist())
    reg_sel = st.selectbox("Region", reg_opts)

with f3:
    ship_opts = ["All"] + sorted(orders["Ship_Mode"].dropna().unique().tolist())
    ship_sel = st.selectbox("Ship Mode", ship_opts)

with f4:
    dmin = orders["Order_Date"].min().date()
    dmax = orders["Order_Date"].max().date()
    date_range = st.date_input("Date range", (dmin, dmax), min_value=dmin, max_value=dmax)

filt = orders.copy()
if seg_sel != "All":  filt = filt[filt["Segment"] == seg_sel]
if reg_sel != "All":  filt = filt[filt["Region"] == reg_sel]
if ship_sel != "All": filt = filt[filt["Ship_Mode"] == ship_sel]
if isinstance(date_range, tuple) and len(date_range) == 2:
    lo, hi = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filt = filt[(filt["Order_Date"] >= lo) & (filt["Order_Date"] <= hi)]

if filt.empty:
    st.warning("No data for the selected filters.")
    st.stop()

filt_df = df.copy()
if seg_sel != "All":  filt_df = filt_df[filt_df["Segment"] == seg_sel]
if reg_sel != "All":  filt_df = filt_df[filt_df["Region"] == reg_sel]
if ship_sel != "All": filt_df = filt_df[filt_df["Ship_Mode"] == ship_sel]
if isinstance(date_range, tuple) and len(date_range) == 2:
    lo, hi = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filt_df = filt_df[(filt_df["Order_Date"] >= lo) & (filt_df["Order_Date"] <= hi)]

# ============================================================
# 5. KPI COMPUTATION
# ============================================================
total_revenue = filt["order_revenue"].sum()
total_orders  = filt["Order_ID"].nunique()
total_cust    = filt["Customer_ID"].nunique()
aov           = filt["order_revenue"].mean()

lo = filt["Order_Date"].min()
hi = filt["Order_Date"].max()
window = (hi - lo).days or 1
prev_lo = lo - pd.Timedelta(days=window)
prev = orders[(orders["Order_Date"] >= prev_lo) & (orders["Order_Date"] < lo)]
rev_delta = pct_change(total_revenue, prev["order_revenue"].sum())
ord_delta = pct_change(total_orders,  prev["Order_ID"].nunique())
aov_delta = pct_change(aov,           prev["order_revenue"].mean())
cust_delta= pct_change(total_cust,    prev["Customer_ID"].nunique())

cust_filt = (filt.groupby("Customer_ID")["Order_ID"].nunique())
repeat_rate = (cust_filt > 1).mean() * 100

sub_by_cat = filt_df.groupby("Category")["Sales"].sum()
top_cat = sub_by_cat.idxmax()
top_cat_share = sub_by_cat.max() / sub_by_cat.sum() * 100

reg_by = filt.groupby("Region")["order_revenue"].sum()
top_region = reg_by.idxmax()
top_region_share = reg_by.max() / reg_by.sum() * 100

# ============================================================
# 6. HERO + KPI GRID
# ============================================================
delta_html = ""
if rev_delta is not None:
    cls = "hero-pill" if rev_delta >= 0 else "hero-pill-neg"
    sign = "+" if rev_delta >= 0 else "-"
    delta_html = f'<span class="{cls}">{sign}{abs(rev_delta):.1f}%</span> vs previous period'

st.markdown(f"""
<div class="hero-card">
    <p class="hero-label">Total Revenue</p>
    <p class="hero-value">{fmt_money(total_revenue)}</p>
    <div class="hero-delta">{delta_html}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

with c1: st.markdown(metric_card("ORD","icon-purple","Total Orders",
                                 fmt_int(total_orders), ord_delta,
                                 variant="purple"), unsafe_allow_html=True)
with c2: st.markdown(metric_card("CUS","icon-green","Unique Customers",
                                 fmt_int(total_cust), cust_delta,
                                 variant="green"), unsafe_allow_html=True)
with c3: st.markdown(metric_card("AOV","icon-blue","Avg Order Value",
                                 fmt_money(aov), aov_delta,
                                 variant="blue"), unsafe_allow_html=True)
with c4: st.markdown(metric_card("RPT","icon-pink","Repeat Rate",
                                 f"{repeat_rate:.1f}%",
                                 sub="share of customers with 2+ orders",
                                 variant="pink"), unsafe_allow_html=True)
with c5: st.markdown(metric_card("CAT","icon-orange","Top Category",
                                 top_cat,
                                 sub=f"{top_cat_share:.1f}% of revenue",
                                 variant="orange"), unsafe_allow_html=True)
with c6: st.markdown(metric_card("REG","icon-purple","Top Region",
                                 top_region,
                                 sub=f"{top_region_share:.1f}% of revenue",
                                 variant="indigo"), unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ============================================================
# 7. TRENDS
# ============================================================
section("Revenue Trend", "Monthly revenue across the selected filters")

trend = (filt.assign(Month=filt["Order_Date"].dt.to_period("M").dt.to_timestamp())
             .groupby("Month")
             .agg(revenue=("order_revenue","sum"),
                  orders=("Order_ID","nunique"))
             .reset_index())

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=trend["Month"], y=trend["revenue"],
    mode="lines", fill="tozeroy",
    line=dict(color="#7C5CFF", width=3),
    fillcolor="rgba(124,92,255,0.15)",
    hovertemplate="%{x|%b %Y}<br>Revenue: $%{y:,.0f}<extra></extra>",
))
fig.update_layout(**PLOT_LAYOUT, height=320)
st.plotly_chart(fig, use_container_width=True)
end_section()

# ============================================================
# 8. CATEGORY / SUBCATEGORY
# ============================================================
cA, cB = st.columns([1.4, 1])

with cA:
    section("Sub-Category Revenue", "Top 10 by revenue")
    sub_rev = (filt_df.groupby("Sub_Category")["Sales"]
                      .sum().sort_values(ascending=False).head(10).reset_index())
    fig2 = px.bar(sub_rev, x="Sales", y="Sub_Category",
                  orientation="h", color_discrete_sequence=["#7C5CFF"])
    fig2.update_layout(**PLOT_LAYOUT, height=340,
                       xaxis_title="", yaxis_title="")
    fig2.update_yaxes(autorange="reversed")
    st.plotly_chart(fig2, use_container_width=True)
    end_section()

with cB:
    section("Top Products", "Ranked by revenue")
    top_prod = (filt_df.groupby("Product_Name")
                       .agg(revenue=("Sales","sum"),
                            orders=("Order_ID","nunique"))
                       .sort_values("revenue", ascending=False)
                       .head(5).reset_index())
    rows = ""
    for i, r in top_prod.iterrows():
        rows += f"""
        <div class="ranking-row">
          <div style="display:flex; align-items:center;">
            <div class="rank-badge">{i+1:02d}</div>
            <div>
              <p class="rank-name">{r['Product_Name'][:42]}</p>
              <p class="rank-sub">{int(r['orders'])} orders</p>
            </div>
          </div>
          <div class="rank-value">{fmt_money(r['revenue'])}</div>
        </div>"""
    st.markdown(rows, unsafe_allow_html=True)
    end_section()

# ============================================================
# 9. GEOGRAPHY
# ============================================================
section("Regional Performance", "Revenue by region")
reg_df = (filt.groupby("Region")
              .agg(revenue=("order_revenue","sum"),
                   orders=("Order_ID","nunique"))
              .reset_index()
              .sort_values("revenue", ascending=False))
fig3 = px.bar(reg_df, x="Region", y="revenue",
              color="Region",
              color_discrete_sequence=["#7C5CFF","#5B7CFA","#38BDF8","#A78BFA"])
fig3.update_layout(**PLOT_LAYOUT, height=300, showlegend=False,
                   xaxis_title="", yaxis_title="")
st.plotly_chart(fig3, use_container_width=True)
end_section()

# ============================================================
# 10. RETENTION / RFM
# ============================================================
section("Retention - RFM Segments",
        "Customer segmentation based on recency, frequency and monetary value")
rfm_summary = (rfm.groupby("RFM_Segment")
                  .agg(customers=("Customer_ID","count"),
                       revenue=("total_revenue","sum"))
                  .reset_index()
                  .sort_values("revenue", ascending=False))

fig4 = px.bar(rfm_summary, x="RFM_Segment", y="revenue",
              color="RFM_Segment",
              color_discrete_sequence=px.colors.sequential.Purples_r)
fig4.update_layout(**PLOT_LAYOUT, height=340, showlegend=False,
                   xaxis_title="", yaxis_title="Revenue")
st.plotly_chart(fig4, use_container_width=True)

top_seg = rfm_summary.iloc[0]
st.markdown(f"""
<div class="insight-card">
  <p class="insight-title">Key Insight</p>
  <p class="insight-body"><b>{top_seg['RFM_Segment']}</b> is the highest-revenue segment,
  contributing <b>{fmt_money(top_seg['revenue'])}</b> from
  <b>{int(top_seg['customers'])}</b> customers.
  Prioritize retention here before scaling acquisition.</p>
</div>
""", unsafe_allow_html=True)
end_section()

# ============================================================
# 10b. INSIGHTS
# ============================================================
section("Insights", "Auto-generated from the current filters")

ins_cat = filt_df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
top_cat_name = ins_cat.index[0]
top_cat_pct  = ins_cat.iloc[0] / ins_cat.sum() * 100

ins_sub = filt_df.groupby("Sub_Category")["Sales"].sum().sort_values(ascending=False)
top_sub_name = ins_sub.index[0]
top_sub_pct  = ins_sub.iloc[0] / ins_sub.sum() * 100

ins_month = (filt.assign(Month=filt["Order_Date"].dt.month)
                 .groupby("Month")["order_revenue"].sum())
peak_month_num = int(ins_month.idxmax())
peak_month_pct = ins_month.max() / ins_month.sum() * 100
month_names = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]
peak_month_name = month_names[peak_month_num - 1]

champ_loyal = rfm[rfm["RFM_Segment"].isin(["Champions","Loyal"])]
champ_loyal_cust_pct = len(champ_loyal) / len(rfm) * 100
champ_loyal_rev_pct  = champ_loyal["total_revenue"].sum() / rfm["total_revenue"].sum() * 100

atrisk_hv = rfm[rfm["RFM_Segment"] == "At-Risk High Value"]
atrisk_hv_cust = len(atrisk_hv)
atrisk_hv_rev_pct = atrisk_hv["total_revenue"].sum() / rfm["total_revenue"].sum() * 100

insight_a = insight_card(
    "Revenue Concentration",
    f"<b>{top_cat_name}</b> drives <b>{top_cat_pct:.1f}%</b> of revenue, "
    f"led by <b>{top_sub_name}</b> at <b>{top_sub_pct:.1f}%</b>. "
    f"Protect these categories before expanding elsewhere."
)

insight_b = insight_card(
    "Seasonality",
    f"<b>{peak_month_name}</b> is the strongest month, contributing "
    f"<b>{peak_month_pct:.1f}%</b> of annual revenue. "
    f"Concentrate campaigns in Q4 to match demand peaks."
)

insight_c = insight_card(
    "Loyalty Asset",
    f"<b>Champions + Loyal</b> represent <b>{champ_loyal_cust_pct:.1f}%</b> of customers "
    f"but <b>{champ_loyal_rev_pct:.1f}%</b> of revenue. "
    f"This tier is the highest-leverage retention target."
)

insight_d = insight_card(
    "Priority Win-Back",
    f"<b>At-Risk High Value</b> customers number only <b>{atrisk_hv_cust}</b> "
    f"but hold <b>{atrisk_hv_rev_pct:.1f}%</b> of revenue. "
    f"Personalized outreach here has the highest return."
)

insight_e = insight_card(
    "Retention Baseline",
    f"Repeat rate is <b>{repeat_rate:.1f}%</b>. Acquisition is not the bottleneck - "
    f"the priority is increasing order frequency and reactivating stale buyers."
)

ic1, ic2 = st.columns(2)
with ic1:
    st.markdown(insight_a, unsafe_allow_html=True)
    st.markdown(insight_c, unsafe_allow_html=True)
    st.markdown(insight_e, unsafe_allow_html=True)
with ic2:
    st.markdown(insight_b, unsafe_allow_html=True)
   
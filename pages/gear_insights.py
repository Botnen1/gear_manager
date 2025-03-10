import streamlit as st
from utils.db_utils import get_session
from utils.db_setup import Gear
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.title("📊 Gear Inventory Insights")

    session = get_session()
    gear_items = session.query(Gear).all()

    if not gear_items:
        st.info("No gear available to analyze.")
        return

    # Create DataFrame from gear items
    df = pd.DataFrame([{
        "name": gear.name,
        "category": gear.category,
        "weight_grams": gear.weight_grams,
        "status": gear.status,
        "notes": gear.notes,
        "link": gear.link
    } for gear in gear_items])

    # Quick stats
    st.subheader("🔖 Quick Stats")
    total_items = len(df)
    total_weight = df["weight_grams"].sum()
    avg_weight = df["weight_grams"].mean()
    heaviest = df.loc[df["weight_grams"].idxmax()]
    lightest = df.loc[df["weight_grams"].idxmin()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gear Items", total_items)
    col2.metric("Total Weight", f"{total_weight:.2f} g")
    col3.metric("Average Weight", f"{avg_weight:.2f} g")

    st.markdown("---")

    col4, col5 = st.columns(2)
    col4.metric("Heaviest Item", f"{heaviest['name']} ({heaviest['weight_grams']} g)")
    col5.metric("Lightest Item", f"{lightest['name']} ({lightest['weight_grams']} g)")

    # Gear by Category
    st.subheader("📁 Gear Breakdown by Category")
    category_counts = df["category"].value_counts()
    if not category_counts.empty:
        fig, ax = plt.subplots()
        category_counts.plot.pie(autopct='%1.1f%%', ax=ax)
        plt.ylabel('')
        st.pyplot(fig)
    else:
        st.warning("No category data available.")

    # Weight distribution
    st.subheader("⚖️ Gear Weight Distribution")
    weight_per_category = df.groupby("category")["weight_grams"].sum()
    if not weight_per_category.empty:
        fig2, ax2 = plt.subplots()
        weight_per_category.plot.bar(ax=ax2)
        plt.xticks(rotation=45)
        plt.ylabel('Total Weight (grams)')
        st.pyplot(fig2)
    else:
        st.warning("No weight data available.")

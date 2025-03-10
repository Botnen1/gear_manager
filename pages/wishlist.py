import streamlit as st
from utils.db_utils import get_session
from utils.db_setup import Gear, Wishlist  # ✅ Fix: Import Gear

def app():
    st.title("🎁 Gear Wishlist Tracker")
    session = get_session()

    # Function to add an item to wishlist (without affecting inventory)
    def add_wishlist_item(name, category, target_price, link):
        session = get_session()

        # Check if gear already exists
        existing_gear = session.query(Gear).filter(Gear.name == name.strip()).first()

        if not existing_gear:
            # If not in Gear table, create it (but NOT as "owned")
            new_gear = Gear(
                name=name.strip(),
                category=category,
                status="wishlist",  # Wishlist items are not owned
                link=link.strip() if link else ""
            )
            session.add(new_gear)
            session.commit()
            gear_id = new_gear.id
        else:
            gear_id = existing_gear.id

        # Check if item is already in wishlist
        existing_wishlist = session.query(Wishlist).filter(Wishlist.gear_id == gear_id).first()
        if existing_wishlist:
            st.warning(f"'{name}' is already in the wishlist!")
            return

        # Add item to Wishlist
        wishlist_item = Wishlist(
            gear_id=gear_id,
            target_price=target_price
        )
        session.add(wishlist_item)
        session.commit()

    # Add Wishlist Form
    with st.expander("➕ Add Item to Wishlist"):
        with st.form("wishlist_form", clear_on_submit=True):
            name = st.text_input("Gear Name")
            category = st.selectbox("Category", ["Camp", "Cooking", "Clothing", "Shoes", "Gear", "Electronics", "Fishing", "Firepouch", "Misc"])
            target_price = st.number_input("Target Price ($)", min_value=0.0, step=1.0)
            link = st.text_input("Product Link (optional)")

            submitted = st.form_submit_button("Add to Wishlist")
            if submitted:
                if name.strip():
                    add_wishlist_item(name, category, target_price, link)
                    st.success(f"✅ '{name.strip()}' added to wishlist!")
                    st.rerun()
                else:
                    st.error("Please enter a gear name.")

    # Display Wishlist Items
    st.subheader("🔖 Current Wishlist Items:")
    wishlist_items = session.query(Wishlist).all()

    if wishlist_items:
        for item in wishlist_items:
            gear = session.query(Gear).filter(Gear.id == item.gear_id).first()

            if gear:
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"""
                    **{gear.name}** ({gear.category})  
                    - **Target Price:** ${item.target_price:.2f}  
                    - **Link:** [Open Link]({gear.link if gear.link else '#'})  
                    """)
                with col2:
                    if st.button("🗑️", key=f"delete_wishlist_{item.id}"):
                        session.delete(item)
                        session.commit()
                        st.warning(f"Deleted '{gear.name}' from wishlist!")
                        st.rerun()
                st.markdown("---")
    else:
        st.info("Wishlist is currently empty.")

import streamlit as st
from utils.db_utils import get_session
from utils.db_setup import Gear
import os

IMAGE_DIR = "gear_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def save_image(image, gear_name):
    image_path = os.path.join(IMAGE_DIR, f"{gear_name}.png")
    with open(image_path, "wb") as f:
        f.write(image.getbuffer())
    return image_path

def app():
    st.title("📦 Gear Inventory Tracker")
    session = get_session()

    # Function to add gear (only to inventory)
    def add_gear(name, category, weight, notes, link, image):
        image_path = save_image(image, name) if image else None
        gear_item = Gear(
            name=name.strip(),
            category=category,
            weight_grams=weight,
            status="owned",  # Ensuring only owned gear is here
            notes=notes.strip(),
            link=link.strip(),
            image_path=image_path
        )
        session.add(gear_item)
        session.commit()

    # Add new gear form
    with st.expander("➕ Add New Gear"):
        with st.form("new_gear_form", clear_on_submit=True):
            name = st.text_input("Gear Name")
            category = st.selectbox("Category", ["Camp", "Cooking", "Clothing", "Shoes", "Gear", "Electronics", "Fishing", "Firepouch", "Accessories", "Documents", "Misc"])
            weight = st.number_input("Weight (grams)", min_value=0.0, step=1.0)
            notes = st.text_area("Notes (optional)")
            link = st.text_input("Link (optional)")
            image = st.file_uploader("Upload Gear Image (optional)", type=["png", "jpg", "jpeg"])

            submitted = st.form_submit_button("Add Gear")
            if submitted:
                if name.strip():
                    existing = session.query(Gear).filter(Gear.name == name.strip()).first()
                    if existing:
                        st.error("Gear already exists.")
                    else:
                        add_gear(name, category, weight, notes, link, image)
                        st.success(f"✅ '{name.strip()}' added successfully!")
                        st.rerun()
                else:
                    st.error("Enter gear name.")

    # Display Gear Items with Edit & Delete Options
    st.subheader("🗃️ Current Inventory")
    gear_items = session.query(Gear).all()

    if gear_items:
        cols = st.columns(3)  # Adjust number for grid layout

        for idx, gear in enumerate(gear_items):
            col = cols[idx % 3]  # Place items in a flexible grid layout
            with col:
                with st.container(border=True):  # ✅ Removed fixed height to prevent scrolling
                    # ✅ Set fixed max width for images but allow auto-height
                    if gear.image_path and os.path.exists(gear.image_path):
                        st.image(gear.image_path, use_container_width=False, width=150)

                    st.markdown(f"### {gear.name}")
                    st.caption(f"{gear.category}")
                    st.markdown(f"- **Weight:** {gear.weight_grams} grams")
                    st.markdown(f"- **Status:** {gear.status}")
                    st.markdown(f"- **[Link]({gear.link})**")
                    st.markdown(f"- **Notes:** {gear.notes if gear.notes else '_No notes_'}")

                    # Edit button
                    if st.button(f"✏️ Edit", key=f"edit_{gear.id}"):
                        st.session_state['edit_item_id'] = gear.id

                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{gear.id}"):
                        session.delete(gear)
                        session.commit()
                        st.success(f"Deleted '{gear.name}'!")
                        st.rerun()

                    # Editing form (if user clicked edit)
                    if st.session_state.get('edit_item_id') == gear.id:
                        with st.form(f"edit_form_{gear.id}"):
                            new_category = st.selectbox("Category", 
                                ["Camp", "Cooking", "Clothing", "Shoes", "Gear", "Electronics", "Fishing", "Firepouch", "Accessories", "Documents", "Misc"],
                                index=["Camp", "Cooking", "Clothing", "Shoes", "Gear", "Electronics", "Fishing", "Firepouch", "Accessories", "Documents", "Misc"].index(gear.category)
                            )
                            new_weight = st.number_input("Weight (grams)", value=gear.weight_grams)
                            new_status = st.selectbox("Status", ["owned", "wishlist", "ordered"], index=["owned", "wishlist", "ordered"].index(gear.status))
                            new_notes = st.text_area("Notes", value=gear.notes if gear.notes else "")
                            new_link = st.text_input("Link", value=gear.link if gear.link else "")

                            # Image Upload (show existing image if available)
                            st.markdown("### Update Image")
                            if gear.image_path and os.path.exists(gear.image_path):
                                st.image(gear.image_path, caption="Current Image", width=100)  # ✅ Smaller image preview
                            new_image = st.file_uploader("Upload New Image (optional)", type=["png", "jpg", "jpeg"])

                            # Save Changes Button
                            if st.form_submit_button("Save Changes"):
                                gear.category = new_category
                                gear.weight_grams = new_weight
                                gear.status = new_status
                                gear.notes = new_notes.strip()
                                gear.link = new_link.strip()

                                # Update Image if a new one is uploaded
                                if new_image:
                                    image_path = save_image(new_image, gear.name)  # Save and update image
                                    gear.image_path = image_path

                                session.commit()
                                st.success(f"✅ '{gear.name}' updated successfully!")
                                del st.session_state['edit_item_id']
                                st.rerun()
    else:
        st.info("Your inventory is empty.")

import sqlite3

conn = sqlite3.connect('data/gear.db')
cursor = conn.cursor()

# Manually add the new column
cursor.execute("ALTER TABLE gear ADD COLUMN image_path TEXT;")

conn.commit()
conn.close()

print("✅ Column 'image_path' added successfully!")

import sqlite3

def create_tables():

    conn = sqlite3.connect('properties.db')

    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS properties_raw
                    (id INTEGER PRIMARY KEY, title TEXT, location TEXT, price TEXT, property_type TEXT, bedrooms TEXT, bathrooms TEXT, area TEXT, link TEXT)''')
    conn.commit()

    c.execute('''CREATE TABLE IF NOT EXISTS properties_cleaned
                    (id INTEGER PRIMARY KEY, title TEXT, location TEXT, price REAL, property_type TEXT, bedrooms INTEGER, bathrooms INTEGER, area REAL, link TEXT)''')
    conn.commit()

    return True


create_tables()

def insert_raw_data(data_df):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()

    for index, row in data_df.iterrows():
        c.execute('''INSERT INTO properties_raw (title, location, price, property_type, bedrooms, bathrooms, area, link) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (row['title'], row['location'], row['price'], row['property_type'], row['bedrooms'], row['bathrooms'], row['area'], row.get('link', None)))
    
    conn.commit()
    return True

def insert_cleaned_data(data_df):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()

    for index, row in data_df.iterrows():
        c.execute('''INSERT INTO properties_cleaned (title, location, price, property_type, bedrooms, bathrooms, area, link) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (row['title'], row['location'], row['price'], row['property_type'], row['bedrooms'], row['bathrooms'], row['area'], row.get('link', None)))
    
    conn.commit()
    return True




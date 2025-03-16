import sqlite3
import os

def view_database_contents():
    # Connect to the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # View Categories
        print("\n=== Categories ===")
        cursor.execute('SELECT name, slug, description FROM resources_category')
        categories = cursor.fetchall()
        for cat in categories:
            print(f"Name: {cat[0]}")
            print(f"Slug: {cat[1]}")
            print(f"Description: {cat[2]}")
            print("-" * 50)
        
        # View Resources
        print("\n=== Resources ===")
        cursor.execute('''
            SELECT title, resource_type, url, description 
            FROM resources_resource 
            LIMIT 5
        ''')
        resources = cursor.fetchall()
        for res in resources:
            print(f"Title: {res[0]}")
            print(f"Type: {res[1]}")
            print(f"URL: {res[2]}")
            print(f"Description: {res[3][:100]}...")  # Show first 100 chars of description
            print("-" * 50)
        
        # Count resources by type
        print("\n=== Resource Counts by Type ===")
        cursor.execute('''
            SELECT resource_type, COUNT(*) 
            FROM resources_resource 
            GROUP BY resource_type
        ''')
        counts = cursor.fetchall()
        for count in counts:
            print(f"{count[0]}: {count[1]} resources")
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    view_database_contents() 
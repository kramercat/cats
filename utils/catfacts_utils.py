import sqlite3
import requests
import time

# Step 1: Set up the database connection and cursor
conn = sqlite3.connect("data/cat_facts.db")
cursor = conn.cursor()

# Step 2: Create the table if not already created
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS cat_facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT NOT NULL,
        length INTEGER NOT NULL
    )
"""
)


# Function to fetch and insert cat facts from a specific page
def fetch_and_insert_facts(page):
    # Fetch the data from the API
    url = f"https://catfact.ninja/facts?page={page}"
    response = requests.get(url, headers={"accept": "application/json"})

    if response.status_code == 200:
        data = response.json()

        # Insert each fact into the database
        for fact_item in data["data"]:
            fact = fact_item["fact"]
            length = fact_item["length"]
            cursor.execute(
                """
                INSERT INTO cat_facts (fact, length)
                VALUES (?, ?)
            """,
                (fact, length),
            )

        # Commit the changes after each page
        conn.commit()

        # Return the next page and total number of pages
        next_page = data.get("next_page_url")
        total_pages = data.get("last_page", 1)
        return next_page, total_pages

    else:
        print(f"Error fetching page {page}: {response.status_code}")
        return None, None


# Step 3: Paginate through all the pages
def paginate_facts():
    page = 1
    while True:
        print(f"Fetching page {page}...")
        next_page, total_pages = fetch_and_insert_facts(page)

        if next_page and page < total_pages:
            page += 1
            time.sleep(
                1
            )  # Adding a delay between requests to avoid hitting the API too fast
        else:
            break


# Step 4: Start paginating and inserting data
paginate_facts()

# Step 5: Close the database connection
conn.close()

print("Data successfully paginated and inserted into 'cat_facts.db'.")

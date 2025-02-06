import pandas as pd
import psycopg2  # For PostgreSQL interaction (install: pip install psycopg2-binary)
import os

# --- Configuration (Best practice to store these securely, not directly in code) ---
CSV_FILE_PATH = os.environ.get("CSV_FILE_PATH") or "data_to_import.csv"  # Use environment variable for path
DB_HOST = os.environ.get("DB_HOST") or "your_db_host"
DB_NAME = os.environ.get("DB_NAME") or "your_db_name"
DB_USER = os.environ.get("DB_USER") or "your_db_user"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or "your_db_password"


def clean_and_format_data(df):
    """Performs data cleaning and formatting."""

    # Example 1: Convert 'date' column to datetime objects
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Handle invalid dates

    # Example 2: Clean up inconsistent 'city' names (more complex cleaning)
    if 'city' in df.columns:
        df['city'] = df['city'].str.strip().str.title() # Remove leading/trailing spaces and capitalize

    # Example 3: Handle missing values (replace with a default or drop rows)
    # df.fillna(0, inplace=True)  # Replace NaN with 0 (be careful with this!)
    df.dropna(subset=['required_column'], inplace=True) # Drop rows where 'required_column' is empty

    return df


def import_data_to_postgres(df):
    """Imports the cleaned data to a PostgreSQL database."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()

        # Create table if it doesn't exist (adapt to your table schema)
        create_table_query = """
            CREATE TABLE IF NOT EXISTS your_table_name (
                id SERIAL PRIMARY KEY,  -- Example ID column
                date DATE,
                city TEXT,
                -- ... other columns ...
            );
        """
        cur.execute(create_table_query)
        conn.commit()

        # Efficiently insert data using parameterized query (prevents SQL injection)
        for index, row in df.iterrows():
            insert_query = """
                INSERT INTO your_table_name (date, city, ...)  -- Add other columns
                VALUES (%s, %s, ...)  -- Add placeholders for other columns
            """
            values = (row['date'], row['city'], ...) # Add other columns
            cur.execute(insert_query, values)

        conn.commit()
        print("Data imported successfully!")

    except (Exception, psycopg2.Error) as error:
        print(f"Error importing data: {error}")

    finally:
        if conn:
            cur.close()
            conn.close()


def main():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        cleaned_df = clean_and_format_data(df)
        import_data_to_postgres(cleaned_df)

    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
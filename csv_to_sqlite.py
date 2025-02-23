#!/usr/bin/env python3

import sys
import os
import sqlite3
import csv

def main():
    # We expect two arguments: database name and CSV file name.
    if len(sys.argv) != 3:
        print("Usage: python csv_to_sqlite.py <database.db> <input.csv>")
        sys.exit(1)

    db_name = sys.argv[1]
    csv_file = sys.argv[2]

    # Derive table name from CSV filename, minus path and extension.
    table_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Connect to (or create) the SQLite database.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the CSV.
    with open(csv_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        # The first row is the header, which we expect to be valid SQL column names.
        header = next(reader)

        # Build a CREATE TABLE statement with each column as TEXT.
        columns_definition = ", ".join([f"{col} TEXT" for col in header])
        create_table_sql = f"CREATE TABLE {table_name} ({columns_definition});"

        # Create the table.
        cursor.execute(create_table_sql)

        # Prepare an INSERT statement with placeholders for each column.
        placeholders = ", ".join(["?"] * len(header))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        # Insert each row from the CSV.
        for row in reader:
            cursor.execute(insert_sql, row)

    # Commit the transaction and close the connection.
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

import mysql.connector
from mysql.connector import Error

def insert_objects_to_db(connection, objects, table_name, field_mapping):
    try:
        if not objects:
            print("No objects to insert.")
            return

        # Map object fields to table fields
        mapped_fields = ', '.join(field_mapping.values())
        values_placeholder = ', '.join(['%s'] * len(field_mapping))

        # Construct the SQL query for batch insert
        sql = f"INSERT INTO {table_name} ({mapped_fields}) VALUES ({values_placeholder})"

        # Prepare the data for batch insertion
        data = [
            tuple(getattr(obj, k) for k in field_mapping.keys())
            for obj in objects
        ]

        # Execute the batch insert
        cursor = connection.cursor()
        cursor.executemany(sql, data)
        connection.commit()

        print(f"{cursor.rowcount} records inserted successfully into {table_name} table.")

    except Error as e:
        print(f"Error while inserting objects into MySQL table: {e}")

    finally:
        cursor.close()
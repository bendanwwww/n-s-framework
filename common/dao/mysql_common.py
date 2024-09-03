from mysql.connector import Error

def insert_objects_to_db(connection, table_name, objects, ignore_fields=None):
    """
    Inserts a list of objects into the specified MySQL table, ignoring specified fields.

    :param connection: A MySQL connection object.
    :param table_name: The name of the table where the data should be inserted.
    :param objects: A list of objects to insert, each with attributes matching the table's columns.
    :param ignore_fields: A list of field names to ignore during the insertion.
    """
    if not objects:
        print("No objects to insert.")
        return

    if ignore_fields is None:
        ignore_fields = []

    # Extract fields from the first object, excluding ignored fields
    all_fields = vars(objects[0]).keys()
    fields = [field for field in all_fields if field not in ignore_fields]
    
    if not fields:
        print("All fields are ignored.")
        return
    
    columns = ', '.join(fields)
    placeholders = ', '.join(['%s'] * len(fields))

    # Construct the SQL query
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Prepare the data for batch insertion, excluding ignored fields
    values_list = [tuple(vars(obj)[field] for field in fields) for obj in objects]

    cursor = connection.cursor()
    try:
        # Execute the SQL command for batch insert
        cursor.executemany(sql, values_list)
        # Commit the changes in the database
        connection.commit()
        print(f"Records inserted successfully into {table_name} table")
    except Error as err:
        # Rollback in case of error
        connection.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()
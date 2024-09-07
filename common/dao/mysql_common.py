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

def fetch_data_and_convert_to_class(connection, table_name, class_obj, ignore_fields=None, extra_condition=None):
    """
    Fetches data from the given MySQL table and converts each row into an instance of the provided class.
    
    Args:
        connection: The MySQL database connection object.
        table_name: The name of the table from which to fetch data.
        class_obj: The class to which the data will be mapped (with no-arg __init__).
        ignore_fields: A list of field names in the class to ignore if not present in the MySQL table.
        extra_condition: An optional SQL condition to filter the results (e.g., 'WHERE id = 5').
    
    Returns:
        A list of class_obj instances populated with data from the MySQL table.
    """
    if ignore_fields is None:
        ignore_fields = []

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Build the SQL query dynamically, incorporating the query condition if provided
    query = f"SELECT * FROM {table_name}"
    if extra_condition:
        query += f" {extra_condition}"
    
    cursor.execute(query)

    # Get column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Dynamically map the data to the provided class
    object_list = []
    for row in rows:
        # Create an instance of the class with no arguments
        obj = class_obj()

        # Populate the attributes of the class object
        for field, value in zip(column_names, row):
            if field not in ignore_fields and hasattr(obj, field):
                setattr(obj, field, value)

        object_list.append(obj)

    return object_list



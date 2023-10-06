import streamlit as st
import sqlite3
import pandas as pd
def insert_record(table_name):
    """
    Inserts a new record into the specified table in the LGD database.

    Parameters:
    - table_name (str): The name of the table to insert the record into.

    Returns:
    - None
    """
    st.header("Insert Record")
    # Connect to the SQLite database
    conn = sqlite3.connect("lgd_database.db")
    cursor = conn.cursor()

    # Retrieve the first 5 rows from the table
    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # Convert the rows to a DataFrame
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    df = df.iloc[:, :-1]
    # Display the retrieved rows in a table
    st.subheader("Existing Records")
    st.write(df)

    # Set default values for level_name and level_code based on table_name
    if table_name == "states":
        level_name = "State"
        level_code = 1
    elif table_name == "district":
        level_name = "District"
        level_code = 2
    elif table_name == "sub_district":
        level_name = "Sub-district"
        level_code = 3
    elif table_name == "block":
        level_name = "Block"
        level_code = 4
    elif table_name == "gp":
        level_name = "Gram Panchayats"
        level_code = 5
    else:
        level_name = ""
        level_code = 0

    # Input fields for entityLGDCode and levelCode
    entity_lgd_code = st.number_input("Entity LGD Code", min_value=0, step=1)

    # Input field for entityName
    entity_name = st.text_input("Entity Name")

    # Input field for entityNameVariants
    entity_name_variants = st.text_input("Entity Name Variants")

    # Input field for entityParent
    entity_parent = st.number_input("Entity Parent", min_value=0, step=1)

    if level_name and level_code:
        st.text(f"Level Name: {level_name}")
        st.text(f"Level Code: {level_code}")
    else:
        # Input fields for levelName and levelCode
        level_name = st.text_input("Level Name")
        level_code = st.number_input("Level Code", min_value=0, step=1)

    # Insert button
    if st.button("Insert"):
        # Perform validation checks before inserting the record
        errors = []

        if entity_lgd_code == 0:
            errors.append("Entity LGD Code cannot be zero.")

        if level_code == 0:
            errors.append("Level Code cannot be zero.")

        if not entity_name or not isinstance(entity_name, str):
            errors.append("Entity Name is required and must be a text.")

        if not level_name or not isinstance(level_name, str):
            errors.append("Level Name is required and must be a text.")

        if not entity_name_variants or not isinstance(entity_name_variants, str):
            errors.append("Entity Name Variants is required and must be a text.")

        if not entity_parent or not isinstance(entity_parent, int):
            errors.append("Entity Parent is required and must be an integer.")

        if errors:
            st.error("\n".join(errors))
        else:
            # Connect to the SQLite database
            conn = sqlite3.connect("lgd_database.db")
            cursor = conn.cursor()

            # Check if the entityLGDCode already exists in the table
            select_query = f"SELECT entityLGDCode FROM {table_name} WHERE entityLGDCode = ?"
            cursor.execute(select_query, (entity_lgd_code,))
            existing_code = cursor.fetchone()

            if existing_code:
                st.error("Entity LGD Code already exists in the table.")
            else:
                # Prepare the SQL query for creating the table if it doesn't exist
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    entityLGDCode INTEGER PRIMARY KEY,
                    entityName TEXT,
                    levelCode INTEGER,
                    levelName TEXT,
                    entityNameVariants TEXT,
                    entityParent INTEGER
                )
                """
                cursor.execute(create_table_query)

                # Prepare the SQL query for inserting the record
                insert_query = f"""
                INSERT INTO {table_name} (entityLGDCode, entityName, levelCode, levelName, entityNameVariants, entityParent)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                values = (entity_lgd_code, entity_name, level_code, level_name, entity_name_variants, entity_parent)

                try:
                    # Execute the SQL query
                    cursor.execute(insert_query, values)
                    conn.commit()
                    st.success("Record inserted successfully!")
                except sqlite3.Error as e:
                    st.error("An error occurred while inserting the record: {}".format(e))
                    conn.rollback()
                finally:
                    # Close the database connection
                    cursor.close()
                    conn.close()

                # Reset the input fields
                entity_lgd_code = 0
                level_code = 0
                entity_name = ""
                level_name = ""
                entity_name_variants = ""
                entity_parent = 0


def update_record(table_name):
    """
    Update a record in a SQLite database table.

    :param table_name: The name of the table to update the record in.
    :type table_name: str

    :return: None
    :rtype: None
    """
    st.header("Update Record")

    # Input field for entityLGDCode
    entity_lgd_code = st.number_input("Entity LGD Code", min_value=0, step=1)

    # Input field for entityName
    entity_name = st.text_input("Entity Name")

    # Input field for entityNameVariants
    entity_name_variants = st.text_input("Entity Name Variants")

    # Input field for entityParent
    entity_parent = st.number_input("Entity Parent", min_value=0, step=1)

    # Update button
    if st.button("Update"):
        # Perform validation checks before updating the record
        errors = []

        if entity_lgd_code == 0:
            errors.append("Entity LGD Code cannot be zero.")

        if not entity_name or not isinstance(entity_name, str):
            errors.append("Entity Name is required and must be a text.")

        if not entity_name_variants or not isinstance(entity_name_variants, str):
            errors.append("Entity Name Variants is required and must be a text.")

        if not entity_parent or not isinstance(entity_parent, int):
            errors.append("Entity Parent is required and must be an integer.")

        if errors:
            st.error("\n".join(errors))
        else:
            # Connect to the SQLite database
            conn = sqlite3.connect("lgd_database.db")
            cursor = conn.cursor()

            # Prepare the SQL query for updating the record
            update_query = f"""
            UPDATE {table_name}
            SET entityName = ?, entityNameVariants = ?, entityParent = ?
            WHERE entityLGDCode = ?
            """
            values = (entity_name, entity_name_variants, entity_parent, entity_lgd_code)

            try:
                # Execute the SQL query
                cursor.execute(update_query, values)
                conn.commit()
                st.success("Record updated successfully!")
            except sqlite3.Error as e:
                st.error("An error occurred while updating the record: {}".format(e))
                conn.rollback()
            finally:
                # Close the database connection
                cursor.close()
                conn.close()

            # Reset the input fields
            entity_lgd_code = 0
            entity_name = ""
            entity_name_variants = ""
            entity_parent = 0

def delete_record(table_name):
    """
    Deletes a record from the specified table in an SQLite database based on the entityLGDCode.
    
    :param table_name: Name of the table to delete the record from.
    :type table_name: str
    
    :return: None
    :rtype: None
    """
    st.header("Delete Record")

    # Input field for entityLGDCode
    entity_lgd_code = st.number_input("Entity LGD Code", min_value=0, step=1)

    # Delete button
    if st.button("Delete"):
        # Connect to the SQLite database
        conn = sqlite3.connect("lgd_database.db")
        cursor = conn.cursor()

        # Prepare the SQL query for deleting the record
        delete_query = f"""
        DELETE FROM {table_name}
        WHERE entityLGDCode = ?
        """
        values = (entity_lgd_code,)

        try:
            # Execute the SQL query
            cursor.execute(delete_query, values)
            conn.commit()
            st.success("Record deleted successfully!")
        except sqlite3.Error as e:
            st.error("An error occurred while deleting the record: {}".format(e))
            conn.rollback()
        finally:
            # Close the database connection
            cursor.close()
            conn.close()

        # Reset the input fields
        entity_lgd_code = 0

""" if __name__ == "__main__":
    table_name = "block"  # Provide the table name here

    # Usage examples
    update_record(table_name)
    delete_record(table) """


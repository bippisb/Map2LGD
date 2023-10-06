import sqlite3
import requests
import sqlite3
import hashlib

def fetch_data_from_api(code,local_body_type_code):
    url = f'https://lgdirectory.gov.in/webservices/lgdws/localBodyList?stateCode={code}&localbodyTypeCode={local_body_type_code}'
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the API.")
        return None

def calculate_hash(data):
    hash_object = hashlib.sha256(str(data).encode())
    return hash_object.hexdigest()


def get_level_code(tablename):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()
    # Execute the SQL query
    query = f"SELECT entityLGDCode FROM {tablename}"
    cursor.execute(query)

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Extract the entityLGDCode values into a Python list
    result = [row[0] for row in rows]

    # Close the cursor and connection
    cursor.close()

    # Print the final result
    return result



def check_and_update_data():
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/villageListWithHierarchy?subDistrictCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/blockList?districtCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/getBlockwiseMappedGP?blockCode='

    try:
        result = get_level_code("states")
        for code in result:
            print(code)
            for local_body_type_code in range(30):
                try:
                    data = fetch_data_from_api(str(code), local_body_type_code)
                    if data:
                        data_hash = calculate_hash(data)
                        insert_local_body_data_in_database(data, data_hash, code)
                    else:
                        print("Failed to fetch data from the API.")
                except Exception as e:
                    print("An error occurred:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))

def insert_district_data_in_database(data,data_hash, code):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS district (
                        entityLGDCode INTEGER PRIMARY KEY,
                        census2001Code TEXT,
                        census2011Code TEXT,
                        entityName TEXT,
                        levelCode INTEGER,
                        levelName TEXT,
                        entityNameVariants TEXT,
                        entityParent TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data into the table
        for item in data:
            entity_lgd_code = item['districtCode']
            census_2001_code = item['census2001Code']
            census_2011_code = item['census2011Code']
            entity_name = item['districtNameEnglish']
            level_code = 2
            level_name = "District"
            entity_name_variants = item['districtNameLocal']
            entity_parent = code

            cursor.execute('''INSERT INTO district (
                                entityLGDCode, census2001Code, census2011Code, entityName,
                                levelCode, levelName, entityNameVariants, entityParent,dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)''',
                           (
                               entity_lgd_code, census_2001_code, census_2011_code, entity_name,
                               level_code, level_name, entity_name_variants, entity_parent,data_hash
                           ))
            print(f"Data for districtCode: {entity_lgd_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except Exception as e:
        # Rollback the transaction in case of any error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()

import sqlite3

def insert_sub_district_data_in_database(data,datahash ,code):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS sub_district (
                        entityLGDCode INTEGER PRIMARY KEY,
                        census2001Code TEXT,
                        census2011Code TEXT,
                        entityName TEXT,
                        levelCode INTEGER,
                        levelName TEXT,
                        entityNameVariants TEXT,
                        entityParent TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data into the table
        for item in data:
            entity_lgd_code = item['subdistrictCode']
            census_2001_code = item['census2001Code']
            census_2011_code = item['census2011Code']
            entity_name = item['subdistrictNameEnglish']
            level_code = 3
            level_name = "sub_district"
            entity_name_variants = item['subdistrictNameLocal']
            entity_parent = code

            cursor.execute('''INSERT INTO sub_district (
                                entityLGDCode, census2001Code, census2011Code, entityName,
                                levelCode, levelName, entityNameVariants, entityParent, dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)''',
                           (
                               entity_lgd_code, census_2001_code, census_2011_code, entity_name,
                               level_code, level_name, entity_name_variants, entity_parent,datahash
                           ))
            print(f"Data for subdistrictCode: {entity_lgd_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except Exception as e:
        # Rollback the transaction in case of any error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()

import sqlite3

def insert_block_data_in_database(data,datahash ,code):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS block (
                        entityLGDCode INTEGER PRIMARY KEY,
                        entityName TEXT,
                        levelCode INTEGER,
                        levelName TEXT,
                        entityNameVariants TEXT,
                        entityParent TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data into the table
        for item in data:
            entity_lgd_code = item['blockCode']
            entity_name = item['blockNameEnglish']
            level_code = 4
            level_name = "block"
            entity_name_variants = item['blockNameLocal']
            entity_parent = code

            cursor.execute('''INSERT INTO block (
                                entityLGDCode, entityName,
                                levelCode, levelName, entityNameVariants, entityParent, dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (
                               entity_lgd_code, entity_name,
                               level_code, level_name, entity_name_variants, entity_parent,datahash
                           ))
            print(f"Data for block: {entity_lgd_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except Exception as e:
        # Rollback the transaction in case of any error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()
import sqlite3
import urllib3

def insert_gp_data_in_database(data, datahash, code):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS gp (
                        entityLGDCode INTEGER PRIMARY KEY,
                        entityName TEXT,
                        levelCode INTEGER,
                        levelName TEXT,
                        entityNameVariants TEXT,
                        entityParent TEXT,
                        entityParentName TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data into the table
        for item in data:
            entity_lgd_code = item['localBodyCode']
            entity_name = item['localBodyNameEnglish']
            level_code = 5
            level_name = "Gram Panchayats"
            entity_name_variants = item['localBodyNameLocal']
            entity_parent = code
            entity_parent_name = "block"

            cursor.execute('''INSERT INTO gp (
                                entityLGDCode, entityName,
                                levelCode, levelName, entityNameVariants, entityParent,entityParentName, dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?,?)''',
                           (
                               entity_lgd_code, entity_name,
                               level_code, level_name, entity_name_variants, entity_parent,entity_parent_name,datahash
                           ))
            print(f"Data for gp: {entity_lgd_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except urllib3.exceptions.TimeoutError as te:
        print("Timeout error occurred while making the HTTP request.")
        # Handle the timeout error here, e.g., retry the request or log the error.

    except Exception as e:
        # Rollback the transaction in case of any other error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()

import sqlite3
import urllib3

def insert_local_body_data_in_database(data, datahash, code):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS local_body (
                        entityLGDCode INTEGER PRIMARY KEY,
                        entityName TEXT,
                        entitylocalBodyTypeName TEXT,
                        levelCode INTEGER,
                        levelName TEXT,
                        entityNameVariants TEXT,
                        entityParent TEXT,
                        entityParentName TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data into the table
        for item in data:
            entity_lgd_code = item['localBodyCode']
            entity_name = item['localBodyNameEnglish']
            entity_local_body_type_name = item['localBodyTypeName']
            level_code = -1
            level_name = "Local Body Type Name"
            entity_name_variants = item['localBodyNameLocal']
            entity_parent = code
            entity_parent_name = "state"

            cursor.execute('''INSERT INTO local_body (
                                entityLGDCode, entityName,entitylocalBodyTypeName,
                                levelCode, levelName, entityNameVariants, entityParent,entityParentName, dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)''',
                           (
                               entity_lgd_code, entity_name,entity_local_body_type_name,
                               level_code, level_name, entity_name_variants, entity_parent,entity_parent_name,datahash
                           ))
            print(f"Data for gp: {entity_lgd_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except urllib3.exceptions.TimeoutError as te:
        print("Timeout error occurred while making the HTTP request.")
        # Handle the timeout error here, e.g., retry the request or log the error.

    except Exception as e:
        # Rollback the transaction in case of any other error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()


import sqlite3

def store_village_data_in_database(data, data_hash):
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS villages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stateCode INTEGER,
                        stateNameEnglish TEXT,
                        districtCode INTEGER,
                        districtNameEnglish TEXT,
                        subDistrictCode INTEGER,
                        subDistrictNameEnglish TEXT,
                        blockCode INTEGER,
                        blockNameEnglish TEXT,
                        localBodyCode INTEGER,
                        localBodyTypeCode INTEGER,
                        localBodyNameEnglish TEXT,
                        villageCode INTEGER,
                        villageNameEnglish TEXT,
                        villageStatus TEXT,
                        dataHash TEXT
                    )''')

    try:
        # Start a transaction
        conn.execute("BEGIN TRANSACTION")

        # Insert the data
        for item in data:
            state_code = item['stateCode']
            state_name = item['stateNameEnglish']
            district_code = item['districtCode']
            district_name = item['districtNameEnglish']
            subdistrict_code = item['subDistrictCode']
            subdistrict_name = item['subDistrictNameEnglish']
            block_code = item['blockCode']
            block_name = item['blockNameEnglish']
            local_body_code = item['localBodyCode']
            local_body_type_code = item['localBodyTypeCode']
            local_body_name = item['localBodyNameEnglish']
            village_code = item['villageCode']
            village_name = item['villageNameEnglish']
            village_status = item['villageStatus']

            # Insert a new row
            cursor.execute('''INSERT INTO villages (
                                stateCode, stateNameEnglish, districtCode, districtNameEnglish,
                                subDistrictCode, subDistrictNameEnglish, blockCode, blockNameEnglish,
                                localBodyCode, localBodyTypeCode, localBodyNameEnglish,
                                villageCode, villageNameEnglish, villageStatus, dataHash
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (
                               state_code, state_name, district_code, district_name,
                               subdistrict_code, subdistrict_name, block_code, block_name,
                               local_body_code, local_body_type_code, local_body_name,
                               village_code, village_name, village_status, data_hash
                           ))
            print(f"Data for stateCode: {state_code}, villageCode: {village_code} inserted successfully.")

        # Commit the changes
        conn.execute("COMMIT")
        print("All data inserted successfully.")

    except Exception as e:
        # Rollback the transaction in case of any error
        conn.execute("ROLLBACK")
        print(f"Error occurred: {str(e)}")

    finally:
        # Close the connection
        conn.close()



def check_write_and_update_data(data,table_name):
    try:
        data = data
        if data:
            conn = sqlite3.connect('lgd_database.db')
            cursor = conn.cursor()

            # Retrieve the stored data from the database
            cursor.execute(f'SELECT entityLGDCode, entityName FROM {table_name}')
            rows = cursor.fetchall()

            changed_rows = set()

            for item in data:
                if table_name == 'states':
                    entity_lgd_code = item['stateCode']
                    entity_name = item['stateNameEnglish']
                elif table_name == 'district':
                    entity_lgd_code = item['districtCode']
                    entity_name = item['districtNameEnglish']
                elif table_name == 'sub_district':
                    entity_lgd_code = item['subdistrictCode']
                    entity_name = item['subdistrictNameEnglish']
                elif table_name == 'block':
                    entity_lgd_code = item['blockCode']
                    entity_name = item['blockNameEnglish']
                elif table_name == 'gp':
                    entity_lgd_code = item['localBodyCode']
                    entity_name = item['localBodyNameEnglish']
                """ elif table_name == 'villages':
                    entity_lgd_code = item['localBodyCode']
                    entity_name = item['localBodyNameEnglish'] """


                # Find the matching row in the database
                matching_rows = [row for row in rows if row[0] == entity_lgd_code]

                if matching_rows:
                    # Check if entityLGDCode and entityName have changed
                    row = matching_rows[0]
                    if row[0] != entity_lgd_code or row[1] != entity_name:
                        changed_rows.add((entity_lgd_code, entity_name))

            if changed_rows:
                print("The following rows have changed:")
                for row in changed_rows:
                    entity_lgd_code, entity_name = row
                    print("entityLGDCode:", entity_lgd_code)
                    print("entityName:", entity_name)
                    print()
                    # Update the values in the database
                    cursor.execute(f"UPDATE {table_name} SET entityName = ? WHERE entityLGDCode = ?", (entity_name, entity_lgd_code))
                    conn.commit()          
                print("Data updated successfully!")

            else:
                print("Data has not changed.")

            # Update the data hash in the database

            conn.close()

        else:
            print("Failed to fetch data from the API.")

    except Exception as e:
        print("An error occurred:", str(e))


def fetch_data_from_api_update(url):
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the API.")
        return None
    

def update_all_data():
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/villageListWithHierarchy?subDistrictCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/blockList?districtCode='
    #url = 'https://lgdirectory.gov.in/webservices/lgdws/getBlockwiseMappedGP?blockCode='
    name_pair = {'district':'states','sub_district':'district','block':'district','gp':'block'}
    for key, value in name_pair.items():
        table_name = key
        print('table name:', table_name)
        try:
            result = get_level_code(value)
            for code in result:
                try:
                    if table_name == 'states':
                        url = f'https://lgdirectory.gov.in/webservices/lgdws/stateList'
                    elif table_name == 'district':
                        url = f'https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode={code}'
                    elif table_name == 'sub_district':
                        url = f'https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode={code}'
                    elif table_name == 'block':
                        url = f'https://lgdirectory.gov.in/webservices/lgdws/blockList?districtCode={code}'
                    elif table_name == 'gp':
                        url = f'https://lgdirectory.gov.in/webservices/lgdws/getBlockwiseMappedGP?blockCode={code}'
                    data = fetch_data_from_api_update(url)

                    if data:
                        check_write_and_update_data(data,table_name)
                    else:
                        print("Failed to fetch data from the API.")
                except Exception as e:
                    print("An error occurred:", str(e))
        except Exception as e:
            print("An error occurred:", str(e))
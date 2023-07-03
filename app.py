from flask import Flask
import pandas as pd
import mysql.connector

app = Flask(__name__)

@app.route('/read-excel')
def read_excel():
    # Read the XLSX file, skipping the first row (header)
    df = pd.read_excel('Gedung 17 Lantai.xlsx', sheet_name='Structural Framing', skiprows=2)

    # Convert DataFrame to a string with ~ delimiter
    df_string = df.to_csv(sep='~', index=False)

    # Save the string to a TXT file
    with open('output.txt', 'w') as txt_file:
        txt_file.write(df_string)

    # Read the TXT file and get the contents
    with open('output.txt', 'r') as txt_file:
        file_contents = txt_file.read()

    # Split the contents into lines
    lines = file_contents.split('\n')

    # Exclude any empty lines
    lines = [line for line in lines if line]

    # Initialize a set to store the unique desired values
    desired_values = set()

    for line in lines:
        rows = line.split('~')
        if len(rows) >= 3:
            value = rows[2]  # Access the value at index 2
            dimension = value.split(': ')[-1]  # Extract the dimension from the value
            desired_values.add(dimension)

    # Join the lines back into a single string
    file_contents_without_header = '\n'.join(lines)

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_wbs_bim_revit'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Insert the unique dimensions into the MySQL table
    for dimension in desired_values:
        query = "INSERT INTO revit (name) VALUES (%s)"
        values = (dimension,)
        cursor.execute(query, values)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    # Return the extracted dimensions
    return ', '.join(desired_values)

@app.route('/read-multiple-sheet')
def read_multiple_sheet():
    # Define the list of sheet names to process
    sheet_names = ['Sheet1', 'Sheet2', 'Sheet3']  # Update with your sheet names

    # Initialize a set to store the unique desired values
    desired_values = set()

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_wbs_bim_revit'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    for sheet_name in sheet_names:
        # Read the XLSX file, skipping the first row (header)
        df = pd.read_excel('Gedung 17 Lantai.xlsx', sheet_name=sheet_name, skiprows=2)

        # Convert DataFrame to a string with ~ delimiter
        df_string = df.to_csv(sep='~', index=False)

        # Save the string to a TXT file
        with open('output.txt', 'w') as txt_file:
            txt_file.write(df_string)

        # Read the TXT file and get the contents
        with open('output.txt', 'r') as txt_file:
            file_contents = txt_file.read()

        # Split the contents into lines
        lines = file_contents.split('\n')

        # Exclude any empty lines
        lines = [line for line in lines if line]

        for line in lines:
            rows = line.split('~')
            if len(rows) >= 3:
                value = rows[2]  # Access the value at index 2
                dimension = value.split(': ')[-1]  # Extract the dimension from the value
                desired_values.add(dimension)

    # Join the lines back into a single string
    file_contents_without_header = '\n'.join(lines)

    # Insert the unique dimensions into the MySQL table
    for dimension in desired_values:
        query = "INSERT INTO revit (name) VALUES (%s)"
        values = (dimension,)
        cursor.execute(query, values)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    # Return the extracted dimensions
    return ', '.join(desired_values)

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()


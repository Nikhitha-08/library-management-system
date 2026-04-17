import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to create a connection to the MySQL database
def create_connection(host="localhost", user="root", passwd="2008", database="LibraryManagement"):
    connection = None
    try:
        temp_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd
        )
        temp_cursor = temp_connection.cursor()
        temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        temp_cursor.close()
        temp_connection.close()

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=database
        )

        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS Books (
                isbn VARCHAR(13) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                publication_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                membership_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Loans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_isbn VARCHAR(13),
                member_id INT,
                loan_date DATETIME,
                return_date DATETIME,
                FOREIGN KEY (book_isbn) REFERENCES Books(isbn) ON DELETE CASCADE,
                FOREIGN KEY (member_id) REFERENCES Members(id) ON DELETE CASCADE
            );
            """
        ]

        cursor = connection.cursor()
        for query in table_queries:
            cursor.execute(query)
        cursor.close()

        print("Connection to MySQL DB successful and tables ensured.")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to execute a query that modifies data
def execute_query(connection, query):
    if connection is None:
        print("Database connection not established. Skipping query execution.")
        return
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to execute a read query
def read_query(connection, query):
    if connection is None:
        print("Database connection not established. Skipping query execution.")
        return None
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

# Function to manage Books
def manage_books(connection):
    while True:
        print("\nBook Management Options:")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Add Book
            isbn = input("Enter Book ISBN: ")
            title = input("Enter Book Title: ")
            genre = input("Enter Book Genre: ")
            publication_date = input("Enter Publication Date (YYYY-MM-DD): ")
            query = f"""
            INSERT INTO Books (isbn, title, genre, publication_date)
            VALUES ('{isbn}', '{title}', '{genre}', '{publication_date}');
            """
            execute_query(connection, query)
        elif choice == '2':  # Update Book
            isbn = input("Enter Book ISBN to Update: ")
            title = input("Enter New Book Title: ")
            genre = input("Enter New Book Genre: ")
            publication_date = input("Enter New Publication Date (YYYY-MM-DD): ")
            query = f"""
            UPDATE Books
            SET title = '{title}', genre = '{genre}', publication_date = '{publication_date}'
            WHERE isbn = '{isbn}';
            """
            execute_query(connection, query)
        elif choice == '3':  # Remove Book
            isbn = input("Enter ISBN of the Book to Remove: ")
            query = f"DELETE FROM Books WHERE isbn = '{isbn}';"
            execute_query(connection, query)
        elif choice == '4':  # View All Books
            books = read_query(connection, "SELECT * FROM Books;")
            for book in books or []:
                print(book)
        elif choice == '5':  # Search Book
            search_term = input("Enter Book Title or ISBN to Search: ")
            query = f"""
            SELECT * FROM Books
            WHERE title LIKE '%{search_term}%' OR isbn = '{search_term}';
            """
            books = read_query(connection, query)
            if books:
                for book in books:
                    print(book)
            else:
                print("No books found matching the search criteria.")
        elif choice == '6':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")

# Function to manage Members
def manage_members(connection):
    while True:
        print("\nMember Management Options:")
        print("1. Add Member")
        print("2. Update Member")
        print("3. Remove Member")
        print("4. View All Members")
        print("5. Search Member")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Add Member
            name = input("Enter Member Name: ")
            email = input("Enter Member Email: ")
            membership_date = datetime.now().strftime('%Y-%m-%d')
            query = f"""
            INSERT INTO Members (name, email, membership_date)
            VALUES ('{name}', '{email}', '{membership_date}');
            """
            execute_query(connection, query)
        elif choice == '2':  # Update Member
            member_id = input("Enter ID of the Member to Update: ")
            name = input("Enter New Member Name: ")
            email = input("Enter New Member Email: ")
            query = f"""
            UPDATE Members
            SET name = '{name}', email = '{email}'
            WHERE id = {member_id};
            """
            execute_query(connection, query)
        elif choice == '3':  # Remove Member
            member_id = input("Enter ID of the Member to Remove: ")
            query = f"DELETE FROM Members WHERE id = {member_id};"
            execute_query(connection, query)
        elif choice == '4':  # View All Members
            members = read_query(connection, "SELECT * FROM Members;")
            for member in members or []:
                print(member)
        elif choice == '5':  # Search Member
            search_term = input("Enter Member Name or Email to Search: ")
            query = f"""
            SELECT * FROM Members
            WHERE name LIKE '%{search_term}%' OR email LIKE '%{search_term}%';
            """
            members = read_query(connection, query)
            if members:
                for member in members:
                    print(member)
            else:
                print("No members found matching the search criteria.")
        elif choice == '6':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")# Function to display all records

def display_all_records(connection):
    print("\nAll Books:")
    books = read_query(connection, "SELECT * FROM Books;")
    if books:
        print("{:<13} | {:<50} | {:<20} | {:<20}".format("ISBN", "Book Title", "Genre", "Publication Date"))
        print("-" * 100)
        for book in books:
            isbn, title, genre, publication_date = book
            print("{:<13} | {:<50} | {:<20} | {:<20}".format(isbn, title, genre, publication_date))
    else:
        print("No books found.")

    print("\nAll Members:")
    members = read_query(connection, "SELECT * FROM Members;")
    if members:
        print("{:<5} | {:<20} | {:<30} | {:<15}".format("ID", "Member Name", "Email", "Membership Date"))
        print("-" * 80)
        for member in members:
            member_id, name, email, membership_date = member
            print("{:<5} | {:<20} | {:<30} | {:<15}".format(member_id, name, email, membership_date))
    else:
        print("No members found.")

    print("\nAll Loans:")
    loans = read_query(connection, """
    SELECT Loans.id, Books.title, Members.name, Loans.loan_date, Loans.return_date
    FROM Loans
    JOIN Books ON Loans.book_isbn = Books.isbn
    JOIN Members ON Loans.member_id = Members.id;
    """)
    if loans:
        print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format("ID", "Book Title", "Member Name", "Loan Date", "Return Date"))
        print("-" * 90)
        for loan in loans:
            loan_id, book_title, member_name, loan_date, return_date = loan
            formatted_loan_date = loan_date.strftime('%d-%m-%Y %H:%M')
            formatted_return_date = (return_date.strftime('%d-%m-%Y %H:%M') if return_date else "Not Returned")
            print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                loan_id, book_title, member_name, formatted_loan_date, formatted_return_date))
    else:
        print("No loans found.")

def manage_loans(connection):
    while True:
        print("\nLoan Management Options:")
        print("1. Rent a Book")
        print("2. Return a Book")
        print("3. View All Loans")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Rent a Book
            book_isbn = input("Enter Book ISBN: ")
            member_id = input("Enter Member ID: ")

            # Check if the book exists
            book_check_query = f"SELECT * FROM Books WHERE isbn = '{book_isbn}';"
            book_exists = read_query(connection, book_check_query)

            # Check if the member exists
            member_check_query = f"SELECT * FROM Members WHERE id = {member_id};"
            member_exists = read_query(connection, member_check_query)

            if not book_exists:
                print(f"Error: Book with ISBN '{book_isbn}' does not exist.")
            elif not member_exists:
                print(f"Error: Member with ID '{member_id}' does not exist.")
            else:
                loan_date = datetime.now()
                query = f"""
                INSERT INTO Loans (book_isbn, member_id, loan_date, return_date)
                VALUES ('{book_isbn}', {member_id}, '{loan_date}', NULL);
                """
                execute_query(connection, query)
                print("Book rented successfully.")

        elif choice == '2':  # Return a Book
            loan_id = input("Enter Loan ID to return: ")
            query = f"DELETE FROM Loans WHERE id = {loan_id};"
            execute_query(connection, query)
            print("Book returned successfully.")

        elif choice == '3':  # View All Loans
            loans = read_query(connection, """
            SELECT Loans.id, Books.title, Members.name, Loans.loan_date, Loans.return_date
            FROM Loans
            JOIN Books ON Loans.book_isbn = Books.isbn
            JOIN Members ON Loans.member_id = Members.id;
            """)
            if loans:
                print("\nLoans:")
                print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                    "ID", "Book Title", "Member Name", "Loan Date", "Return Date"))
                print("-" * 90)
                for loan in loans:
                    loan_id, book_title, member_name, loan_date, return_date = loan
                    formatted_loan_date = loan_date.strftime('%d-%m-%Y %H:%M')
                    formatted_return_date = (return_date.strftime('%d-%m-%Y %H:%M') if return_date else "Not Returned")
                    print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                        loan_id, book_title, member_name, formatted_loan_date, formatted_return_date))
            else:
                print("No loans found.")

        elif choice == '4':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")


# Main Program
def main():
    print("Welcome to the Library Management System!")
    connection = create_connection()

    while True:
        print("\nMain Menu:")
        print("1. Manage Books")
        print("2. Manage Members")
        print("3. Manage Loans")
        print("4. View All Records")
        print("5. Exit")
       
        choice = input("Choose an option: ")
        if choice == '1':
            manage_books(connection)
        elif choice == '2':
            manage_members(connection)
        elif choice == '3':
            manage_loans(connection)
        elif choice == '4':
            display_all_records(connection)
        elif choice == '5':
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

---------- Forwarded message ---------
From: Muthulakshmi Sankarapandian <srmg.muthulakshmi@gmail.com>
Date: Mon, 13 Jan, 2025, 1:22 pm
Subject: cs
To: <nikhithakatturajan@gmail.com>


import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to create a connection to the MySQL database
def create_connection(host="localhost", user="root", passwd="2008", database="LibraryManagement"):
    connection = None
    try:
        temp_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd
        )
        temp_cursor = temp_connection.cursor()
        temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        temp_cursor.close()
        temp_connection.close()

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=passwd,
            database=database
        )

        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS Books (
                isbn VARCHAR(13) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                publication_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                membership_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Loans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_isbn VARCHAR(13),
                member_id INT,
                loan_date DATETIME,
                return_date DATETIME,
                FOREIGN KEY (book_isbn) REFERENCES Books(isbn) ON DELETE CASCADE,
                FOREIGN KEY (member_id) REFERENCES Members(id) ON DELETE CASCADE
            );
            """
        ]

        cursor = connection.cursor()
        for query in table_queries:
            cursor.execute(query)
        cursor.close()

        print("Connection to MySQL DB successful and tables ensured.")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to execute a query that modifies data
def execute_query(connection, query):
    if connection is None:
        print("Database connection not established. Skipping query execution.")
        return
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to execute a read query
def read_query(connection, query):
    if connection is None:
        print("Database connection not established. Skipping query execution.")
        return None
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

# Function to manage Books
def manage_books(connection):
    while True:
        print("\nBook Management Options:")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Add Book
            isbn = input("Enter Book ISBN: ")
            title = input("Enter Book Title: ")
            genre = input("Enter Book Genre: ")
            publication_date = input("Enter Publication Date (YYYY-MM-DD): ")
            query = f"""
            INSERT INTO Books (isbn, title, genre, publication_date)
            VALUES ('{isbn}', '{title}', '{genre}', '{publication_date}');
            """
            execute_query(connection, query)
        elif choice == '2':  # Update Book
            isbn = input("Enter Book ISBN to Update: ")
            title = input("Enter New Book Title: ")
            genre = input("Enter New Book Genre: ")
            publication_date = input("Enter New Publication Date (YYYY-MM-DD): ")
            query = f"""
            UPDATE Books
            SET title = '{title}', genre = '{genre}', publication_date = '{publication_date}'
            WHERE isbn = '{isbn}';
            """
            execute_query(connection, query)
        elif choice == '3':  # Remove Book
            isbn = input("Enter ISBN of the Book to Remove: ")
            query = f"DELETE FROM Books WHERE isbn = '{isbn}';"
            execute_query(connection, query)
        elif choice == '4':  # View All Books
            books = read_query(connection, "SELECT * FROM Books;")
            for book in books or []:
                print(book)
        elif choice == '5':  # Search Book
            search_term = input("Enter Book Title or ISBN to Search: ")
            query = f"""
            SELECT * FROM Books
            WHERE title LIKE '%{search_term}%' OR isbn = '{search_term}';
            """
            books = read_query(connection, query)
            if books:
                for book in books:
                    print(book)
            else:
                print("No books found matching the search criteria.")
        elif choice == '6':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")

# Function to manage Members
def manage_members(connection):
    while True:
        print("\nMember Management Options:")
        print("1. Add Member")
        print("2. Update Member")
        print("3. Remove Member")
        print("4. View All Members")
        print("5. Search Member")
        print("6. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Add Member
            name = input("Enter Member Name: ")
            email = input("Enter Member Email: ")
            membership_date = datetime.now().strftime('%Y-%m-%d')
            query = f"""
            INSERT INTO Members (name, email, membership_date)
            VALUES ('{name}', '{email}', '{membership_date}');
            """
            execute_query(connection, query)
        elif choice == '2':  # Update Member
            member_id = input("Enter ID of the Member to Update: ")
            name = input("Enter New Member Name: ")
            email = input("Enter New Member Email: ")
            query = f"""
            UPDATE Members
            SET name = '{name}', email = '{email}'
            WHERE id = {member_id};
            """
            execute_query(connection, query)
        elif choice == '3':  # Remove Member
            member_id = input("Enter ID of the Member to Remove: ")
            query = f"DELETE FROM Members WHERE id = {member_id};"
            execute_query(connection, query)
        elif choice == '4':  # View All Members
            members = read_query(connection, "SELECT * FROM Members;")
            for member in members or []:
                print(member)
        elif choice == '5':  # Search Member
            search_term = input("Enter Member Name or Email to Search: ")
            query = f"""
            SELECT * FROM Members
            WHERE name LIKE '%{search_term}%' OR email LIKE '%{search_term}%';
            """
            members = read_query(connection, query)
            if members:
                for member in members:
                    print(member)
            else:
                print("No members found matching the search criteria.")
        elif choice == '6':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")# Function to display all records

def display_all_records(connection):
    print("\nAll Books:")
    books = read_query(connection, "SELECT * FROM Books;")
    if books:
        print("{:<13} | {:<50} | {:<20} | {:<20}".format("ISBN", "Book Title", "Genre", "Publication Date"))
        print("-" * 100)
        for book in books:
            isbn, title, genre, publication_date = book
            print("{:<13} | {:<50} | {:<20} | {:<20}".format(isbn, title, genre, publication_date))
    else:
        print("No books found.")

    print("\nAll Members:")
    members = read_query(connection, "SELECT * FROM Members;")
    if members:
        print("{:<5} | {:<20} | {:<30} | {:<15}".format("ID", "Member Name", "Email", "Membership Date"))
        print("-" * 80)
        for member in members:
            member_id, name, email, membership_date = member
            print("{:<5} | {:<20} | {:<30} | {:<15}".format(member_id, name, email, membership_date))
    else:
        print("No members found.")

    print("\nAll Loans:")
    loans = read_query(connection, """
    SELECT Loans.id, Books.title, Members.name, Loans.loan_date, Loans.return_date
    FROM Loans
    JOIN Books ON Loans.book_isbn = Books.isbn
    JOIN Members ON Loans.member_id = Members.id;
    """)
    if loans:
        print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format("ID", "Book Title", "Member Name", "Loan Date", "Return Date"))
        print("-" * 90)
        for loan in loans:
            loan_id, book_title, member_name, loan_date, return_date = loan
            formatted_loan_date = loan_date.strftime('%d-%m-%Y %H:%M')
            formatted_return_date = (return_date.strftime('%d-%m-%Y %H:%M') if return_date else "Not Returned")
            print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                loan_id, book_title, member_name, formatted_loan_date, formatted_return_date))
    else:
        print("No loans found.")

def manage_loans(connection):
    while True:
        print("\nLoan Management Options:")
        print("1. Rent a Book")
        print("2. Return a Book")
        print("3. View All Loans")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ")
        if choice == '1':  # Rent a Book
            book_isbn = input("Enter Book ISBN: ")
            member_id = input("Enter Member ID: ")

            # Check if the book exists
            book_check_query = f"SELECT * FROM Books WHERE isbn = '{book_isbn}';"
            book_exists = read_query(connection, book_check_query)

            # Check if the member exists
            member_check_query = f"SELECT * FROM Members WHERE id = {member_id};"
            member_exists = read_query(connection, member_check_query)

            if not book_exists:
                print(f"Error: Book with ISBN '{book_isbn}' does not exist.")
            elif not member_exists:
                print(f"Error: Member with ID '{member_id}' does not exist.")
            else:
                loan_date = datetime.now()
                query = f"""
                INSERT INTO Loans (book_isbn, member_id, loan_date, return_date)
                VALUES ('{book_isbn}', {member_id}, '{loan_date}', NULL);
                """
                execute_query(connection, query)
                print("Book rented successfully.")

        elif choice == '2':  # Return a Book
            loan_id = input("Enter Loan ID to return: ")
            query = f"DELETE FROM Loans WHERE id = {loan_id};"
            execute_query(connection, query)
            print("Book returned successfully.")

        elif choice == '3':  # View All Loans
            loans = read_query(connection, """
            SELECT Loans.id, Books.title, Members.name, Loans.loan_date, Loans.return_date
            FROM Loans
            JOIN Books ON Loans.book_isbn = Books.isbn
            JOIN Members ON Loans.member_id = Members.id;
            """)
            if loans:
                print("\nLoans:")
                print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                    "ID", "Book Title", "Member Name", "Loan Date", "Return Date"))
                print("-" * 90)
                for loan in loans:
                    loan_id, book_title, member_name, loan_date, return_date = loan
                    formatted_loan_date = loan_date.strftime('%d-%m-%Y %H:%M')
                    formatted_return_date = (return_date.strftime('%d-%m-%Y %H:%M') if return_date else "Not Returned")
                    print("{:<5} | {:<20} | {:<20} | {:<20} | {:<20}".format(
                        loan_id, book_title, member_name, formatted_loan_date, formatted_return_date))
            else:
                print("No loans found.")

        elif choice == '4':  # Back to Main Menu
            break
        else:
            print("Invalid option. Please try again.")


# Main Program
def main():
    print("Welcome to the Library Management System!")
    connection = create_connection()

    while True:
        print("\nMain Menu:")
        print("1. Manage Books")
        print("2. Manage Members")
        print("3. Manage Loans")
        print("4. View All Records")
        print("5. Exit")
       
        choice = input("Choose an option: ")
        if choice == '1':
            manage_books(connection)
        elif choice == '2':
            manage_members(connection)
        elif choice == '3':
            manage_loans(connection)
        elif choice == '4':
            display_all_records(connection)
        elif choice == '5':
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

#Database.py: Module that works with the database.

#importing Sqlite3 for database usage
import sqlite3

#Importing Modules.py for helping functions
import Modules as modules 


#Values for the database
#=========================================================================

#Name of the database (new name = new database)
databaseName = "BudgetTrackerDatabase.db"

#=========================================================================


#Function that creates the database
#=========================================================================

def createDatabase():
    #Connecting to the database and to the cursor 
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    #Checking tables
    #Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)
    
    #Expenses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Expenses 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        categoryId INTEGER,
        FOREIGN KEY(categoryId) REFERENCES Categories(id)
    )
    """)

    #Closing the database
    connection.commit()
    connection.close()
    
#=========================================================================
    

#Helping function for finding if the category is the same as the parameter 
#=========================================================================

def checkIfCategoryIsEqual(categoryName: str , categoryFetchedName):
    #checking if they are the same by lowering both of them to lowercase
    if categoryName.lower() != categoryFetchedName.lower():
        return False
    
    return True

#=========================================================================


#Creating a new category row
#=========================================================================

def addCategoryToDatabase(categoryName : str):
    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    #fixing the categoryName into format english
    categoryName = modules.formatName(categoryName)

    #Checking if category name exists 
    cursor.execute(
        "SELECT name FROM categories WHERE name = ?",
        (categoryName,)
    )
    fetchedCategoryName = cursor.fetchone()

    #Checking if name exists
    #if it doesnt exists we gonna create a new category
    if fetchedCategoryName == None:
        #Inserting a new category row
        cursor.execute("""
        INSERT INTO Categories
            (name)
            VALUES(?)
            """,
            (categoryName,)
        )
        print("Created a new category.")
    #if name exists    
    else:
        print("Category already exists.")

    #Closing the database
    connection.commit()
    connection.close()

#=========================================================================


#Creating a new category row
#=========================================================================
def addCategoryToDatabaseWithID(categoryName : str):
    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()


    #Inserting a new category row
    cursor.execute("""
    INSERT INTO Categories
        (name)
        VALUES(?)
        """,
        (categoryName,)
    )

    #Commitng the data into the database
    connection.commit()

    #Getting the new ID of the new category
    cursor.execute(
        "SELECT id FROM categories WHERE name = ?",
        (categoryName,)
    )
    fetchedID : int = cursor.fetchone()[0]

    #Closing the database
    connection.commit()
    connection.close()

    #returning the ID
    return fetchedID

#=========================================================================


def addExpenseToDatabase(expenseName : str , amount : float , categoryName : str):
    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor  = connection.cursor()

    #Checking if category exists and getting the ID of it
    cursor.execute(
        "SELECT id , name FROM categories WEHRE name = ?",
        (categoryName,)
    )
    categoryRow = cursor.fetchone()
    categoryFetchedID : int = categoryRow[0]
    categoryFetchedName : str = categoryRow[1]

    #Checking if the name is the same
    #if not create a new category for it and take the ID
    if categoryName.lower() != categoryFetchedName.lower():
        addCategoryToDatabaseWithID(categoryName)



    connection.commit()
    connection.close()


    
    

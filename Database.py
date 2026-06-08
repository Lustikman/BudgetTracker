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


#if user gave a new category in the input of expense creating a new category for it
#=========================================================================
def addCategoryToDatabaseForExpense(categoryName : str):
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

#Adding expense into the database
#=========================================================================
def addExpenseToDatabase(expenseName : str , amount : float , categoryName : str):
    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor  = connection.cursor()

    #changing the category name and expense name into format english
    categoryName = modules.formatName(categoryName)
    expenseName = modules.formatName(expenseName)

    #getting the id from the name of the category
    cursor.execute(
        "SELECT id FROM categories WHERE name = ?",
        (categoryName,)
    )
    categoryFetchedID = None

    #checkiing if the category even exists
    categoryRow = cursor.fetchone()
    if categoryRow == None:
        #Creating a new category with the input of name category user gave and take its ID
        categoryFetchedID = addCategoryToDatabaseForExpense(categoryName)

        #Closing the database
        connection.commit()
        connection.close()
    #if exists take the ID
    else:
        categoryFetchedID : int = categoryRow[0]

    
    #Inserting a new expense into the database
    cursor.execute("""
    INSERT INTO Expenses
        (name, amount, categoryId)
        VALUES(?, ?, ?)
        """,
        (expenseName, amount, categoryName)
    )

    #Commiting and closing the database
    connection.commit()
    connection.close()

#=========================================================================

    
    

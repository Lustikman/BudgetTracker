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
        "SELECT name FROM Categories WHERE name = ?",
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
        "SELECT id FROM Categories WHERE name = ?",
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
        "SELECT id FROM Categories WHERE name = ?",
        (categoryName,)
    )
    categoryFetchedID = None

    #checkiing if the category even exists
    categoryRow = cursor.fetchone()
    if categoryRow == None:

        #Closing the database for the new function to open it
        connection.commit()
        connection.close()

        #Creating a new category with the input of name category user gave and take its ID
        categoryFetchedID = addCategoryToDatabaseForExpense(categoryName)

        #Connecting to the database
        connection = sqlite3.connect(databaseName)
        cursor  = connection.cursor()

    #if exists take the ID
    else:
        categoryFetchedID : int = categoryRow[0]

    
    #Inserting a new expense into the database
    cursor.execute("""
    INSERT INTO Expenses
        (name, amount, categoryId)
        VALUES(?, ?, ?)
        """,
        (expenseName, amount, categoryFetchedID)
    )

    #Commiting and closing the database
    connection.commit()
    connection.close()

#=========================================================================


#Giving a list of expenses inside the category
#=========================================================================

def getListOfExpensesByCategory(categoryName : str):

    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor  = connection.cursor()

    #changing the format for the database format
    categoryName = modules.formatName(categoryName)

    #finding the id of the category
    cursor.execute(
        "SELECT id FROM Categories WHERE name = ?",
        (categoryName,)
    )
    fetchedID : int = cursor.fetchone()

    #checking if the ID exists if not end the function
    if fetchedID == None:
        print("Category Doesnt exist.")
        return
    
    else:
        fetchedID = fetchedID[0]
    
    #getting the id,amount,name and the category name of all expenses with the same id number
    cursor.execute("""
                   SELECT
                   Expenses.id,
                   Expenses.amount,
                   Expenses.name,
                   Categories.name AS category_name
                   FROM Expenses INNER JOIN Categories
                   ON  Expenses.categoryId = Categories.id
                   WHERE Expenses.categoryId = ?""",
                   (fetchedID,)
    )
    fetchedExpensesList = cursor.fetchall()

    #checking if there even expnses in the category
    if not fetchedExpensesList:
        print("There no expnses inside the category")
        return 
    
    else:
        for expense_id, amount, name, category_name in fetchedExpensesList:
            print(f"ID: {expense_id} | Name: {name} | Amount: {amount} | Category: {category_name}")

    #Commiting and closing the database
    connection.commit()
    connection.close()

#=========================================================================


#Gives list of all the categories
#=========================================================================

def getListOfAllCategories():

    #Connecting to the database
    connection = sqlite3.connect(databaseName)
    cursor  = connection.cursor()

    #Getting all the categories names and ids
    cursor.execute("""
                   SELECT
                   id , name FROM
                   Categories"""
    )
    fetchedCategories = cursor.fetchall()

    #printing all the categories if empty telling the user
    if not fetchedCategories:
        print("There no categories.")
    
    else:
        for category_id, name in fetchedCategories:
            print(f"ID: {category_id} | Name: {name}")

    #Commiting and closing the database
    connection.commit()
    connection.close()


#=========================================================================


#function that gives all expenses that are in the database of the user
#=========================================================================

def getListOfExpenses():
    
    #connecting into the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    #Getting all the expenses names, amount and id
    cursor.execute("""
                   SELECT
                   Expenses.id,
                   Expenses.name,
                   Expenses.amount,
                   Categories.name
                   FROM Expenses INNER JOIN Categories
                   ON Expenses.categoryId == Categories.id"""
    )
    fetchedExpenses = cursor.fetchall()

    #checking if expenses get any information inside if not tell the user
    if not fetchedExpenses:
        print("There no expenses.")

    else:
        for expenseID , expenseName , expenseAmount , expenseCategory in fetchedExpenses:
            print(f"Expense ID: {expenseID} | Name: {expenseName} | Amount: {expenseAmount} | Category: {expenseCategory}")
    
    #Commiting and closing the database
    connection.commit()
    connection.close()


#=========================================================================


#function that give the sum total of all expenses
#=========================================================================

def getSumTotalAllexpenses():

    #connecting into the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    #Getting all the amounts of the expenses 
    cursor.execute("""
                   SELECT
                   Expenses.amount
                   FROM Expenses"""
    )
    fetchedExpensesAmounts = cursor.fetchall()

    #checking if expenses get any information inside if not tell the user
    if not fetchedExpensesAmounts:
        print("There no expenses.")
        print("Total: 0")
    
    else:
        sum : int = 0
        #numbering the total
        for expenseAmount in fetchedExpensesAmounts:
            sum = sum + expenseAmount[0]
        
        print(f"Amount: {sum}")

    #Commiting and closing the database
    connection.commit()
    connection.close()


#=========================================================================


#Function that do the sum of all expenses inside a specific category
#=========================================================================

def getSumOfAllExpensesByCategory(categoryName: str):

    # connecting into the database
    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()

    #changing the format for the database format
    categoryName = modules.formatName(categoryName) 

    # getting the id of the category user typed
    cursor.execute("""
        SELECT id 
        FROM categories 
        WHERE name = ?
    """, (categoryName,))

    fetchedIdCategory = cursor.fetchone()

    # Checking if the id exists
    if fetchedIdCategory is None:
        print("Category doesn't exist.")
        return

    # Getting all expenses amounts for that category
    cursor.execute("""
                SELECT amount
                FROM Expenses
                WHERE categoryId = ?""", 
    (fetchedIdCategory[0],))
    fetchedExpensesAmounts = cursor.fetchall()

    # calculating total
    total = 0
    for (amount,) in fetchedExpensesAmounts:
        total += amount

    print(f"Amount: {total}")

    # closing connection
    connection.close()

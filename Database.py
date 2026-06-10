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
    with sqlite3.connect(databaseName) as connection:
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
    
#=========================================================================
    

#Function that creates a new category inside the database
#(By getting his name)
#=========================================================================

def addCategoryToDatabase(categoryName : str):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
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

#=========================================================================


#Function that creates a category for an expense that was entered without valid category
#(By giving its name)
#=========================================================================
def addCategoryToDatabaseForExpense(categoryName : str):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()
        
        #Inserting a new category row
        cursor.execute("""
        INSERT INTO Categories
            (name)
            VALUES(?)
            """,
            (categoryName,)
        )

        #Getting the new ID of the new category
        cursor.execute(
            "SELECT id FROM Categories WHERE name = ?",
            (categoryName,)
        )
        fetchedID : int = cursor.fetchone()[0]

        #returning the ID
        return fetchedID

#=========================================================================


#Function that adding expense into the database
#(By getting his name , amount and category he want it to be in)
#(and if user entered invalid category, creates one for him)
#=========================================================================
def addExpenseToDatabase(expenseName : str , amount : float , categoryName : str):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()

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

            #Creating a new category with the input of name category user gave and take its ID
            categoryFetchedID = addCategoryToDatabaseForExpense(categoryName)

            

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

#=========================================================================


#Function that giving a list of expenses that share the same category
#(By entering the name of the category)
#=========================================================================

def getListOfExpensesByCategory(categoryName : str):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()

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
            print("There no expenses inside the category")
            return 
        
        else:
            for expense_id, amount, name, category_name in fetchedExpensesList:
                print(f"ID: {expense_id} | Name: {name} | Amount: {amount} | Category: {category_name}")

#=========================================================================


#Function that gives list of all the categories
#=========================================================================

def getListOfAllCategories():

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()
        
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

#=========================================================================


#Function that gives all expenses that are in the database of the user
#=========================================================================

def getListOfExpenses():
    
    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
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
        
#=========================================================================


#Function that give the sum total of all expenses
#=========================================================================

def getSumTotalAllexpenses():

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
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

#=========================================================================


#Function that do the summary total of all expenses inside a specific category
#(By entering the name of the category)
#=========================================================================

def getSumOfAllExpensesByCategory(categoryName: str):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
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

#=========================================================================


#Function that deletes a category and the expenses inside of it
#by his name (there only be 1 category name)
#=========================================================================

def deleteCategory(categoryName : str):
    
    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()

        #changing the format for the database format
        categoryName = modules.formatName(categoryName) 

        #Before deleting the category, deleting all the expenses 
        cursor.execute("""
            SELECT id 
            FROM categories 
            WHERE name = ?
        """, 
        (categoryName,))

        fetchedIdCategory = cursor.fetchone()

        # Checking if the id exists
        if fetchedIdCategory is None:
            print("Category doesn't exist.")
            return
        
        #Deleting all the expenses inside the category
        cursor.execute("""
                    DELETE FROM Expenses WHERE categoryId = ?""",
                    (fetchedIdCategory[0],)
        )
        

        #deleting the category after deleting all the expenses
        cursor.execute("""
                    DELETE FROM Categories WHERE id = ?""",
                    (fetchedIdCategory[0],)
        )


#=========================================================================


#Function that Deletes the expense by id input
#=========================================================================

def deleteExpense(expenseID: int):

    #Connecting to the database and to the cursor 
    with sqlite3.connect(databaseName) as connection:
        cursor = connection.cursor()

        # Delete the expense with the given ID
        cursor.execute(
            "DELETE FROM Expenses WHERE id = ?",
            (expenseID,)
        )

        # Check if anything was deleted
        if cursor.rowcount == 0:
            print("Expense doesn't exist.")
        else:
            print("Expense deleted.")

#=========================================================================
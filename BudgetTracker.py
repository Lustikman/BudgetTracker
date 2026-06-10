#BudgetTracker.py: The main file that runs the program and the CLI.

#Importing Argparse for CLI
import argparse
#Importing the Database.py module
import Database as database


#setting the ArgumentParser & subparsers
parser = argparse.ArgumentParser(prog="BudgetTracker")
subparsers = parser.add_subparsers(dest="command")

#Creates Database
database.createDatabase()


#Add parser: Add new expenses & categories
#=========================================================================

#Creating a parser for add command
addParser = subparsers.add_parser("add", help="Add an expense/category",)
addSubparser = addParser.add_subparsers(dest="addType" , required=True)

#If the user picked category
#Creating the needed argument
addCategoriesParser = addSubparser.add_parser("category", help="Add a new category")
addCategoriesParser.add_argument("name", type=str, 
                            help="The name of the category")

##If the user picked expense
#Creating the needed arguments
addExpenseParser = addSubparser.add_parser("expense" , help="Add a new expense")
addExpenseParser.add_argument("name", type=str, 
                           help="The name of the expense")
addExpenseParser.add_argument("amount", type=float, 
                           help="The price amoutn of the expense")
addExpenseParser.add_argument("category", type=str, 
                           help="The category of the expense")


#=========================================================================


#List parser: See a list of all expense \ list of expenses inside a specific categories
#=========================================================================

#Creting a parser for the list command
listParser = subparsers.add_parser("list", help="Give a list of expenses/categories or both")
listSubparser = listParser.add_subparsers(dest="listType")

#if the user picked categories list
#Creating the needed arguments
listCategoriesParser = listSubparser.add_parser("category",
                                                help="Give list of categories or gives expenses of the category")
listCategoriesParser.add_argument("categoryName" , type=str,
                                  help="The category name for the list of it", nargs="?")

#if user picked expenses list
#Creating the needed arguments
listExpensesParser = listSubparser.add_parser("expenses" , help="Give list of expenses")

#=========================================================================


#Summary parser: Getting a sum total of amount money of expenses 
#=========================================================================

#Creating a parser for the summary
summaryParser = subparsers.add_parser("sum", help="Give a summary total of all the expenses in category or overall")

#if the user want a specific category
summaryParser.add_argument("sumCategory" , type=str,
                       nargs="?" , help="The category name")

#=========================================================================


#Delete parser: Delete an expenses\category by the name or id
#=========================================================================

#Creating a paerser
deleteParser = subparsers.add_parser("delete", help="Delete Expense/Category by his ID")
deleteSubparser = deleteParser.add_subparsers(dest="deleteType", required=True)

#if the user picked categories list
#Creating the needed arguments
deleteCategoryParser = deleteSubparser.add_parser("category", 
                                                help="Delete a category")
deleteCategoryParser.add_argument("category" , type=str,
                                  help="The name of the category")

#if the user picked categories list
#Creating the needed arguments
deleteExpenseParser = deleteSubparser.add_parser("expense", 
                                                help="Delete a expense")
deleteExpenseParser.add_argument("expense" , type=int,
                                  help="The name of the expense")

#=========================================================================

#Getting the command the user typed
#=========================================================================
args = parser.parse_args()
#DEBUG TO SEE THE COMMAND
#print(f"User input: {args}")
#=========================================================================


#Checking the input of the user
#=========================================================================

#If user picked "add"
if args.command == "add":

    #if user picked category
    if args.addType == "category":
        database.addCategoryToDatabase(args.name)
    #if user picked expense
    elif args.addType == "expense":
        database.addExpenseToDatabase(args.name , args.amount , args.category)
    #if user picked invalid input
    else:
        print("Invalid add type")

#If user picked "list"
elif args.command == "list":

    #if user picked category
    if args.listType == "category":
        
        #checking if user put category name for expenses 
        if args.categoryName:
            database.getListOfExpensesByCategory(args.categoryName)

        #if user only used category for list of categories
        else:
            database.getListOfAllCategories()

    #gives list of all expenses in the database   
    elif args.listType == "expenses":
        database.getListOfExpenses()

#if user picked "sum"
elif args.command == "sum":

    #Gives a sum total of all
    if not args.sumCategory:
        database.getSumTotalAllexpenses()

    #Gives the sum total of expenes of the same category
    else:
        database.getSumOfAllExpensesByCategory(args.sumCategory)

#if user picked "delete"
elif args.command == "delete":

    #if user want to delete a category
    if args.deleteType == "category":
        database.deleteCategory(args.category)
    
    #if user want to delete a expense
    elif args.deleteType == "expense":
        database.deleteExpense(args.expense)

elif args.command is None:
    parser.print_help()

#=========================================================================


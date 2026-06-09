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


#add: Add new expenses & category 
#=========================================================================

addParser = subparsers.add_parser("add", help="Add an expense/category",)
addSubparser = addParser.add_subparsers(dest="addType" , required=True)

#If the user picked category
addCategoriesParser = addSubparser.add_parser("category", help="Add a new category")
addCategoriesParser.add_argument("name", type=str, 
                            help="The name of the category")

##If the user picked expense
addExpenseParser = addSubparser.add_parser("expense" , help="Add a new expense")
addExpenseParser.add_argument("name", type=str, 
                           help="The name of the expense")
addExpenseParser.add_argument("amount", type=float, 
                           help="The price amoutn of the expense")
addExpenseParser.add_argument("category", type=str, 
                           help="The category of the expense")


#=========================================================================


#list: see the list of expenses\categories or both
#=========================================================================

listParser = subparsers.add_parser("list", help="Give a list of expenses/categories or both")
listSubparser = listParser.add_subparsers(dest="listType")

#if the user picked categories list
listCategoriesParser = listSubparser.add_parser("category", 
                                                help="Give list of categories or gives expenses of the category")
listCategoriesParser.add_argument("categoryName" , type=str,
                                  nargs="?" , help="The category name for the list of it")

#if user picked expenses list
listExpensesParser = listSubparser.add_parser("expense" , help="Give list of expenses")

#=========================================================================


#summary: see the total cost of all expenses or specific category total
#=========================================================================

sumParser = subparsers.add_parser("sum", help="Give a summary total of all the expenses in category or overall")

#if the user want a specific category
sumParser.add_argument("sumCategory" , type=str,
                       nargs="?" , help="The category name")

#=========================================================================

#delete: delete an expense by it's ID

#Parse the command that was sent by the user
#=========================================================================
args = parser.parse_args()
print(f"User input: {args}")
#=========================================================================


#Checking the decisions of the user command 
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
    elif args.listType == "expense":
        database.getListOfExpenses()

elif args.command == "sum":

    #if user wanted a specific category
    if not args.sumCategory:
        database.getSumTotalAllexpenses()

    else:
        database.getSumOfAllExpensesByCategory(args.sumCategory)










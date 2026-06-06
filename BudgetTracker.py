#Importing Argparse for CLI
import argparse

#setting the ArgumentParser & subparsers
parser = argparse.ArgumentParser(prog="BudgetTracker")
subparsers = parser.add_subparsers(dest="command")

#add: Add new expenses & category 
#=========================================================================

addParser = subparsers.add_parser("add", help="Add an expense/category",)

addSubparser = addParser.add_subparsers(dest="addType")

##If the user picked expense
expenseParser = addSubparser.add_parser("expense" , help="Add a new expense")
expenseParser.add_argument("name", type=str, 
                           help="The name of the expense")
expenseParser.add_argument("amount", type=float, 
                           help="The price amoutn of the expense")
expenseParser.add_argument("category", type=str, 
                           help="The category of the expense")

#If the user picked category
categoryParser = addSubparser.add_parser("category", help="Add a new category")
categoryParser.add_argument("name", type=str, 
                            help="The name of the category")

#=========================================================================




#list: see the list of expenses
#summary: see the total cost of all items
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
    if args.addType == "expense":
        print("Expense: Database set soon")

    elif args.addType == "category":
        print("Category: Database set soon")




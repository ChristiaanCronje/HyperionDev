import math

# The user chooses between an investment or a bond and then
# Calculations are made based on input given
print("investment - to calculate the amount of interest you'll earn on " 
      "your investment")
print("bond - to calculate the amount you'll have to pay on a home loan")
choice = input("Enter either 'investment' or 'bond' from the menu above "
               "to proceed: ")

# If investment was chosen, request the user for the respective inputs
# And ask to choose whether user wants simple or compound interest
# Work out the total amount of money for the option the user chose
# (Compound or interest)
# Print it out
# If bond was chosen, request the user for the respective inputs and
# Calculate the amount they have to repay each month
# Print it out
if choice.lower() == "investment":
    deposit_amount = int(input("Enter the amount of money you are " 
                               "depositing: "))
    interest_rate = int(input("Enter the interest rate you will be using: "))
    year_count = int(input("Enter the number of years " 
                           "you plan on investing: "))
    interest = input("Enter whether you want simple or compund interest: ")
    
    if interest == "simple":
        total_amount = deposit_amount*(1 + (interest_rate/100)*year_count)
        print("The total amount once the interest is aplied " 
              f"is {round(total_amount, 2)}")
    else:
        total_amount = deposit_amount*math.pow(
                           (1+interest_rate/100), year_count
                       )
        print("The total amount once the interest is aplied " 
              f"is {round(total_amount, 2)}")
elif choice.lower() == "bond":
    house_value = int(input("Enter the present value of your house: "))
    interest_rate = int(input("Enter the interest rate you will be using: "))
    month_count = int(input("Enter the amount of months you plan " 
                            "to replay the bond: "))

    repayment = (((interest_rate/100)/12)*house_value
    )/(
        1 - (1 + ((interest_rate/100))/12)**(-month_count)
    )
    print(f"The amount you have to repay each month is {round(repayment, 2)}")

print()
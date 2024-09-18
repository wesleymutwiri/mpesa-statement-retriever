import math


def compound_interest(rate, number_of_years,  principle):

    amount = principle * (1 + rate/100)**number_of_years
    print(amount)

def main():
    principle = float(input("Provide a starting amount: "))
    no_of_years = float(input("Provide number of years: "))
    rate = float(input("Provide a percentage rate: "))
    compound_interest(rate, no_of_years, principle)

if __name__ == '__main__':
    main()
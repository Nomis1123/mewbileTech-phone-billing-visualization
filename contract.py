"""
CSC148, Winter 2023
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call

# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class MTMContract(Contract):
    """ The subclass for contract

    === Public Attributes ===
    Month: the current month of th contract

    Year: the current year of the contract

    bill: the bill due at each month or at the end of the contract
    """

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("MTM", MTM_MINS_COST)

        self.bill.add_fixed_cost(MTM_MONTHLY_FEE)

    def bill_call(self, call: Call) -> None:
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))


class PrepaidContract(Contract):
    """ The subclass for contract

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    balance:
        The balance that the customer can access to make calls
    """
    balance: float

    def __init__(self, start, balance) -> None:
        self.balance = -1 * balance
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)

        if self.balance < 0:
            self.bill.add_fixed_cost(self.balance)
            self.balance = 0

        if self.bill.get_cost() > -10.0:
            self.bill.add_fixed_cost(-25.0)

    def bill_call(self, call: Call) -> None:
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        return Contract.cancel_contract(self)


class TermContract(Contract):
    """ The subclass for contract


    === Public Attributes ===
    end:
         end date for the contract
    deposit:
         deposit is the initial amount the customer has to give to start the
         contract
    """
    end: datetime.date
    deposit: float

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        Contract.__init__(self, start)
        self.end = end
        self.deposit = TERM_DEPOSIT

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)

        self.bill.add_fixed_cost(TERM_MONTHLY_FEE)

        if month == self.start.month and year == self.start.year:
            if self.deposit > 0:
                self.bill.add_fixed_cost(TERM_DEPOSIT)
                self.deposit *= -1

    def bill_call(self, call: Call) -> None:
        if self.bill.free_min + ceil(call.duration / 60.0) <= TERM_MINS:
            self.bill.add_free_minutes(ceil(call.duration / 60.0))

        elif self.bill.free_min == TERM_MINS:
            self.bill.add_billed_minutes(ceil(call.duration / 60.0))

        else:
            self.bill.add_billed_minutes((ceil(call.duration / 60.0))
                                         - TERM_MINS)
            self.bill.free_min = TERM_MINS

    def cancel_contract(self) -> float:
        now = datetime.datetime.now()
        if now > self.end:
            self.bill.add_fixed_cost(self.deposit)
        return Contract.cancel_contract(self)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })

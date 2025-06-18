import datetime
from contract import *


class PrepaidContract(Contract):
    balance: float

    def __init__(self, start, credit):
        self.balance = -1*credit
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("PREPAID", PREPAID_MINS_COST)

        if self.balance > -10.0:
            self.balance -= 25.0
            self.bill.add_fixed_cost(25.0)

    def bill_call(self, call: Call) -> None:
        self.balance += call.duration * PREPAID_MINS_COST

    def cancel_contract(self) -> float:
        if self.balance > 0:
            self.bill.add_fixed_cost(self.balance)
        return Contract.cancel_contract()

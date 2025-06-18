import datetime
from contract import *


class TermContract(Contract):
    end: datetime.date
    deposit: float

    def __init__(self, start, end):
        Contract.__init__(self, start)
        self.end = end
        self.deposit = TERM_DEPOSIT

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("TERM", TERM_MINS_COST)

        if self.deposit > 0:
            self.bill.add_fixed_cost(TERM_DEPOSIT)
            self.deposit *= -1


    def bill_call(self, call: Call) -> None:
        if self.bill.free_min + call.duration <= TERM_MINS:
            self.bill.add_free_minutes(call.duration)

        elif self.bill.free_min == TERM_MINS:
            self.bill.add_billed_minutes(call.duration)

        else:
            self.bill.add_billed_minutes((self.bill.free_min + call.duration) - TERM_MINS)
            self.bill.free_min = TERM_MINS

    def cancel_contract(self) -> float:
        now = datetime.datetime.now()
        if now > self.end:
            self.bill.add_fixed_cost(self.deposit)
        return Contract.cancel_contract()













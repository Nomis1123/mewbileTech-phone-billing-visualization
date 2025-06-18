import datetime
from contract import *


class MTMContract(Contract):

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        self.bill = bill
        self.bill.set_rates("MTM", MTM_MINS_COST)


    def bill_call(self, call: Call) -> None:
        self.bill.add_billed_minutes(call.duration)


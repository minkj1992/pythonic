import random
import string
from enum import Enum
from typing import List, Callable


def generate_id(length=8):
    # helper function for generating an id
    return ''.join(random.choices(string.ascii_uppercase, k=length))


class SupportTicket:

    def __init__(self, customer, issue):
        self.id = generate_id()
        self.customer = customer
        self.issue = issue


OrderingFn = Callable[[List[SupportTicket]], List[SupportTicket]]


# 열거형 멤버의 형은 그것이 속한 열거형
class OrderingStrategy(Enum):
    FIFO: OrderingFn = lambda arr: arr.copy()
    FILO: OrderingFn = lambda arr: [*reversed(arr.copy())]
    RANDOM: OrderingFn = lambda arr: sorted(arr, key=lambda k: random.random())
    BLACK_HOLE: OrderingFn = lambda arr: []


class CustomerSupport:

    def __init__(self):  # noqa
        self.tickets: List[SupportTicket] = []

    def create_ticket(self, customer, issue):
        self.tickets.append(SupportTicket(customer, issue))

    def process_tickets(self, ordering_fn: OrderingFn):
        # create the ordered list
        ticket_list = ordering_fn(self.tickets)

        # if it's empty, don't do anything
        if len(ticket_list) == 0:
            print("There are no tickets to process. Well done!")
            return

        # go through the tickets in the list
        for ticket in ticket_list:
            self.process_ticket(ticket)

    def process_ticket(self, ticket: SupportTicket):
        print("==================================")
        print(f"Processing ticket id: {ticket.id}")
        print(f"Customer: {ticket.customer}")
        print(f"Issue: {ticket.issue}")
        print("==================================")


if __name__ == '__main__':
    # create the application
    app = CustomerSupport()

    # register a few tickets
    app.create_ticket("John Smith", "My computer makes strange sounds!")
    app.create_ticket("Linus Sebastian", "I can't upload any videos, please help.")
    app.create_ticket("Arjan Egges", "VSCode doesn't automatically solve my bugs.")

    # process the tickets
    app.process_tickets(OrderingStrategy.BLACK_HOLE)  # type: ignore[arg-type]

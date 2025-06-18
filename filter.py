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
import time
import datetime
from call import Call
from customer import Customer


class Filter:
    """ A class for filtering customer data on some criterion. A filter is
    applied to a set of calls.

    This is an abstract class. Only subclasses should be instantiated.
    """

    def __init__(self) -> None:
        pass

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all calls from <data>, which match the filter
        specified in <filter_string>.

        The <filter_string> is provided by the user through the visual prompt,
        after selecting this filter.
        The <customers> is a list of all customers from the input dataset.

         If the filter has
        no effect or the <filter_string> is invalid then return the same calls
        from the <data> input.

        Note that the order of the output matters, and the output of a filter
        should have calls ordered in the same manner as they were given, except
        for calls which have been removed.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        - all calls included in <data> are valid calls from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """
    A class for resetting all previously applied filters, if any.
    """

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Reset all of the applied filters. Return a List containing all the
        calls corresponding to <customers>.
        The <data> and <filter_string> arguments for this type of filter are
        ignored.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        """
        filtered_calls = []
        for c in customers:
            customer_history = c.get_history()
            # only take outgoing calls, we don't want to include calls twice
            filtered_calls.extend(customer_history[0])
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Reset all of the filters applied so far, if any"


class CustomerFilter(Filter):
    """
    A class for selecting only the calls from a given customer.
    """

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data> made or
        received by the customer with the id specified in <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains a valid
        customer ID.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.

        Do not mutate any of the function arguments!
        """

        customer = None

        for cst in customers:
            x = cst.get_id()
            if str(x) == filter_string:
                customer = cst
                break

        if customer is None:
            return data
        else:
            filtered = []
            for call in data:
                for line in customer.get_phone_numbers():
                    if line in (call.src_number, call.dst_number):
                        filtered.append(call)
                        break
            return filtered

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """
    A class for selecting only the calls lasting either over or under a
    specified duration.
    """

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data> with a duration
        of under or over the time indicated in the <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains the following
        input format: either "Lxxx" or "Gxxx", indicating to filter calls less
        than xxx or greater than xxx seconds, respectively.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.

        Do not mutate any of the function arguments!
        """

        if 2 <= len(filter_string) <= 4 and \
                filter_string[1:].rstrip().isdigit():
            total = int(filter_string[1:].rstrip())
            times = []

            if filter_string[0] == "G":
                for call in data:
                    if call.duration > total:
                        times.append(call)

            else:
                for call in data:
                    if call.duration < total:
                        times.append(call)

            return times
        return data

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls based on duration; " \
               "L### returns calls less than specified length, G### for greater"


class LocationFilter(Filter):
    """
    A class for selecting only the calls that took place within a specific area
    """

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data>, which took
        place within a location specified by the <filter_string>
        (at least the source or the destination of the event was
        in the range of coordinates from the <filter_string>).

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains four valid
        coordinates within the map boundaries.
        These coordinates represent the location of the lower left corner
        and the upper right corner of the search location rectangle,
        as 2 pairs of longitude/latitude coordinates, each separated by
        a comma and a space:
          lowerlong, lowerlat, upperlong, upperlat
        Calls that fall exactly on the boundary of this rectangle are
        considered a match as well.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.


        Do not mutate any of the function arguments!
        """

        lowerlong = None
        lowerlat = None
        upperlong = None
        upperlat = None

        try:
            point1 = filter_string.find(", ")
            if point1 > 0:
                lowerlong = float(filter_string[0:point1])

                filter_string = filter_string[point1 + 2:]
                point2 = filter_string.find(", ")
                lowerlat = float(filter_string[0:point2])

                filter_string = filter_string[point2 + 2:]
                point3 = filter_string.find(", ")
                upperlong = float(filter_string[0:point3])

                filter_string = filter_string[point3 + 2:].rstrip()
                upperlat = float(filter_string)
                point = self.findpoints(lowerlong, lowerlat, upperlong,
                                        upperlat, data)

                return point
            else:
                return data
        except (TypeError, ValueError):
            return data

    def findpoints(self, lowerlong: float, lowerlat: float, upperlong: float,
                    upperlat: float, data: list[Call]) -> []:
        """
        function to find the points for the map
        """

        point = []
        if (-79.697878 <= lowerlong <= -79.196382) and (
                -79.697878 <= upperlong <= -79.196382) and (
                43.576959 <= lowerlat <= 43.799568) and (
                43.576959 <= upperlat <= 43.799568):
            for call in data:
                if ((lowerlong <= call.src_loc[0] <= upperlong) and (
                        lowerlat <= call.src_loc[1] <= upperlat)) \
                        or ((lowerlong <= call.dst_loc[0] <= upperlong)
                            and (lowerlat <= call.dst_loc[1]
                                 <= upperlat)):
                    point.append(call)

        return point

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls made or received in a given rectangular area. " \
               "Format: \"lowerlong, lowerlat, " \
               "upperlong, upperlat\" (e.g., -79.6, 43.6, -79.3, 43.7)"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'time', 'datetime', 'call', 'customer'
        ],
        'max-nested-blocks': 4,
        'allowed-io': ['apply', '__str__'],
        'disable': ['W0611', 'W0703'],
        'generated-members': 'pygame.*'
    })

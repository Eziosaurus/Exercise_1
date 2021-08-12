# Name: Edo Martinelli
# Section Leader: Abby Collier
# Date: 01/28/2021
# Assignment: ISTA 350 Hw1
# Summary: This program uses regular expression, linar search, and binary search
# to find counterfeit dollar bills.
# Collaboration: Got help from Rich.

import re

class WatchList:
    # Summary: Class WatchList will check if bills are in the counterfeit watchlist.
    def __init__(self, fname = ''):
        # Summary: This magic method holds three instance variables. That maps
        # the denominations and serial numbers of dollar bills into a dictionary, sorts it, 
        # and checks the bills for valid serial numbers.
        # Parameters: fname: A filename that holds serial numbers and denominations of
        # dollar bills. Default empty string.
        self.bills = {'5': [], '10': [], '20': [], '50': [], '100': []}
        self.is_sorted = True
        
        if fname:
            text = open(fname)
            for line in text:
                sn, dnom = line.split()
                self.bills[dnom].append(sn)

            self.is_sorted = False

        self.validator = re.compile('^[A-M][A-L](?!0{8})\d{8}[A-NP-Y]$')
    
    def insert(self, bill_str):
        # Summary: This method function checks if bill_str is in the bills dictionary and 
        # if it's sorted. Append if string not in dictionary and not sorted. Insert string if
        # dictionary is sorted.
        # Parameters: bill_str: A string that will be inserted in bills dictionary.
        sn, dnom = bill_str.split()

        if sn not in self.bills[dnom] and self.is_sorted == True:
            for i in range(len(self.bills[dnom])):
                if self.bills[dnom][i] > sn:
                    self.bills[dnom].insert(i, sn)
                    break
        
        if sn not in self.bills[dnom]:
            self.bills[dnom].append(sn)
    
    def sort_bills(self):
        # Summary: This method function sorts the list in the bills dictionary.
        for key in self.bills:
            self.bills[key] = sorted(self.bills[key])
        self.is_sorted = True
    
    def linear_search(self, bill_str):
        # Summary: This method function takes a string does a linear search on bills dictionary 
        # and returns true if string is dictionary. Returns false otherwise. Used if dictionary 
        # is not sorted.
        # Parameters: bill_str: A string that will be used in a linear search to 
        # check if string is in bills dictionary.
        # Returns: A boolean: True is string is in dictionary. False otherwise.
        sn, dnom = bill_str.split()
        return sn in self.bills[dnom]
        
    def binary_search(self, bill_str):
        # Summary: This method function takes a string does a binary search on bills dictionary 
        # and returns true if string is dictionary. Returns false otherwise. Used if dictionary 
        # is sorted.
        # Parameters: bill_str: A string that will be used in a binary search to 
        # check if string is in bills dictionary.
        # Returns: A boolean: True is string is in dictionary. False otherwise.
        sn, dnom = bill_str.split()
        bills = self.bills[dnom]
        n = len(bills)

        left = 0
        right = n - 1

        while left <= right:
            mid = (left + right) // 2
            if sn == bills[mid]:
                return True
            elif sn < bills[mid]:
                right = mid - 1
            else:
                left = mid + 1
        
        return False

    def check_bills(self, fname, boo = False):
        # Summary: This method function takes a file containing a list of dollar bill information,
        # checks it by using either a linear or binary search, and create/return a list of 
        # counterfeit bills.
        # Parameters: fname: A filename that holds serial numbers and denominations of
        # dollar bills.
        # boo: A boolean that has a default of False. If True, this function will use a binary search.
        # If False, this function will use a linear search.
        # Returns: fake_bills: A list of appended counterfeit bills.
        if boo and not self.is_sorted:
            self.sort_bills()
        
        fake_bills = []
        
        if self.is_sorted:
            search = self.binary_search
        else:
            search = self.linear_search
        
        for line in open(fname):
            bills = line.strip()
            serial_number = bills.split()[0]

            if search(bills) or not self.validator.match(serial_number):
                fake_bills.append(bills)
        
        return fake_bills
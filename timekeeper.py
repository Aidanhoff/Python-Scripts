import os
import datetime as dt

x = input('Enter a command:')
while x <> 'quit':
    if x = 'new':
        '''function to create new record'''
    elif x = 'view':
        '''function to view existing records'''
    elif x = 'edit':
        '''function to edit record'''
    elif x = 'export':
        '''function to export to a tbd format'''
    elif x = 'help':
        '''function to print list of commands'''
    else:
        print('Sorry, command not recognized. \n Please use \'help\' command.')
    
records = {}

def strip_hr_min(time):
    return dt.strptime(time, %H:%M)
    
class new_record:
    def __init__(self):
        self.date = dt.date.today()
        self.start = strip_hr_min(input('Start time:'))
        self.end = strip_hr_min(input('End time:'))
        self.lunch = strip_hr_min(input('Break time:'))
        self.partner = input('Partner:')
        self.superv = input('Supervisor:')
        self.loc = input('Location:')

        records = dict(
            start=start, end=end, lunch=lunch, partner=partner, superv=superv,      
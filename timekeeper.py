import datetime as dt

x = input('Enter a command:')
while not x == 'quit':
    if x == 'new':
        '''create new record class instance'''
    elif x == 'view':
        '''call class print function'''
    elif x == 'edit':
        '''edit class attributes'''
    elif x == 'export':
        '''call class export function'''
    elif x == 'help':
        '''call help function'''
    else:
        print('Sorry, command not recognized. \n Please use \'help\' command.')
    
records = {}

#def strip_hr_min(time):
    #return dt.strptime(time, %H:%M)

class record:
    def __init__(self, date, start, end, lunch, partner, superv, loc):
        self.date = dt.date.today()
        self.start = strip_hr_min(input('Start time:'))
        self.end = strip_hr_min(input('End time:'))
        self.lunch = strip_hr_min(input('Break time:'))
        self.partner = input('Partner:')
        self.superv = input('Supervisor:')
        self.loc = input('Location:')
        
        new_rec = dict(date=self.date, start=self.start, end=self.end, lunch=self.lunch, partner=self.partner, superv=self.superv, loc=self.loc)
    def view(self, x):
        if x == 'view':
            print (new_rec)


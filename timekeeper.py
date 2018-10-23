import datetime as dt
import time as t

cmd = input('Enter a command:')
while not cmd == 'quit':
    if cmd == 'new':
        new_rec = record(date, start, end, lunch, partner, superv, loc)
    elif cmd == 'view':
        #scroll through previously created records
    elif cmd == 'edit':
        #edit class attributes
    elif cmd == 'export':
        #call class export function
    elif cmd == 'help':
        print('Available Commands: \n
                \'quit\': Exit the API
                \'new\': Start a new record input
                \'view\': View existing records, starting with the last input. \n
                Navigate further back with d, and forward with a. \n 
                Edit the current entry with \'edit\' \n
                Quit to the previous menu with \'quit'\!
                \'export\': Exports data to .csv file in Documents/'TimekeeperExport')
    else:
        print('Sorry, command not recognized. \n Please use \'help\' command.')
    
records = {}

#def strip_hr_min(time):
    #return dt.strptime(time, %H:%M)

class record:
    def __init__(self, date, start, end, lunch, partner, superv, loc):
        self.date = dt.date.today()
        #need function strip_hr_min
        self.start = strip_hr_min(input('Start time:'))
        self.end = strip_hr_min(input('End time:'))
        self.lunch = strip_hr_min(input('Break time:'))
        self.partner = input('Partner:')
        self.superv = input('Supervisor:')
        self.loc = input('Location:')
        
        new_rec = dict(date=self.date, start=self.start, end=self.end, lunch=self.lunch, partner=self.partner, superv=self.superv, loc=self.loc)
    def view(self, x):
        print(new_rec[-1])
        view_cmd = input('Enter')
    def strip_hr_min(self, x):
        return t.strptime(x[, %H:%M]))
    def export(self):
        #export to .csv using numpy or pandas
    
    
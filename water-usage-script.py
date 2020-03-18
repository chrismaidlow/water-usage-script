#######################################################################
# Computer Project #6
# 
# Algorithm
#
#   Prompt for file until opened. Read file creating list of tuples containing
#   pertinant data points. Extract data for state entered when prompted. 
#   Calculate usage values for counties and display values and plot. 
#
########################################################################

import pylab

STATES = {'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'}
USERS = ["Public", "Domestic", "Industrial", "Irrigation","Livestock"]

def open_file():
    ''' Prompts user for filename loops until proper input '''
    
    #Error checking for file entered
    
    while True:
    
        try:
            filename = input("Input a file name: ")
            fp = open(filename)
            return fp
            
        except FileNotFoundError: 
            print("Unable to open file. Please try again.")
    
def read_file(fp):
    '''
        Iterate through file picking out data point for each line and
        composing tuple of data points before appending to list
    
    '''
    #Remove first line in file and initiate list
  
    forget = fp.readline()
    data_list = []
    
    #Iterate through file 
    
    for line in fp:
        
        item = line.split(",")
        
        #Important data points allocated to variable names
     
        state = item[0]
        county = item[2]
        population = (float(item[6]) * 1000)
        fresh_water = float(item[114])
        salt_water = float(item[115])
        public = float(item[18])
        domestic = float(item[26])
        industrial = float(item[35])
        livestock = float(item[59])
        
        #Error checking helps with inconsistent irrigation values
        
        try:
            
            irrigation = float(item[45])
            
        except ValueError:
            
            irrigation = 0

        #Tuple created for each line of data points
        
        tup = (state,county,population, fresh_water, salt_water, public,
               domestic, industrial, irrigation, livestock)
    
        #Tuple then appended to list
    
        data_list.append(tup)
        
    return data_list

def compute_usage(state_list):
    ''' Computes total water and per person usage. Returns list '''
    
    usage_list = []
    
    #Iterates through state list picking out values from each tuple
    
    for item in state_list:
        
        county = item[1]
        
        salt = item[4]
        
        fresh = item[3]
        
        population = item[2]
        
        #Calculate total water
        
        total_water = salt + fresh
        
        #Calculate per person usage
        
        per_person_water = (fresh)/(population)
        
        #Form tuple of four values
        
        tup = (county,population, total_water,per_person_water)
        
        #Append tuple to list
        
        usage_list.append(tup)
        
    return usage_list
        
def extract_data(data_list, state):
    ''' If state in list. Append data to state_list'''
    
    state_list = []
    
    #If prompt entered by user (state) is in a tuple inside data_list
    #appends that item to state_list
    
    for item in data_list:
    
        if state in item:
            
            state_list.append(item)
    
    return state_list
           
def display_data(state_list, state):
    ''' displays data for state_list '''
    
    #Calls the computer_usage function for the list of counties (state_list)

    usage_list = compute_usage(state_list)
    
    print()
    
    #Print title

    title = "Water Usage in " + state + " for 2010"
    
    #Display formatting for title and header
    
    print("{:^88s}".format(title))
    header = "{:<23s}{:>22s}{:>23s}{:>22s}".format("County", \
    "Population", "Total (Mgal/day)", " Per Person (Mgal/person)")
    print(header)
    
    #Prints each item in usage_list with correct formatting
    
    for item in usage_list:
        
        print("{:<23s}{:>22,.0f}{:>23.2f}{:>23.4f}".format(item[0],item[1],item[2],item[3]))
        
def plot_water_usage(some_list, plt_title):
    
    '''
        Creates a list "y" containing the water usage in Mgal/d of all counties.
        Y should have a length of 5. The list "y" is used to create a pie chart
        displaying the water distribution of the five groups.

        This function is provided by the project.
    '''

    # accumulate public, domestic, industrial, irrigation, and livestock data
    y =[ 0,0,0,0,0 ]

    for item in some_list:

        y[0] += item[5]
        y[1] += item[6]
        y[2] += item[7]
        y[3] += float(item[8])
        y[4] += item[9]

    total = sum(y)
    y = [round(x/total * 100,2) for x in y] # computes the percentages.

    color_list = ['b','g','r','c','m']
    pylab.title(plt_title)
    pylab.pie(y,labels=USERS,colors=color_list)
    pylab.show()
    #pylab.savefig("plot.png")  # uncomment to save plot to a file
    
def main():
    '''Calls other functions. Handles entry for state prompt '''

    print("Water Usage Data from the US and its States and Territories.\n")
   
    fp = open_file()
    
    data_list = read_file(fp)
    
    #Input state code
    
    state = input("\nEnter state code or 'all' or 'quit': ")
    
    state = state.upper()
    
    #While state code is not Quit keep looping
    
    while state != "QUIT":
    
        #If tree for correct state code and plotting
        
        if state in STATES:
            
            state_list = extract_data(data_list, state)
    
            display_data(state_list, state)
    
            answer = input("\nDo you want to plot? ")
    
            answer = answer.upper()
    
            plt_title = ("Water Usage In " + state + " for 2010 (Mgal/day)")
    
            if answer == "YES":
    
                plot_water_usage(state_list,plt_title)
                
            state = input("\nEnter state code or 'all' or 'quit': ")
            
            state = state.upper()
            
            continue
        
        #If tree for the entry equaling all
            
        if state == "ALL":
            
            display_data(data_list, "ALL")
            
            answer = input("\nDo you want to plot? ")
    
            answer = answer.upper()
    
            plt_title = ("Water Usage In " + "All" + " for 2010 (Mgal/day)")
    
            if answer == "YES":
    
                plot_water_usage(data_list,plt_title)
                
            state = input("\nEnter state code or 'all' or 'quit': ")
            
            state = state.upper()
            
            continue
        
        #If entry is not a valid entry
            
        else:

            print("Error in state code.  Please try again.")
            state = input("\nEnter state code or 'all' or 'quit': ")
            
            state = state.upper()
            
            continue
 
    
if __name__ == "__main__":
    
    main()
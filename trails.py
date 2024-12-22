 user_id=res[0]  # as user can only add an expense after logging in
    family_id=res[1] # The family id will be associated with the user_id
    
    ############### INPUT SECTION ################
    
    ## as the category must be selected form the drop down in the final stage
    print("1.Rent \n 2. Travel \n 3.investment \n 4.grociries \n 5.food \n 6.Movies \n 7.stationery \n 8.gifts \n 9.bills \n 10.health \n 11.medical \n 12.emi \n choose the type of your expense:")
    category_id=int(input())  #in the later stages this will be mapped when selected
    
# {    
    #### taking the date input    
    date_=input("YYYY-MM-DD:")
    
    if not date_: ### if the user leaves an empty space for the date input  ###### this is just for our convenience ### helps testing the code  
        
        date_in=datetime.now().date()  ### we are going to utilixe this in frontend where we can put the default value as current date
    
    else:
        
        date_in=datetime.strptime(date_,"%Y-%m-%d").date() ### extracting the date format form the string input
        curr_date=datetime.now().date()
        
        while date_in>curr_date:   ## comparing the date input with the current date to check if the user enters a date in future
            print("Invalid date. Please Try Again:")
            date_=input("YYYY-MM-DD:")
            date_in=datetime.strptime(date_,"%Y-%m-%d").date()
            
    print(date_in)

# } #amount spent
    amount=float(input("Enter the amount:"))
    
    #description 
    desc=input("describe your expense(optional):")
    if not desc:
        #### since description is optional included this just to check if the category name can be fetched and used 
        cursor.execute("SELECT name FROM categories WHERE category_id=%s",(category_id,))
        res=cursor.fetchone()
        description="used on "+res[0] 
        
        #description="null"
    else:
        description=desc
    
    ### end of input section
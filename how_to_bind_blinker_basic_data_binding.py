from blinker import signal



# Assume This is a method that contains sending Info to client from an API
def send_email_to_client(invoice):
	print("sending email to client", invoice)


# we create a signal object called send_data  that handles signal event.
send_data  = signal('send-data') # signal object created of send-data


# this decorator works at runtime to when send method is called.
@send_data.connect
def receive_data(sender,**data):
	print("inside receive data method")
	sender(data);
	#print("sender is a object:",sender) # print the type
	

generated_invoice ={
        "1": {"Company":"MTN"},
        "2": {"EmployeeIDs":[1,2,3,4,5,6]},
        "3": {"NumberOfHours":[1,2,3,4]},
        "4": {"UnitPrice":10},
        "5": {"Cost":90},
        "6": {"Total": 20000}
    }
    
# we call send method  belonging to the signal class that will accept the sendEmailToClient function as an object.
result = send_data.send(send_email_to_client,data=generated_invoice) # this will print out sendEmailToClient has an object. 


from blinker import signal



# Assume This is a method that contains sending Info to client
def sendEmailToClient():
	return "i am inside sendEmailToClient method"


# we create a signal object called send_data  that handles signal event.
send_data  = signal('send-data') # signal object created of send-data


# this decorator works at runtime to when send method is called.
@send_data.connect
def receive_data(sender):
	print("sender is a object:",sender) # print the type
	print('received:' , sender() , ' ', 'from receive_data method')


# we call send method  belonging to the signal class that will accept the sendEmailToClient function as an object.
result = send_data.send(sendEmailToClient) # this will print out sendEmailToClient has an object. 


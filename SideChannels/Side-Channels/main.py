import errorMsg, timingAttack

'''
This file as well as errorMSG and timingAttack need to be stored with the folders for the different
challenges - in the Side-Channels folder inside of the SideChannels folder 
'''

# Select the challenge, this will pass this option to the appropriate file containing the code to
# exploit that type of side-channel
while True:
    option = " "
    while option not in "12345":
        print("1: 4 Digit Pin error message\n2: Pin error message\n3: Password error message\n4: Password timing")
        print("5: Rsa timing")
        option = input()
    if option == "1" or option == "2" or option == "3":
        errorMsg.run(option)
    elif option == "4":
        timingAttack.password_timing()
    elif option == "5":
        timingAttack.rsa_timing_false()
    else:
        problem = "oh no"



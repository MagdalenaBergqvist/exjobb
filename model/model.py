import sys
import math
import time

gravity = 0.001
fuel_out_at = 0
mass = 32500 # Total weight (LBS)
velocity_calc = 1


#Function used for game loop
def model():
    global fuel_out_at

    #Functionality exicuted once at the start of every game
    game_state = inital_state()
    print_instructions()
    print_values(game_state)

    #Loop used for one game instance
    while(True):

        #Ask user for fuel input
        ans = input("K:")

        if(check_input(ans)):

            #Calculate new variables
            rate = int(ans)
            fuel_update(game_state, rate)
            velocity_altitude_update(game_state, rate)

            #End game if the fuel is out
            if(game_state["fuel"] <= 0):
                fuel_out_at = game_state["time"]
                free_falling(game_state)
                print_ending(game_state)
                return

            #End game if spacecraft already on the moon
            elif(game_state["altitude"] <= 0):
                fuel_out_at = False
                print_ending(game_state)
                return

            #Print gamestate
            print_values(game_state)

        #Print error msg if input is incorrect
        else:
            print_error()

#Function used to set the initial gamestate
def inital_state():
    global velocity_calc
    velocity_calc = 1
    return {"time": 0, "altitude": 120, "velocity": 3600, "fuel": 16000}

#Function used to verify that the input is correct
def check_input(input):
    if(input.isnumeric()):
        if((int(input) > 7 and int(input) <= 200) or int(input) == 0 ):
            return True
    return False

######### FUNCTIONS USED FOR CALCULATIONS ########
#Function used to update the time for each iteration
def time_update(game_state):
    new_time = game_state["time"] + 10
    game_state["time"] = new_time

#Function used to update the fuel level for each iteration
def fuel_update(game_state, rate):
    for x in range(10):
        new_fuel = game_state["fuel"] - (rate)
        if(new_fuel > 0):
            game_state["fuel"] = new_fuel
            game_state["time"] = game_state["time"] + 1
        else:
            game_state["fuel"] = 0
            game_state["time"] = game_state["time"] + 1
            break

#Function used to update the velocity and altitude for each iteration
def velocity_altitude_update(game_state, rate):
    global velocity_calc
    tmp = 10 * rate / mass

    #Calculate new altitude
    altitude_calc = game_state["altitude"] - (gravity * 50) - velocity_calc * 10 + (18 * ((tmp / 2) + (pow(tmp, 2) / 6 )+ (pow(tmp, 3) / 12) + (pow(tmp, 4) / 20) + (pow(tmp, 5) / 30)))

    #New velocity based on Tsiolkovsky rocket equation.
    #Taylor series of ln(1-Q) is used.
    velocity_calc = velocity_calc + (gravity * 10) +( 1.8 * (-tmp -((pow(tmp, 2)) / 2) - ((pow(tmp,3)) / 3) - ((pow(tmp, 4)) / 4) - ((pow(tmp, 5)) / 5)))

    game_state["altitude"] = altitude_calc
    game_state["velocity"] = 3600 * velocity_calc

#Function used to calculate velocity and time of impact when fuel runs out
def free_falling(game_state):
    global velocity_calc
    #velocity_calc = game_state["velocity"] #Only for testing
    tmp = (math.sqrt(velocity_calc * velocity_calc + 2 * game_state["altitude"] * gravity) - velocity_calc) / gravity
    velocity_calc = velocity_calc + tmp * gravity
    game_state["velocity"] = 3600 * velocity_calc
    game_state["time"] = game_state["time"] + tmp

######### END OF CALCULATIONS ########

######### PRINT FUNCTIONS ##########
#Function used to print game instructions at the begining of the game
def print_instructions():
    print("")
    print("CONTROL CALLING LUNAR MODULE. MANUAL CONTROL IS NECESSARY")
    print("YOU MAY RESET FUEL RATE K EACH 10 SECS TO 0 OR ANY VALUE")
    print("BETWEEN 8 & 200 LBS/SEC. YOU'VE 16000 LBS FUEL. ESTIMATED")
    print("FREE FALL IMPACT TIME-120 SECS. CAPSULE WEIGHT-32500 LBS")
    print("FIRST RADAR CHECK COMING UP")
    print("")
    print("")
    print("COMMENCE LANDING PROCEDURE")
    print("TIME,SECS   ALTITUDE,   VELOCITY,MPH   FUEL,LBS   FUEL RATE")

#Function used to print gamestate
def print_values(game_state):
    small_gap = "       "
    large_gap = "           "
    string = small_gap + str(round(game_state["time"])) + small_gap + str(round(game_state["altitude"])) + large_gap + str(round(game_state["velocity"])) + small_gap + str(game_state["fuel"]) + small_gap
    print(string, end="")

#Function used to print error msg
def print_error():
    string = "NOT POSSIBLE.........................................."
    print(string, end="")

#Function used to print the gamestate at the end of a game
def print_ending(game_state):
    gap = "       "
    if(fuel_out_at):
        print("FUEL OUT AT" + gap + str(fuel_out_at)+" SECS")
    print("ON THE MOON AT" + gap + str(round(game_state["time"])) + " SECS")
    print("IMPACT VELOCITY OF" + gap + str(round(game_state["velocity"])) + " M.P.H.")
    print("FUEL LEFT:" + gap + str(game_state["fuel"]) + " LBS")
    print_result(game_state)

#Function used to print the result of the game
def print_result(game_state):
    if (game_state["velocity"] < 1):
        print("PERFECT LANDING !-(LUCKY)")
    elif(game_state["velocity"] < 10):
        print("GOOD LANDING-(COULD BE BETTER)")
    elif(game_state["velocity"] < 22):
        print("CONGRATULATIONS ON A POOR LANDING")
    elif(game_state["velocity"] < 40):
        print("CRAFT DAMAGE. GOOD LUCK")
    elif(game_state["velocity"] < 60):
        print("CRASH LANDING-YOU'VE 5 HRS OXYGEN")
    else:
        print("SORRY,BUT THERE WERE NO SURVIVORS-YOU BLEW IT!")
        deep = round(game_state["velocity"] * 0.277777, 2)
        print("IN FACT YOU BLASTED A NEW LUNAR CRATER " + str(deep) + " FT. DEEP")
    print("")
    print("")
    print("")

######### END OF PRINT FUNCTIONS ##########

#Main loop, starts new game
if __name__ == "__main__":
    while(True):
        model()
        while(True):
            print("TRY AGAIN?")
            ans = input("(ANS. YES OR NO):")
            if(ans == "No" or ans == "NO"):
                quit()
            elif(ans == "Yes" or ans == "YES"):
                break

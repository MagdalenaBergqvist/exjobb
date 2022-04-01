import sys
import math
import time

gravity = 0.001
fuel_out_at = 0
mass = 32500 # Total weight (LBS)
speed_calc = 1
#Function used for game loop
def model():
    game_state = inital_state()
    print_instructions()
    print_values(game_state)
    while(True):
        ans = input("")
        if(check_input(ans)):
            rate = int(ans)
            fuel_update(game_state, rate)
            speed_altitude_update(game_state, rate)
            if(game_state["fuel"] <= 0):
                global fuel_out_at
                fuel_out_at = game_state["time"]
                free_falling(game_state)
                print_ending(game_state)
                return
            print_values(game_state)
        else:
            print_error()

#Function used to print game state
def print_values(game_state):
    gap = "       "
    string = gap + str(game_state["time"]) + gap + str(game_state["alt"]) + gap + str(game_state["miles"]) + gap + str(game_state["speed"]) + gap + str(game_state["fuel"]) + gap + "K=:"
    print(string, end="\n")

def print_error():
    string = "NOT POSSIBLE...................................................K=:"
    print(string, end="\n")

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
    print("TIME,SECS   ALTITUDE,MILES+FEET   VELOCITY,MPH   FUEL,LBS   FUEL RATE")

def print_ending(game_state):
    gap = "       "
    print("FUEL OUT AT" + gap + str(fuel_out_at)+" SECS")
    print("ON THE MOON AT" + gap + str(game_state["time"]) + " SECS")
    print("IMPACT VELOCITY OF" + gap + str(game_state["speed"]) + " M.P.H.")
    print("FUEL LEFT:" + gap + str(game_state["fuel"]) + " LBS")
    print_result(game_state)

def print_result(game_state):
    if (game_state["speed"] < 1):
        print("PERFECT LANDING !-(LUCKY)")
    elif(game_state["speed"] < 10):
        print("GOOD LANDING-(COULD BE BETTER)")
    elif(game_state["speed"] < 22):
        print("CONGRATULATIONS ON A POOR LANDING")
    elif(game_state["speed"] < 40):
        print("CRAFT DAMAGE. GOOD LUCK")
    elif(game_state["speed"] < 60):
        print("CRASH LANDING-YOU'VE 5 HRS OXYGEN")
    else:
        print("SORRY,BUT THERE WERE NO SURVIVORS-YOU BLEW IT!")
        deep = round(game_state["speed"] * 0.277777, 2)
        print("IN FACT YOU BLASTED A NEW LUNAR CRATER " + str(deep) + " FT. DEEP")
    print("")
    print("")
    print("")

#Set the initial gamestate
def inital_state():
    return {"time": 0, "alt": 120, "miles": 0, "speed": 3600.0, "fuel": 16000.0}

#Update the time for each iteration
def time_update(game_state):
    new_time = game_state["time"] + 10
    game_state["time"] = new_time

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

def check_input(input):
    if(input.isnumeric()):
        if((int(input) > 7 and int(input) <= 200) or int(input) == 0 ):
            return True
    return False

def free_falling(game_state):
    global speed_calc
    tmp = (math.sqrt(speed_calc * speed_calc + 2 * game_state["alt"] * gravity) - speed_calc) / gravity
    speed_calc = speed_calc * tmp * gravity
    game_state["speed"] = round(3600 * speed_calc)
    game_state["time"] = round(game_state["time"] + tmp)


def speed_altitude_update(game_state, rate):
    global speed_calc
    tmp = 10 * rate / mass
    alt_calc = game_state["alt"] - ((gravity * 10) * (10 / 2)) - speed_calc * 10 + (1.8 * 10 * ((tmp / 2) + (pow(tmp, 2) / 6 )+ (pow(tmp, 3) / 12) + (pow(tmp, 4) / 20) + (pow(tmp, 5) / 30)))
    speed_calc = speed_calc + (gravity * 10) +( 1.8 * (-tmp -((pow(tmp, 2)) / 2) - ((pow(tmp,3)) / 3) - ((pow(tmp, 4)) / 4) - ((pow(tmp, 5)) / 5)))

    game_state["alt"] = round(alt_calc)
    game_state["speed"] = round(3600 * speed_calc)


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

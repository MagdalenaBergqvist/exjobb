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

#Set the initial gamestate
def inital_state():
    return {"time": 0, "alt": 120, "miles": 0, "speed": 3600.0, "fuel": 16000.0}

#Update the time for each iteration
def time_update(game_state):
    new_time = game_state["time"] + 10
    game_state["time"] = new_time

def fuel_update(game_state, rate):
    new_fuel = game_state["fuel"] - (rate * 10)
    game_state["fuel"] = new_fuel

def check_input(input):
    if(input.isnumeric()):
        if((int(input) > 7 and int(input) < 200) or int(input) == 0 ):
            return True

if __name__ == "__main__":
    model(sys.argv[1:])

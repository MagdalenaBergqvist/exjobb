import sys

#Function used for game loop
def model(args):
    game_state = inital_state()
    print_instructions()
    print_values(game_state)

    for input in args:
        rate = int(input)
        time_update(game_state)
        fuel_update(game_state, rate)
        print_values(game_state)

#Function used to print game state
def print_values(game_state):
    gap = "       "
    string = gap + str(game_state["time"]) + gap + str(game_state["alt"]) + gap + str(game_state["miles"]) + gap + str(game_state["speed"]) + gap + str(game_state["fuel"]) + gap + "K=:"
    print(string, end="")

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

#Set the initial gamestate
def inital_state():
    return {"time": 0, "alt": 120, "miles": 0, "speed": 3600, "fuel": 16000}

#Update the time for each iteration
def time_update(game_state):
    new_time = game_state["time"] + 10
    game_state["time"] = new_time

def fuel_update(game_state, rate):
    print(rate)
    new_fuel = game_state["fuel"] - (rate * 10)
    game_state["fuel"] = new_fuel

if __name__ == "__main__":
    model(sys.argv[1:])

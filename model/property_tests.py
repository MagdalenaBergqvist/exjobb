from model import *
import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers, text, dictionaries

#Test that text input is always incorrect
@given(lists(text()))
def test_error_input(x):
    assert(check_input(str(x)) == False)

#Checks that all valid input is accepted
@given(integers().filter(lambda x: (x > 7 and x < 201)))
def test_valid_input(x):
    assert(check_input(str(x)) == True)

#Checks that time is always increasing
@given(a = integers(), b = integers(), c = integers(), d = integers(), e = integers())
def test_time(a,b,c,d,e):
    game_state = {"time": a, "alt": b, "miles": c, "speed": d, "fuel": e}
    time_update(game_state)
    assert(a < game_state["time"] )

#Checks that fuel can not increase
@given(a = integers(), b = integers(), c = integers(), d = integers(), e = integers().filter(lambda x: (x >= 0)), rate=integers().filter(lambda x: (x >= 0)))
def test_fuel_level(a,b,c,d,e,rate):
    game_state = {"time": a, "alt": b, "miles": c, "speed": d, "fuel": e}
    fuel_update(game_state, rate)
    assert(e >= game_state["fuel"])

#Tests that free falling does not decrease speed
@given(a = integers().filter(lambda x: (x >= 0)), b = integers().filter(lambda x: (x > 0)), c = integers().filter(lambda x: (x >= 0)), d = integers().filter(lambda x: (x >= 0 and x < 1000000)), e = integers().filter(lambda x: (x >= 0)))
def test_free_falling_speed(a,b,c,d,e):
    game_state = {"time": a, "alt": b, "miles": c, "speed": d, "fuel": e}
    free_falling(game_state)
    assert(d <= game_state["speed"])

#Tests that time of free falling can not be negative
@given(a = integers().filter(lambda x: (x >= 0)), b = integers().filter(lambda x: (x >= 0)), c = integers().filter(lambda x: (x >= 0)), d = integers().filter(lambda x: (x >= 0)), e = integers().filter(lambda x: (x >= 0)))
def test_free_falling_time(a,b,c,d,e):
    game_state = {"time": a, "alt": b, "miles": c, "speed": d, "fuel": e}
    free_falling(game_state)
    assert(a <= game_state["time"])

#Checks that for positive speed the altitude should always be lowered
@given(a = integers(), b = integers().filter(lambda x: (x >= 1 and x <= 1000000)), c = integers(), d = integers(), e = integers().filter(lambda x: (x >= 1)), rate=integers().filter(lambda x: (x >= 8 and x <= 200)))
def test_lower_alt(a,b,c,d,e,rate):
    game_state = {"time": a, "alt": b, "miles": c, "speed": d, "fuel": e}
    speed_altitude_update(game_state, rate)
    assert(b >= game_state["alt"])

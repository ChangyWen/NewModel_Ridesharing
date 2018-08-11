from util import Rider, Vehicle, State
from strategy import match_stage, routing_stage, gen_time_rider
from numpy import np

map = np.zeros(100, 100)
distance = np.zeros(100, 100)
p_i = np.zeros((100, 100, 24*60), dtype=np.float)
state = State()
time = 1
vehicle = Vehicle()
vehicles = [vehicle]
rider = Rider()
riders = [rider]
time_rider = {} # t:[rider_list]

def action(rider_list)->list:
    '''
    action for every vehicle
    aim at the max obj
    :return:
    '''
    new_vehicles = match_stage(rider_list, vehicles)
    new_vehicles = routing_stage(rider_list, new_vehicles)
    update(new_vehicles)
    return

def update(vehicles: list):
    '''
    调用Vehicles和State的update方法
    update time
    :return:
    '''
    global time
    time = time + 1
    for i in range(len(vehicles)):
        vehicles[i].update()
    state.update()

def run(current_time: int, time_rider: dict):
    '''
    :param current_time:
    :param time_rider:
    :return:
    '''
    rider_list = time_rider[current_time]
    action(rider_list, vehicles)

def init(time: int, time_rider: dict):
    time_rider = gen_time_rider(time_rider)
    while time < 24*60:
        run(time, time_rider)
        time += 1
    return
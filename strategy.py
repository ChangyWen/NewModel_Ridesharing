import random
from util import State, Vehicle

def match_stage(rider_list: list, vehicles: list) -> list:
    '''
    :param rider_list:
    :param vehicles:
    :return:
    '''
    for i in range(len(vehicles)):
        print() # match rider for every driver (update the pickup_list)
    return vehicles

def routing_stage(rider_list: list, vehicle: Vehicle) -> list:
    '''
    :param rider_list:
    :param vehicles:
    :return: a route of an vehicle with the pickup_list from match_stage
    '''
    return

def gen_time_rider(time_rider: dict, riders: list)-> dict:
    '''
    :param time_rider:
    :param riders:
    :return:
    '''
    new_rider = {}
    for i in range(24):
        new_rider[i] = []
    for i in range(len(time_rider)):
        new_rider[i // 60] += time_rider[i]
    random.seed(10)
    for i in range(len(new_rider)):
        new_rider[i] = random.sample(new_rider[i], 1000)
    for i in range(24*60):
        time_rider[i] = []
    for i in range(len(new_rider)):
        for j in range(len(new_rider[j])):
            slot = riders[new_rider[j]].appear_time
            time_rider[slot].append(new_rider[j])
    return time_rider

def gen_neighbor(vertex: list, radius: float) -> dict:
    '''
    :param vertex:
    :return: neighbors of every vertex in the graph with radius = radius
    '''
    # dict = {v_id:[neighbor_list]}
    return

def expected_obj(state: State, vehicles: list) -> int:
    '''
    :param state:
    :param vehicles:
    :return: the expected objective function value
    '''
    e_obj = 0
    return e_obj
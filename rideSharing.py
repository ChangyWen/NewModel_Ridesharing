import util
import strategy
from numpy import np
import init_instances as ii
import copy
import strategy as st
def action(vehicle: util.Vehicle):
    # state = copy.deepcopy(ii.state)
    # riders = copy.deepcopy(ii.riders)
    riders = ii.riders
    rider = riders[vehicle.picked_up[0]]
    from_node = rider.from_node
    to_node = rider.to_node
    (shortest_path, shortest_time) = ii.floyd_path(from_node, to_node)
    time_slack = rider.deadline - rider.appear_slot - shortest_time
    if time_slack > 10:
        neighbor = st.gen_neighbor(shortest_path, time_slack)
        if len(neighbor) >= 2:
            best_expected = 0
            best_pair = [-1,-1]
            for i in range(len(neighbor)):
                for j in range(i+1, len(neighbor)):
                    temp_expected = st.cal_expected_revenue(vehicle, neighbor[i] ,neighbor[j])
                    if temp_expected > best_expected:
                        best_expected = temp_expected
                        best_pair[0], best_pair[1] = neighbor[i], neighbor[j]
            vehicle.pre_pickup += best_pair
        elif len(neighbor) > 0:
            vehicle.pre_pickup.append(neighbor[0])
    else:
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
    # state.update()

def cal_revenue(vehicle: util.Vehicle):
    print()

def run():
    ii.init_param()
    # vehicles = copy.deepcopy(ii.vehicles)
    vehicles = ii.vehicles
    for i in range(len(vehicles)):
        action(vehicles[i])
        cal_revenue(vehicles[i])
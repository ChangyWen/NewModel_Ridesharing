import util
import init_instances as ii
import strategy as st
import cal_revenue as cr
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
            if best_pair != [-1,-1]:
                vehicle.pre_pickup = best_pair
        elif len(neighbor) > 0:
            vehicle.pre_pickup.append(neighbor[0])
    else:
        return

def update(vehicle: util.Vehicle):
    vehicle.update_first()

def run():
    ii.init_param()
    # vehicles = copy.deepcopy(ii.vehicles)
    vehicles = ii.vehicles
    # for i in range(len(vehicles)):
    for i in range(3):
        action(vehicles[i])
        print('yeah')
        update(vehicles[i])
        # print(vehicles[i].location)
        # print(ii.riders[vehicles[i].picked_up[0]].from_node)
        # print(ii.riders[vehicles[i].picked_up[0]].to_node)
        print(vehicles[i].pre_pickup)
        print(vehicles[i].route)
        # cr.cal_final_revenue(vehicles[i])

if __name__ == '__main__':
    run()
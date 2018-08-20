import util
import init_instances as ii
import cal_revenue as cr
import feasible_check as fc
import strategy as st
import gen_map as gm
def action(vehicle: util.Vehicle):
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
                for j in range(len(neighbor)):
                    if i == j:
                        continue
                    temp_expected = st.cal_expected_revenue(vehicle, neighbor[i] ,neighbor[j])
                    a_d = vehicle.slot + ii.floyd_path(vehicle.location, neighbor[i])[1] + \
                          ii.floyd_path(neighbor[i], neighbor[j])[1] + ii.floyd_path(neighbor[j], to_node)[1]
                    if temp_expected > best_expected and a_d <= rider.deadline:
                        best_expected = temp_expected
                        best_pair[0], best_pair[1] = neighbor[i], neighbor[j]
            if best_pair != [-1,-1]:
                vehicle.pre_pickup = best_pair
    else:
        return

def update(vehicle: util.Vehicle):
    vehicle.update_first()

def simulate_pickup(v: util.Vehicle) -> int:
    v.passed_route = []
    v.passed_route.append(v.route[0])
    slot_i = v.slot
    flag = False
    i = 0
    length1 = len(v.route)
    print('first planning route')
    print(v.route)
    for i in range(1, length1 - 1):
        slot_i += gm.delta[(v.route[i - 1], v.route[i])]
        v.slot = slot_i
        v.location = v.route[i]
        v.passed_route.append(v.route[i])
        if len(ii.state.s_n[int(slot_i)][v.route[i]])> 0:
            for rider in ii.state.s_n[int(slot_i)][v.route[i]]:
                v.onboard.append(rider)
                (des_order, isOk) = fc.feasible_pick(v, rider, slot_i)
                if isOk:
                    ii.state.s_n[int(slot_i)][v.route[i]].remove(rider)
                    v.picked_up.append(rider)
                    v.update_pick(v.route[i],des_order)
                    print(des_order)
                    d = 0
                    for rider in v.picked_up:
                        d += 1
                        print('No.%(i)d:' % {'i': d})
                        print(ii.riders[rider].from_node)
                        print(ii.riders[rider].to_node)
                    print('Second planning route:')
                    print(v.route)
                    v.load += 1
                    flag = True
                    break
                else:
                    v.onboard.pop(-1)
        if flag:
            break
    if i == length1 - 2 and not flag:
        slot_i += gm.delta[(v.route[i], v.route[i + 1])]
        v.slot = slot_i
        v.location = v.route[i + 1]
        v.passed_route.append(v.route[i + 1])
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i + 1]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = slot_i
                v.load -= 1
        return cr.cal_final(v)
    flag = False
    length2 = len(v.route)
    for i in range(1, length2 - 1):
        if len(v.onboard) == 0:
            break
        slot_i += gm.delta[(v.route[i - 1], v.route[i])]
        v.slot = slot_i
        v.location = v.route[i]
        v.passed_route.append(v.route[i])
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = slot_i
                v.load -= 1
        if len(ii.state.s_n[int(slot_i)][v.route[i]])> 0:
            for rider in ii.state.s_n[int(slot_i)][v.route[i]]:
                v.onboard.append(rider)
                (des_order, isOk) = fc.feasible_pick(v, rider, slot_i)
                if isOk:
                    v.picked_up.append(rider)
                    d = 0
                    for rider in v.picked_up:
                        d += 1
                        print('No.%(i)d:'%{'i':d})
                        print(ii.riders[rider].from_node)
                        print(ii.riders[rider].to_node)
                    print('Third planning route:')
                    print(v.route)
                    ii.state.s_n[int(slot_i)][v.route[i]].remove(rider)
                    v.update_pick(v.route[i], des_order)
                    flag = True
                    break
                else:
                    v.onboard.pop(-1)
        if flag:
            break
    if i == length2 - 2 and not flag:
        slot_i += gm.delta[(v.route[i], v.route[i + 1])]
        v.slot = slot_i
        v.location = v.route[i + 1]
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i + 1]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = slot_i
                v.load -= 1
        v.passed_route.append(v.route[i + 1])
        return cr.cal_final(v)
    if flag:
        for i in range(1, len(v.route)):
            slot_i += gm.delta[(v.route[i - 1], v.route[i])]
            # slot_i += ii.floyd_path(v.route[i - 1], v.route[i])[1] / util.average_speed
            v.slot = slot_i
            v.location = v.route[i]
            if len(v.onboard) == 0:
                break
            v.passed_route.append(v.route[i])
            onboard = v.onboard.copy()
            for rider in onboard:
                if ii.riders[rider].to_node == v.route[i]:
                    v.onboard.remove(rider)
                    v.drop_off_slot[rider] = slot_i
                    v.load -= 1
    return cr.cal_final(v)

def run():
    ii.init_param()
    vehicles = ii.vehicles
    # print(ii.riders[vehicles[47].picked_up[0]].from_node)
    # print(ii.riders[vehicles[47].picked_up[0]].to_node)
    # print(ii.floyd_path(6, 24)[0])
    # print(ii.floyd_path(24,26)[0])
    # print(ii.floyd_path(6,26)[0])
    # for i in range(len(vehicles)):
    for i in range(30, 100):
        action(vehicles[i])
        print('vehicle%(i)d:'%{'i':i})
        update(vehicles[i])
        print(simulate_pickup(vehicles[i]))
        print('passed route:')
        print(vehicles[i].passed_route)
#
if __name__ == '__main__':
    run()
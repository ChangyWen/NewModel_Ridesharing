import util
import init_instances as ii
import cal_revenue as cr
import feasible_check as fc
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
            if best_pair != [-1,-1]:
                vehicle.pre_pickup = best_pair
        elif len(neighbor) > 0:
            vehicle.pre_pickup.append(neighbor[0])
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
    # print('fist planning route:')
    # print(v.route)
    length1 = len(v.route)
    for i in range(1, length1 - 1):
        if len(v.onboard) == 0:
            break
        slot_i += ii.floyd_path(v.route[i-1], v.route[i])[1] / util.average_speed
        v.slot = slot_i
        v.passed_route.append(v.route[i])
        drop = []
        for k in range(len(v.onboard)):
            if v.route[i] == ii.riders[v.onboard[k]].to_node:
                drop.append(k)
        for k in drop:
            v.drop_off_slot[v.onboard[k]] = slot_i
            v.onboard.pop(k)
        if len(ii.state.s_n[int(slot_i)][v.route[i]])> 0:
            for rider in ii.state.s_n[int(slot_i)][v.route[i]]:
                v.onboard.append(rider)
                (des_order, isOk) = fc.feasible_pick(v, rider, slot_i)
                if isOk:
                    ii.state.s_n[int(slot_i)][v.route[i]].remove(rider)
                    v.picked_up.append(rider)
                    # d = 0
                    # for rider in v.picked_up:
                    #     d += 1
                    #     print('第%(i)d：' % {'i': d})
                    #     print(ii.riders[rider].from_node)
                    #     print(ii.riders[rider].to_node)
                    v.update_pick(v.route[i],des_order)
                    # print('second planning route:')
                    # print(v.route)
                    flag = True
                    break
                else:
                    v.onboard.pop(-1)
        if flag:
            break
    if i == length1 - 2 and not flag:
        v.passed_route.append(v.route[i + 1])
        return cr.cal_final(v)
    slot_i = v.slot
    flag = False
    length2 = len(v.route)
    for i in range(1, length2 - 1):
        if len(v.onboard) == 0:
            break
        slot_i += ii.floyd_path(v.route[i - 1], v.route[i])[1] / util.average_speed
        v.slot = slot_i
        v.passed_route.append(v.route[i])
        drop = []
        for k in range(len(v.onboard)):
            if v.route[i] == ii.riders[v.onboard[k]].to_node:
                drop.append(k)
        for k in drop:
            v.drop_off_slot[v.onboard[k]] = slot_i
            v.onboard.pop(k)
        if len(ii.state.s_n[int(slot_i)][v.route[i]])> 0:
            for rider in ii.state.s_n[int(slot_i)][v.route[i]]:
                v.onboard.append(rider)
                (des_order, isOk) = fc.feasible_pick(v, rider, slot_i)
                if isOk:
                    v.picked_up.append(rider)
                    ii.state.s_n[int(slot_i)][v.route[i]].remove(rider)
                    d = 0
                    for rider in v.picked_up:
                        d += 1
                        print('第%(i)d：' % {'i': d})
                        print(ii.riders[rider].from_node)
                        print(ii.riders[rider].to_node)
                    v.update_pick(v.route[i], des_order)
                    # print('third planning route:')
                    # print(v.route)
                    flag = True
                    break
                else:
                    v.onboard.pop(-1)
        if flag:
            break
    if i == length2 - 2 and not flag:
        v.passed_route.append(v.route[i + 1])
        return cr.cal_final(v)
    if flag:
        for i in range(1, len(v.route)):
            if len(v.onboard) == 0:
                break
            v.passed_route.append(v.route[i])
            drop = []
            for k in range(len(v.onboard)):
                if v.route[i] == ii.riders[v.onboard[k]].to_node:
                    drop.append(k)
            for k in drop:
                v.drop_off_slot[v.onboard[k]] = slot_i
                v.onboard.pop(k)
        # rest_route = v.route
        # rest_route.pop(0)
        # v.passed_route += rest_route
    return cr.cal_final(v)

def run():
    ii.init_param()
    # vehicles = copy.deepcopy(ii.vehicles)
    vehicles = ii.vehicles
    # print(ii.riders[0].to_node)
    # for i in range(len(vehicles)):
    for i in range(3):
        action(vehicles[i])
        print('vehicle%(i)d:'%{'i':i})
        update(vehicles[i])
        print(simulate_pickup(vehicles[i]))
        print('passed route:')
        print(vehicles[i].passed_route)

if __name__ == '__main__':
    run()
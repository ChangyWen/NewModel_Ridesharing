import util
import gen_map
import cal_Probability as cp
import init_instances as ii

def routing_stage(s, node1: int, node2: int) -> list:
    if ii.floyd_path(s, node1)[1] + ii.floyd_path(node1, node2) > ii.floyd_path(s, node2)[1] + \
            ii.floyd_path(node2, node1)[1]:
        return [node2, node1]
    else:
        return [node1, node2]

def gen_neighbor(shortest_path: list, time_slack: int, floyd_path: util.Floyd_Path) -> list:
    neighbor = []
    for i in range(len(shortest_path) - 1):
        for j in range(len(gen_map.nodes)):
            if shortest_path[i] != j and j not in neighbor and floyd_path(i,j)[1] <= time_slack / 2:
                neighbor.append(j)
    return neighbor

def feasible_check(pre1:int,drop1:int,pre2:int,d:int, ddl: int, time_1:int) -> list:
    feasible_list = []
    min_i = time_1 + ii.floyd_path(pre1, drop1)[1]
    time_i = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
    time_d = time_i + (ii.floyd_path(drop1, pre2)[1] + ii.floyd_path(pre2,d)[1]) /util.average_speed
    feasible_list.append(False if time_d > ddl else True)
    time_i = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, drop1)[1]) / util.average_speed
    time_d = time_i + ii.floyd_path(drop1, d)[1] / util.average_speed
    feasible_list.append(False if time_d > ddl or time_i > (min_i + 20) else True)
    time_d = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1]) / util.average_speed
    time_i = time_d + ii.floyd_path(d, drop1)[1] / util.average_speed
    feasible_list.append(False if time_d > ddl or time_i > (min_i + 20) else True)
    return feasible_list


def feasible1_set(d:int ,ddl: int, pre1: int, time_1: int, pre2: int) -> (dict,bool):
    order_dict = {}
    for drop1 in gen_map.nodes:
        dis1 = ii.floyd_path(pre1, drop1)[1] + ii.floyd_path(drop1, pre2)[1] + ii.floyd_path(pre2, d)[1]
        dis2 = ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, drop1)[1] + ii.floyd_path(drop1, d)[1]
        dis3 = ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1] + ii.floyd_path(d, drop1)[1]
        order_dict[1], order_dict[2], order_dict[3] = dis1, dis2, dis3
        feasible_list = feasible_check(pre1,drop1,pre2,d, ddl, time_1)

    # set1_dict = {}
    # d = ii.riders[vehicle.picked_up[0]].to_node
    # ddl = ii.riders[vehicle.picked_up[0]].deadline
    # order_dict = {}
    # for i in gen_map.nodes:
    #     order = routing_stage(pre1, i, pre2)
    #     if order[0] == pre2:
    #         time_2 = time_1 + ii.floyd_path(pre1, pre2)[1]
    #         drop_order = routing_stage(pre2, i, d)
    #         if feasible_check(order.pop() + drop_order, False, time_1, time_2):
    #             set1_dict[i] = (time_2, False)
    #         else:
    #             continue
    #     else:
    #         time_2 = time_1 + ii.floyd_path(pre1, i)[1] + ii.floyd_path(i, pre2)[1]
    #         if feasible_check(order.append(d), True, time_1, time_2):
    #             set1_dict[i] = (time_2, True)
    #         else:
    #             continue
    # return set1_dict
    #         if drop_order[0] == i:
    #             time_i = time_2 + ii.floyd_path(pre2, i)[1]
    #             if time_i <= time_1 + ii.floyd_path(pre1, i)[1] + 20:
    #                 time_d = time_i + ii.floyd_path(i, d)[1]
    #                 if time_d <= ddl:
    #                     set1_dict[i] = (time_2, False)
    #                 else:
    #                     continue
    #             else:
    #                 continue
    #     else:
    #         time_2 = time_1 + ii.floyd_path(pre1, i)[1] + ii.floyd_path(i, pre2)[1]
    #         time_d = time_2 + ii.floyd_path(pre2, d)[1]
    #         if time_d > ddl:
    #             continue
    #         else:
    #             set1_dict[i] = (time_2, True)  # True for the drop_off node of pre1 is between pre1 and pre2
    # return set1_dict

def feasible2_set(vehicle: util.Vehicle, pre1:int, drop1: int, pre2: int, time2: int) -> list:
    return

def count_revenue(vehicle, pre1,drop1,pre2,drop2) -> int:
    return

def cal_expected_revenue(vehicle: util.Vehicle, node1: int, node2: int) -> int:
    first_rider = ii.riders[vehicle.picked_up[0]]
    time = first_rider.appear_slot
    s = first_rider.from_node
    d = first_rider.to_node
    ddl = first_rider.deadline
    pre_pickup = routing_stage(s,node1, node2)
    pre1, pre2 = pre_pickup[0], pre_pickup[1]
    time1 = ii.floyd_path(s, pre1)[1] / util.average_speed + time
    # time2 = ii.floyd_path(pre1, pre2)[1] / util.average_speed + time1
    expected_revenue = cp.P_i[pre1][time1]
    set1_dict = feasible1_set(d, ddl, pre1, time1, pre2)
    temp1 = 0
    for drop1,time2 in set1_dict.items():
        set2_dict = feasible2_set(vehicle, pre1, drop1, pre2, time2)
        temp2 = 0
        for drop2 in set2_dict.keys():
            w = count_revenue(vehicle, pre1,drop1,pre2,drop2)
            temp2 += w * cp.P_ij[pre2][drop2][time2]
        temp2 = temp2 * cp.P_i[pre2][time2]
        temp1 += cp.P_ij[pre1][drop1][time1] * temp2
    expected_revenue *= temp1
    return expected_revenue
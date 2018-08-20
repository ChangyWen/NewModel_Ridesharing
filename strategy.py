import util
import gen_map
import cal_Probability as cp
import init_instances as ii
import feasible_check as fc
import cal_revenue as cr
def routing_stage(s, node1: int, node2: int) -> list:
    if ii.floyd_path(s, node1)[1] + ii.floyd_path(node1, node2)[1] > ii.floyd_path(s, node2)[1] + \
            ii.floyd_path(node2, node1)[1]:
        return [node2, node1]
    else:
        return [node1, node2]

def gen_neighbor(shortest_path: list, time_slack: int = 10) -> list:
    neighbor = []
    for i in range(len(shortest_path) - 1):
        for j in gen_map.nodes:
            if  j not in neighbor and i and ii.floyd_path(i,j)[1] <= time_slack / 2:
                neighbor.append(j)
    dict1 = {}
    s = shortest_path[0]
    d = shortest_path[-1]
    max_dis = ii.floyd_path(s,d)[1]
    for i in neighbor:
        dict1[i] = ii.floyd_path(s, i)[1]
    dict1 = {k:v for k,v in dict1.items() if v < max_dis}
    sort_dict = dict(sorted(dict1.items(), key=lambda d: d[1], reverse=False))
    neighbor = list(sort_dict.keys())
    return neighbor


def cal_time_2(type1:int, pre1:int,drop1:int,pre2:int,time_1:int) -> int:
    if type1 == 1:
        time_2 = time_1 + (ii.floyd_path(pre1, drop1)[1] + ii.floyd_path(drop1, pre2)[1]) / util.average_speed
    else:
        time_2 = time_1 + (ii.floyd_path(pre1, pre2)[1]) / util.average_speed
    return time_2

def cal_expected_revenue(vehicle, node1: int, node2: int) -> int:
    first_rider = ii.riders[vehicle.picked_up[0]]
    time = first_rider.appear_slot
    s = first_rider.from_node
    d = first_rider.to_node
    ddl = first_rider.deadline
    pre_pickup = routing_stage(s,node1, node2)
    pre1, pre2 = pre_pickup[0], pre_pickup[1]
    time_1 = ii.floyd_path(s, pre1)[1] / util.average_speed + time
    expected_revenue = cp.P_i[pre1][int(time_1)]
    set1_dict = fc.feasible1_set(d, ddl, pre1, time_1, pre2)
    temp1 = 0
    P, P1, P2, P3 = 0, 0, 0, 0
    for drop1,type1 in set1_dict.items():
        time_2 = cal_time_2(type1, pre1, drop1, pre2, time_1)
        ddl_1 = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed + 20
        set2_dict = fc.feasible2_set(type1,d,ddl, drop1, ddl_1, pre2, time_2)
        temp2 = 0

        infeasible_drop2 = set(gen_map.nodes) ^ set(set2_dict.keys())
        term1 = 1 - cp.P_i[pre2][int(time_2)]
        w = cr.cal_pre1_revenue(vehicle, type1, pre1, drop1,time_1, pre2, d)
        for drop2 in infeasible_drop2:
            P1 += cp.P_ij[pre2][drop2][int(time_2)]
        term = w * P1 * cp.P_i[pre2][int(time_2)] + term1 * w
        P1 = P1 * cp.P_i[pre2][int(time_2)]

        for drop2,type2 in set2_dict.items():
            w = cr.cal_two_revenue(vehicle, type1,type2, pre1,drop1,time_1, pre2,drop2, time_2, d)
            temp2 += w * cp.P_ij[pre2][drop2][int(time_2)]
            P2 += cp.P_ij[pre2][drop2][int(time_2)]
        temp2 = temp2 * cp.P_i[pre2][int(time_2)]
        temp1 += cp.P_ij[pre1][drop1][int(time_1)] * temp2
        temp1 += cp.P_ij[pre1][drop1][int(time_1)] * term
        P2 = P2 * cp.P_i[pre2][int(time_2)]
        P += (P1 + P2 + term1) * cp.P_ij[pre1][drop1][int(time_1)]
    expected_revenue *= temp1
    P *= cp.P_i[pre1][int(time_1)]

    factor2 = 1 - cp.P_i[pre1][int(time_1)]
    temp4 = 0
    rest = set(gen_map.nodes) ^ set(set1_dict.keys())
    for drop1 in rest:
        temp4 += cp.P_ij[pre1][drop1][int(time_1)]
    factor2 = factor2 + cp.P_i[pre1][int(time_1)] * temp4
    P4 = factor2
    #   factor2 += cp.P_i[pre1][int(time_1)] * cp.P_ij[pre2][drop1][int(time_1)]
    time_2 = time_1 + ii.floyd_path(pre1, pre2)[1] / util.average_speed
    set2_dict = fc.feasible2_set(1, d, ddl, 0, 0, pre2, time_2)
    factor2 *= cp.P_i[pre2][int(time_2)]
    temp = 0
    P5 = 0
    for drop2,type2 in set2_dict.items():
        P5 += cp.P_ij[pre2][drop2][int(time_2)]
        w = cr.cal_pre2_revenue(vehicle,type2, pre1, pre2, drop2, time_2)
        temp += w * cp.P_ij[pre2][drop2][int(time_2)]
    P5 *= cp.P_i[pre2][int(time_2)]
    P = P + P4 + P5
    factor2 *= temp
    expected_revenue += factor2
    no_ride_sharing_revenue = P * cr.cal_no_revenue(vehicle,pre1, pre2, d)
    expected_revenue += no_ride_sharing_revenue
    return expected_revenue

def cal_best_one(v, node: int, time:int) -> int:
    factor = 0
    for drop in gen_map.nodes:
        ddl = time + ii.floyd_path(node, drop)[1] / util.average_speed + 40
        (drop_list, flag) = fc.check_feasible_3(v, node, drop, ddl, time)
        if flag:
            w = cr.cal_last_one_revenue(v, drop_list, time, node)
            factor += cp.P_ij[node][drop][time] * w
    factor *= cp.P_i[node][time]
    return factor

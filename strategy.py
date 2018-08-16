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
            if j not in shortest_path and j not in neighbor and i and ii.floyd_path(i,j)[1] <= time_slack / 2:
            # if shortest_path[i] != j and j not in neighbor and i and ii.floyd_path(i,j)[1] <= time_slack / 2:
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
    # time2 = ii.floyd_path(pre1, pre2)[1] / util.average_speed + time1
    expected_revenue = cp.P_i[pre1][int(time_1)]
    set1_dict = fc.feasible1_set(d, ddl, pre1, time_1, pre2)
    temp1 = 0
    for drop1,type1 in set1_dict.items():
        time_2 = cal_time_2(type1, pre1, drop1, pre2, time_1)
        ddl_1 = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed + 20
        set2_dict = fc.feasible2_set(type1,d,ddl, drop1, ddl_1, pre2, time_2)
        temp2 = 0
        for drop2,type2 in set2_dict.items():
            w = cr.cal_revenue(type1,type2, pre1,drop1,time_1, pre2,drop2, time_2)
            temp2 += w * cp.P_ij[pre2][drop2][int(time_2)]
        temp2 = temp2 * cp.P_i[pre2][int(time_2)]
        temp1 += cp.P_ij[pre1][drop1][int(time_1)] * temp2
    expected_revenue *= temp1

    factor2 = 1 - cp.P_i[pre1][int(time_1)]
    rest = set(gen_map.nodes) ^ set(set1_dict.keys())
    for drop1 in rest:
        factor2 += cp.P_i[pre1][int(time_1)] * cp.P_ij[pre2][drop1][int(time_1)]
    time_2 = time_1 + ii.floyd_path(pre1, pre2)[1] / util.average_speed
    set2_dict = fc.feasible2_set(1, d, ddl, 0, 0, pre2, time_2)
    factor2 *= cp.P_i[pre2][int(time_2)]
    temp = 0
    for drop2,type2 in set2_dict.items():
        w = 1 # !!!!!
        temp += w * cp.P_ij[pre2][drop2][int(time_2)]
    factor2 *= temp
    expected_revenue += factor2

    return expected_revenue

def cal_best_one(v, node: int, time:int) -> int:
    factor = 0
    for drop in gen_map.nodes:
        ddl = time + ii.floyd_path(node, drop)[1] / util.average_speed + 20
        if fc.check_feasible_3(v, node, drop, ddl):
            factor += cp.P_ij[node][drop][time] * 5 # 1!!!!
    factor *= cp.P_i[node][time]
    return factor

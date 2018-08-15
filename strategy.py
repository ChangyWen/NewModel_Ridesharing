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

def gen_neighbor(shortest_path: list, time_slack: int) -> list:
    neighbor = []
    for i in range(len(shortest_path) - 1):
        for j in gen_map.nodes:
            if shortest_path[i] != j and j not in neighbor and ii.floyd_path(i,j)[1] <= time_slack / 2:
                neighbor.append(j)
    return neighbor

# def feasible1_check(pre1:int,drop1:int,pre2:int,d:int, ddl: int, time_1:int) -> dict:
#     feasible_dict = {}
#     min_i = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
#     time_i = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
#     time_d = time_i + (ii.floyd_path(drop1, pre2)[1] + ii.floyd_path(pre2,d)[1]) /util.average_speed
#     feasible_dict[1] = (False if time_d > ddl else True)
#     time_i = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, drop1)[1]) / util.average_speed
#     time_d = time_i + ii.floyd_path(drop1, d)[1] / util.average_speed
#     feasible_dict[2] = (False if time_d > ddl or time_i > (min_i + 20) else True)
#     time_d = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1]) / util.average_speed
#     time_i = time_d + ii.floyd_path(d, drop1)[1] / util.average_speed
#     feasible_dict[3] = (False if time_d > ddl or time_i > (min_i + 20) else True)
#     return feasible_dict
#
# def feasible2_check(type1: int,pre2, drop2, drop1, ddl_1, d, ddl, time_2 ) -> dict:
#     ddl_2 = time_2 + ii.floyd_path(pre2, drop2) / util.average_speed + 20
#     feasible_dict = {}
#     if type1 == 3:
#         d,drop1 = drop1,d
#         ddl, ddl_1 = ddl_1, ddl
#     time_j = time_2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
#     time_i = time_j +  ii.floyd_path(drop2, drop1)[1] / util.average_speed
#     time_d = time_i + ii.floyd_path(drop1, d) /  util.average_speed
#     feasible_dict[1] = (False if time_i > ddl_1 or time_d > ddl else True)
#     time_i = time_2 + ii.floyd_path(pre2, drop1)[1] / util.average_speed
#     time_j = time_i + ii.floyd_path(drop1, drop2)[1] / util.average_speed
#     time_d = time_j + ii.floyd_path(drop2, d) / util.average_speed
#     feasible_dict[2] = (False if time_i > ddl_1 or time_j > ddl_2 or time_d > ddl else True)
#     time_i = time_2 + ii.floyd_path(pre2, drop1)[1] / util.average_speed
#     time_d = time_i + ii.floyd_path(drop1, d)[1] / util.average_speed
#     time_j = time_d + ii.floyd_path(d, drop2) / util.average_speed
#     feasible_dict[3] = (False if time_i > ddl_1 or time_j > ddl_2 or time_d > ddl else True)
#     return feasible_dict
#
# def feasible1_set(d:int ,ddl: int, pre1: int, time_1: int, pre2: int) -> dict:
#     order_dict = {}
#     return_dict = {}
#     for drop1 in gen_map.nodes:
#         dis1 = ii.floyd_path(pre1, drop1)[1] + ii.floyd_path(drop1, pre2)[1] + ii.floyd_path(pre2, d)[1]
#         dis2 = ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, drop1)[1] + ii.floyd_path(drop1, d)[1]
#         dis3 = ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1] + ii.floyd_path(d, drop1)[1]
#         order_dict[1], order_dict[2], order_dict[3] = dis1, dis2, dis3
#         feasible_dict = feasible1_check(pre1,drop1,pre2,d, ddl, time_1)
#         if True not in feasible_dict.values():
#             continue
#         elif False not in feasible_dict.values():
#             type1 = sorted(order_dict.items(), key = lambda d:d[1],reverse=False)[0][0]
#         else:
#             true_key = [k for k,v in feasible_dict.items() if v == True]
#             true_dict = {k:v for k,v in order_dict.items() if k in true_key}
#             type1 = sorted(true_dict.items(), key=lambda d: d[1], reverse=False)[0][0]
#         return_dict[drop1] = type1
#     return return_dict
#
# def feasible2_set(type1:int,d:int,ddl:int, drop1: int,ddl_1:int, pre2: int, time_2: int) -> dict:
#     order_dict = {}
#     return_dict = {}
#     if type1 == 1:
#         for drop2 in gen_map.nodes:
#             true_dict = {1:True, 2:True}
#             dis_dict = {}
#             dis1 = ii.floyd_path(pre2, drop2)[1] + ii.floyd_path(drop2, d)[1]
#             dis_dict[1] = dis1
#             if time_2 + dis1 / util.average_speed > time_2 + ii.floyd_path(pre2, drop2)[1] /util.average_speed:
#                 true_dict[1] = False
#             dis2 = ii.floyd_path(pre2, d)[1] + ii.floyd_path(d, drop2)[1]
#             dis_dict[2] = dis2
#             if time_2 + ii.floyd_path(pre2, d)[1] /util.average_speed > ddl or time_2 + dis2 /util.average_speed > \
#                 time_2 + ii.floyd_path(pre2, drop2)[1] /util.average_speed:
#                 true_dict[2] = False
#             if True not in true_dict.values():
#                 continue
#             else:
#                 true_key = [k for k, v in true_dict.items() if v == True]
#                 true_dict = {k: v for k, v in dis_dict.items() if k in true_key}
#                 type2 = sorted(true_dict.items(), key=lambda d: d[1], reverse=False)[0][0]
#             return_dict[drop2] = type2
#         return return_dict
#     elif type1 == 3:
#         d,drop1 = drop1,d
#         ddl,ddl_1 = ddl_1,ddl
#     for drop2 in gen_map.nodes:
#         dis1 = ii.floyd_path(pre2, drop2)[1] + ii.floyd_path(drop2, drop1)[1] + ii.floyd_path(drop2, d)[1]
#         dis2 = ii.floyd_path(pre2, drop1)[1] + ii.floyd_path(drop1, drop2)[1] + ii.floyd_path(drop2, d)[1]
#         dis3 = ii.floyd_path(pre2, drop1)[1] + ii.floyd_path(drop1, d)[1] + ii.floyd_path(d, drop2)[1]
#         order_dict[3], order_dict[4], order_dict[5] = dis1, dis2, dis3
#         feasible_dict = feasible2_check(type1, pre2, drop2, drop1, ddl_1, d, ddl, time_2)
#         if True not in feasible_dict.values():
#             continue
#         elif False not in feasible_dict.values():
#            type2 = sorted(order_dict.items(), key = lambda d:d[1],reverse=False)[0][0]
#         else:
#             true_key = [k for k, v in feasible_dict.items() if v == True]
#             true_dict = {k:v for k, v in order_dict.items() if k in true_key}
#             type2 = sorted(true_dict.items(), key=lambda d: d[1], reverse=False)[0][0]
#         return_dict[drop2] = type2
#     return return_dict
#     # elif type1 == 3:
#     #     for drop2 in gen_map.nodes:
#     #         dis1 = ii.floyd_path(pre2, drop2)[1] + ii.floyd_path(drop2, d)[1] + ii.floyd_path(d, drop1)[1]
#     #         dis2 = ii.floyd_path(pre2, d)[1] + ii.floyd_path(d, drop2)[1] + ii.floyd_path(drop2, drop1)[1]
#     #         dis3 = ii.floyd_path(pre2, d)[1] + ii.floyd_path(d, drop1)[1] + ii.floyd_path(drop1, drop2)[1]
#     #         feasible2_check(type1, pre2, drop2, drop1, ddl_1, d, ddl, time_2)

def cal_time_2(type1:int, pre1:int,drop1:int,pre2:int,time_1:int) -> int:
    if type1 == 1:
        time_2 = time_1 + (ii.floyd_path(pre1, drop1)[1] + ii.floyd_path(drop1, pre2)[1]) / util.average_speed
    else:
        time_2 = time_1 + (ii.floyd_path(pre1, pre2)[1]) / util.average_speed
    return time_2

def cal_expected_revenue(vehicle: util.Vehicle, node1: int, node2: int) -> int:
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
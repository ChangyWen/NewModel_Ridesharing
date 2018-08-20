import util
import init_instances as ii

beta = 0.4
rate = 4

def cal_two_revenue(v, type1, type2, pre1,drop1, time1,pre2,drop2, time2, d:int) -> float:
    if type2 == 1:
        a_1 = time1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
        a_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
        a_d = a_2 + ii.floyd_path(drop2, d)[1] / util.average_speed
    elif type2 == 2:
        a_1 = time1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
        a_d = time2 + ii.floyd_path(pre2, d)[1] / util.average_speed
        a_2 = a_d + ii.floyd_path(d, drop2)[1] / util.average_speed
    if type1 == 2:
        if type2 == 3:
            a_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
            a_1 = a_2 + ii.floyd_path(drop2, drop1)[1] / util.average_speed
            a_d = a_1 + ii.floyd_path(drop1, d)[1] / util.average_speed
        elif type2 == 4:
            a_1 = time2 + ii.floyd_path(pre2, drop1)[1] / util.average_speed
            a_2 = a_1 + ii.floyd_path(drop1, drop2)[1] / util.average_speed
            a_d = a_2 + ii.floyd_path(drop2, d)[1] / util.average_speed
        elif type2 == 5:
            a_1 = time2 + ii.floyd_path(pre2, drop1)[1] / util.average_speed
            a_d = a_1 + ii.floyd_path(drop1, d)[1] / util.average_speed
            a_2 = a_d + ii.floyd_path(d, drop2)[1] / util.average_speed
    elif type1 == 3:
        if type2 == 3:
            a_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
            a_d = a_2 + ii.floyd_path(drop2, d)[1] / util.average_speed
            a_1 = a_d + ii.floyd_path(d, drop1)[1] / util.average_speed
        elif type2 == 4:
            a_d = time2 + ii.floyd_path(pre2, d)[1] / util.average_speed
            a_2 = a_d + ii.floyd_path(d, drop2)[1] / util.average_speed
            a_1 = a_2 + ii.floyd_path(drop2, drop1)[1] / util.average_speed
        elif type2 == 5:
            a_d = time2 + ii.floyd_path(pre2, d)[1] / util.average_speed
            a_1 = a_d + ii.floyd_path(drop1, d)[1] / util.average_speed
            a_2 = a_1 + ii.floyd_path(d, drop2)[1] / util.average_speed
    ea_1 = time1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
    er_1 = rate * ii.floyd_path(pre1, drop1)[1] - beta * (a_1 - ea_1)
    ea_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
    er_2 = rate * ii.floyd_path(pre2, drop2)[1] - beta * (a_2 - ea_2)
    ea_d = v.slot + ii.floyd_path(v.location, d)[1] / util.average_speed
    er_d = rate * ii.floyd_path(v.location, d)[1] - beta * (a_d - ea_d)
    return er_1 + er_2 + er_d

def cal_pre1_revenue(v, type1, pre1, drop1,time_1, pre2, d) -> float:
    if type1 == 1:
        a_1 = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
        a_d = a_1 + (ii.floyd_path(drop1, pre2)[1] + ii.floyd_path(pre1, drop1)[1]) / util.average_speed
    elif type1 == 2:
        a_1 = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, drop1)[1]) / util.average_speed
        a_d = a_1 + ii.floyd_path(drop1, d)[1] / util.average_speed
    else:
        a_d = time_1 + (ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1]) / util.average_speed
        a_1 = a_d + ii.floyd_path(d, drop1)[1] / util.average_speed
    ea_1 = time_1 + ii.floyd_path(pre1, drop1)[1] / util.average_speed
    ea_d = v.slot + ii.floyd_path(v.location, d)[1] / util.average_speed
    er_1 = rate * ii.floyd_path(pre1, drop1)[1] - beta * (a_1 - ea_1)
    er_d = rate * ii.floyd_path(v.location, d)[1] - beta * (a_d - ea_d)
    return er_1 + er_d

def cal_pre2_revenue(v, type2, pre1, pre2, drop2, time2) -> float:
    d = ii.riders[v.picked_up[0]].to_node
    if type2 == 1:
        a_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
        a_d = a_2 + ii.floyd_path(drop2, d)[1] / util.average_speed
    else:
        a_d = time2 + ii.floyd_path(pre2, d)[1] / util.average_speed
        a_2 = a_d + ii.floyd_path(d, drop2)[1] / util.average_speed
    ea_2 = time2 + ii.floyd_path(pre2, drop2)[1] / util.average_speed
    ea_d = v.slot + ii.floyd_path(v.location, d)[1] / util.average_speed
    r_2 = rate * ii.floyd_path(pre2, drop2)[1] - beta * (a_2 - ea_2)
    r_d = rate * ii.floyd_path(v.location, d)[1] - beta * (a_d - ea_d)
    return r_2 + r_d

def cal_no_revenue(v, pre1, pre2, d) -> float:
    ea_d = v.slot + ii.floyd_path(v.location, d)[1] / util.average_speed
    a_d = v.slot + (ii.floyd_path(v.location, pre1)[1] + ii.floyd_path(pre1, pre2)[1] + ii.floyd_path(pre2, d)[1]) \
          / util.average_speed
    return rate * (ii.floyd_path(v.location, d)[1]) - beta * (a_d - ea_d)

def cal_last_one_revenue(v, drop_list, time ,node) -> float:
    a_i_list = []
    ea_i_list = []
    dis_i = []
    a_i = time
    revenue = 0
    order_dict = {}
    for i in range(len(drop_list)):
        for rider in v.onboard:
            if ii.riders[rider].to_node == drop_list[i]:
                order_dict[i] = rider
                break
        if i not in order_dict.keys():
            order_dict[i] = -1
    order_dict = dict(sorted(order_dict.items(), key=lambda e:e[0], reverse=False))
    for i in range(len(order_dict)):
        if order_dict[i] == -1:
            a_i_list.append(a_i + ii.floyd_path(node, drop_list[i])[1] / util.average_speed)
            ea_i_list.append(time + ii.floyd_path(node, drop_list[i])[1] / util.average_speed)
            dis_i.append(ii.floyd_path(node, drop_list[i])[1])
        if order_dict[i] == v.onboard[0]:
            a_i_list.append(a_i + ii.floyd_path(node, drop_list[i])[1] / util.average_speed)
            ea_i_list.append(ii.riders[v.onboard[0]].appear_slot +
                             ii.floyd_path(ii.riders[v.onboard[0]].from_node, ii.riders[v.onboard[0]].to_node)[
                                 1] / util.average_speed)
            dis_i.append(ii.floyd_path(ii.riders[v.onboard[0]].from_node, ii.riders[v.onboard[0]].to_node)[1])
        if order_dict == v.onboard[1]:
            a_i_list.append(a_i + ii.floyd_path(node, drop_list[i])[1] / util.average_speed)
            ea_i_list.append(ii.riders[v.onboard[1]].appear_slot +
                             ii.floyd_path(ii.riders[v.onboard[1]].from_node, ii.riders[v.onboard[1]].to_node)[
                                 1] / util.average_speed)
            dis_i.append(ii.floyd_path(ii.riders[v.onboard[1]].from_node, ii.riders[v.onboard[1]].to_node)[1])
        node = drop_list[i]
    for i in range(len(a_i_list)):
        r = rate * dis_i[i] - beta * (a_i_list[i] - ea_i_list[i])
        revenue += r
    return revenue

def cal_final(v) -> float:
    final_revenue = 0
    for r in v.picked_up:
        ea = ii.riders[r].appear_slot + ii.floyd_path(ii.riders[r].from_node, ii.riders[r].to_node)[1] / util.average_speed
        a = v.drop_off_slot[r]
        print('delay:')
        print(a - ea)
        revenue = rate * ii.floyd_path(ii.riders[r].from_node, ii.riders[r].to_node)[1] - beta * (a - ea)
        final_revenue += revenue
    return final_revenue




import util
import init_instances as ii

beta = 0.4
rate = 4
s = ii.state
def cal_two_revenue(v, type1, type2, pre1,drop1, time1,pre2,drop2, time2, d:int) -> int:
    # if type1 == 1:
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

def cal_one_revenue(v, type2, pre1, pre2, drop2):
    return 5

def cal_last_one_revenue(v, pre, drop):
    return

def cal_final(v) -> int:

    return




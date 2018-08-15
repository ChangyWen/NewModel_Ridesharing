import util
import init_instances as ii
import feasible_check as fc
import strategy as st
s = ii.state
def cal_revenue(type1, type2, pre1,drop1, time1,pre2,drop2, time2) -> int:
    # if type1 == 1:
    #     if type2 == 1:
    #     elif type2 == 2:
    # elif type1 == 2:
    #     elif type2 == 3:
    #     elif type2 == 4:
    #     elif type2 == 5:
    # elif type1 == 3:
    #     elif type2 == 3:
    #     elif type2 == 4:
    #     elif type2 == 5:
    return 5

def cal_final_revenue(v: util.Vehicle) -> int:
    # flag = False
    # passed_route = []
    # for i in range(2):
    #     route = v.route.copy()
    #     start = route.pop(0)
    #     passed_route.append(start)
    #     slot_i = v.slot + ii.floyd_path(start, route[0])[1] / util.average_speed
    #     for node in route:
    #         passed_route.append(node)
    #         if len(s.s_n[slot_i][node]) > 0:
    #             for rider in s.s_n[slot_i][node]:
    #                 if fc.feasible_check(rider):
    #                     v.picked_up.append(rider)
    #                     st.arrange_last(v, slot_i, node)
    #                     flag = True
    #                     break
    #             if flag:
    #                 break

    return

from read_data import read_riders
from numpy import np

def cal_P_i():
    days = 31
    data = read_riders(r'data\yellow_tripdata_2017-12.csv')
    data.sort(key = take_puLoctaion)
    loc_nums = data[-1][2]
    slot_nums = 60 * 24
    P_i = np.array(loc_nums, slot_nums)
    for i in range(len(data)):
        data[i].insert(0, data[i][0].day)
        data[i][1] = data[i][1].hour * 60 + data[i][1].minute
        data[i][2] = data[i][2].hour * 60 + data[i][2].minute
    for i in range(loc_nums):
        loc_temp = list(filter(lambda x:x[3] == i, data))
        for j in range(len(loc_temp)):
            for k in range(slot_nums):
                slot_temp = list(filter(lambda x:x[0] == k, loc_temp))
                for d in range(days):
                    final = list(filter(lambda x: x[0] == d, slot_temp))
                    P_i[i][k] = len(len(final)) / days


def take_puLoctaion(elem):
    return elem[2]

# def take_location

cal_P_i()
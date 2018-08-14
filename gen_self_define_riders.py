import pandas as pd
from random import choice
from random import randint
from random import sample
from cal_Probability import slot_nums,days
from gen_map import *
import util

def gen_ori_riders() -> list:
    floyd_path = set_Floyd_Path()
    df = pd.DataFrame(columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    for k in range(50000):
        t_p = randint(0, slot_nums - 1)
        pickup = choice(nodes)
        drop_off = choice(nodes)
        d = randint(1, days)
        min_travel_time = floyd_path(pickup, drop_off)[1] / util.average_speed
        t_d = t_p + min_travel_time
        df.loc[k] = [t_p, t_d, pickup, drop_off ,d]
    df.to_csv(r'data\self_gen_riders.csv', index= False,header=True, float_format='%d')
    # riders_list = df.values.tolist()
    # return riders_list

def choose_instances(nums: int):
    df = pd.read_csv(r'data\self_gen_riders.csv')
    riders_list = df.values.tolist()
    riders = sample(riders_list, nums)
    riders = pd.DataFrame(riders, columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    riders.to_csv(r'data\choosed_instances.csv',index= False,header=True, float_format='%d')
    return riders

# gen_ori_riders()
# if __name__ == '__main__':
#     choose_instances(500)
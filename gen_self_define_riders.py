import numpy as np
import pandas as pd
from random import choice
from random import randint
from random import sample
from cal_Probability import loc_nums,slot_nums,days
from gen_map import nodes,set_Floyd_Path
from util import average_speed

def gen_ori_riders() -> list:
    floyd_path = set_Floyd_Path()
    df = pd.DataFrame(columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    for k in range(10000):
        t_p = randint(0, slot_nums - 1)
        pickup = choice(nodes)
        drop_off = choice(nodes)
        d = randint(1, days)
        min_travel_time = floyd_path(pickup, drop_off)[1] / average_speed
        t_d = t_p + min_travel_time
        df.loc[k] = [t_p, t_d, pickup, drop_off ,d]
    df.to_csv(r'data\self_gen_riders.csv', index= False,header=True)
    # riders_list = df.values.tolist()
    # return riders_list

def choose_instances(nums: int):
    df = pd.read_csv(r'data\self_gen_riders.csv')
    riders_list = df.values.tolist()
    riders = sample(riders_list, nums)
    print(riders)
    riders = pd.DataFrame(riders, columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    return riders

# gen_ori_riders()
# choose_instances(5)
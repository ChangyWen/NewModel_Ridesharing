import gen_self_define_riders
from util import *
import gen_map
import pandas as pd
from random import randint

riders = []
vehicles = []

def init_instances():
    gen_map.set_Floyd_Path()
    riders_df = pd.read_csv(r'data\choosed_instances.csv')
    global riders
    for i in range(len(riders_df)):
        rider = Rider(i, riders_df.loc[i,'PULocationID'], riders_df.loc[i,'DOLocationID'],\
                      riders_df.loc[i,'tpep_pickup_datetime'], riders_df.loc[i,'tpep_dropoff_datetime'] + randint(5,15))
        rider.flag = 1
        riders.append(rider)
        vehicle = Vehicle(i, rider.from_node, rider.appear_time, i)
        vehicle.load += 1
        vehicles.append(vehicle)

def init_request():
    riders_df = gen_self_define_riders.choose_instances(5000)
    for i in range(len(riders_df)):
        rider = Rider(i, riders_df.loc[i,'PULocationID'], riders_df.loc[i,'DOLocationID'],\
                      riders_df.loc[i,'tpep_pickup_datetime'], riders_df.loc[i,'tpep_dropoff_datetime'] + randint(5,15))
        riders.append(rider)

# if __name__ == '__main__':
#     init_instances()
#     init_request()
#     print(len(riders))
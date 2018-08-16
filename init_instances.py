import util
import gen_map
import pandas as pd
import cal_Probability as cp
#from random import randint

riders = []
vehicles = []
state = None
floyd_path = None

def init_instances():
    riders_df = pd.read_csv(r'data\choosed_instances_500.csv')
    global riders
    for i in range(len(riders_df)):
        if riders_df.loc[i, 'tpep_pickup_datetime'] > 1300:
            continue
        rider = util.Rider(i, riders_df.loc[i,'PULocationID'], riders_df.loc[i,'DOLocationID'],\
                      riders_df.loc[i,'tpep_pickup_datetime'], riders_df.loc[i,'tpep_dropoff_datetime'] + 25)
        rider.flag = 1
        riders.append(rider)
        vehicle = util.Vehicle(i, rider.from_node, rider.appear_slot, rider.r_id)
        vehicle.load += 1
        vehicles.append(vehicle)

def init_request():
    # riders_df = gen_self_define_riders.choose_instances(5000)
    # riders_df = pd.read_csv(r'data\choosed_instances_5000.csv')
    riders_df = pd.read_csv(r'data\self_gen_riders.csv')
    for i in range(len(riders_df)):
        rider = util.Rider(i, riders_df.loc[i,'PULocationID'], riders_df.loc[i,'DOLocationID'],\
                      riders_df.loc[i,'tpep_pickup_datetime'], riders_df.loc[i,'tpep_dropoff_datetime'] + 25)
        riders.append(rider)

def init_states():
    dict = {}
    global state
    for i in range(60 * 24):
        dict[i] = {}
        for j in range(1, 30 + 1):
            dict[i][j] = []
    for i in range(len(riders)):
        if riders[i].flag == 1:
            continue
        dict[riders[i].appear_slot][riders[i].from_node].append(riders[i].r_id)
    state = util.State(dict)

def init_param():
    init_instances()
    init_request()
    init_states()
    global floyd_path
    floyd_path = gen_map.set_Floyd_Path()
    cp.cal_P_i(r'data\self_gen_riders.csv')

# if __name__ == '__main__':
#     init_param()
#     print(floyd_path(1,5))
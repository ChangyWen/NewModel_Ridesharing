
class vertex(object):
    def __init__(self, v_id: int, x, y):
        self.v_id = v_id
        self.x_coor = x
        self.y_coor = y


class Rider(object):
    def __init__(self, r_id, ori, des, appear_time, deadline, delay_t):
        self.r_id = r_id
        self.ori = ori
        self.des = des
        self.pu_t = 0
        self.deadline = deadline
        self.delay_t = delay_t
        self.appear_time = appear_time
        self.flag = 0

class Vehicle(object):
    def __init__(self):
        self.v_id
        self.location
        self.cap
        self.load
        self.pickup_list = []
        self.route = []
        self.violation_time = 0

    def update(self):
        '''
        update pickup_list
        update load
        update route
        update violation_time
        :return:
        '''
        print()

class State(object):
    def __init__(self, current_time: int, vehicles: list, riders: list):
        self.current_time = current_time
        #self.p_i = p_i
        self.vehicles = vehicles
        self.riders = riders

    def update(self):
        '''
        update vehicles
        update riders
        :return:list
        '''
        print()

average_speed = 1

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

class Floyd_Path():
    def __init__(self, node , node_map, path_map):
        self.node = node
        self.node_map = node_map
        self.path_map = path_map
        self.node_length = len(node_map)
        self._init_Floyd()

    def __call__(self, from_node, to_node):
        self.from_node = from_node - 1
        self.to_node = to_node - 1
        return self._format_path(), self.node_map[from_node - 1][to_node - 1]

    def _init_Floyd(self):
        for k in range(self.node_length):
            for i in range(self.node_length):
                for j in range(self.node_length):
                    tmp = self.node_map[i][k] + self.node_map[k][j]
                    if self.node_map[i][j] > tmp:
                        self.node_map[i][j] = tmp
                        self.path_map[i][j] = self.path_map[i][k]

    def _format_path(self):
        node_list = []
        temp_node = self.from_node
        obj_node = self.to_node
        node_list.append(self.node[temp_node])
        while True:
            node_list.append(self.node[self.path_map[temp_node][obj_node]])
            temp_node = self.path_map[temp_node][obj_node]
            if temp_node == obj_node:
                break
        return node_list


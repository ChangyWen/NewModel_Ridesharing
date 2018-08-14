import gen_map
from init_instances import *
average_speed = 1


class vertex(object):
    def __init__(self, v_id: int, x, y):
        self.v_id = v_id
        self.x_coor = x
        self.y_coor = y


class Rider(object):
    def __init__(self, r_id, from_node: int, to_node: int, appear_time: int, deadline: int):
        self.r_id = r_id
        self.from_node = from_node
        self.to_node = to_node
        self.pu_t = 0
        self.deadline = deadline
        self.delay_t = 0
        self.appear_time = appear_time
        self.flag = 0

class Vehicle(object):
    def __init__(self, v_id, location: int, slot: int, first_rider: int):
        self.v_id = v_id
        self.location = location
        self.slot = slot
        self.cap = 3
        self.load = 0
        self.picked_up = [first_rider]
        self.pre_pickup = []
        self.route = []
        self.violation_time = 0

    def insert_rider(self, rider: int, index: int = -1):
        if index == -1:
            self.picked_up.append(rider)
        else:
            self.picked_up.insert(index, rider)

    def insert_pre_pickup(self, loc: int, index: int = -1):
        if index == -1:
            self.pre_pickup.append(loc)
        else:
            self.pre_pickup.insert(index, loc)

    def update(self):
        self.route = []
        if len(self.picked_up) > 1:
            for i in range(len(self.picked_up) - 1):
                from_node = riders[self.picked_up[i]].from_node
                to_node = riders[self.picked_up[i + 1]].to_node
                self.route += gen_map.floyd_path(from_node, to_node)[0]
        if len(self.pre_pickup) > 0:
            from_node = riders[self.picked_up[-1]].from_node
            to_node = self.pre_pickup[0]
            self.route += gen_map.floyd_path(from_node, to_node)
        if len(self.pre_pickup) > 1:
            for i in range(len(self.pre_pickup) - 1):
                from_node = self.pre_pickup[i]
                to_node = self.pre_pickup[i + 1]
                self.route += gen_map.floyd_path(from_node, to_node)[0]

        '''
        clean route
        '''
        temp_route = self.route.copy()
        n = 0
        nums = len(self.route) - 1
        for i in range(nums):
            if temp_route[i] == temp_route[i+1]:
                self.route.pop(i - n)
                n += 1
        ''''''
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


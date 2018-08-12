from util import Floyd_Path
from numpy import np

node = ['node_a','node_b']
node_list = [('node_a','node_b',1)]

def set_map(node_map, node, node_list, path_map) -> (np.array,np.array()):
    '''
    :param node_map:
    :param node:
    :param node_list:
    :param path_map:
    :return:
    '''
    for i in range(len(node)):
        node_map[i][i] = 0
    for x,y,val in node_list:
        node_map[node.index(x)][node.index(y)] = node_map[node.index(y)][node.index(x)] = val
        path_map[node.index(x)][node.index(y)] = node.index(y)
        path_map[node.index(y)][node.index(x)] = node.index(x)
    return node_map, path_map
from itertools import permutations
import pandas as pd
from math import floor


def get_container_params(x: float, y: float, z: float):
    return({
        'x1': 0,
        'x2': x,
        'y1': 0,
        'y2': y,
        'z1': 0,
        'z2': z
    })

def get_auxiliary_box_params():
    return {

    }

def select_space(space_list: list):
    return max(space_list, key=lambda x: x.y1)


def max_items_left(item_list: list):
    return len(max(item_list, key=lambda x: len(x)))


def calculate_fits(space, bx, ax, num_items):

    ax_dist = {}
    missing_axis = ''.join(list(set(['x', 'y', 'z'])-set(ax)))

    ax_dist[ax[0]] = min([floor(space.params.get(ax[0]) / bx.params.get(ax[0])), num_items])
    ax_dist[ax[1]] = min([floor(space.params.get(ax[1]) / bx.params.get(ax[1])), num_items / ax_dist[ax[0]]]) \
                       if ax_dist[ax[0]] > 0 else 0
    ax_dist[missing_axis] = 1

    depth_fit = space.params.get('x') - (bx.params.get('x') * ax_dist['x'])
    height_fit = space.params.get('y') - (bx.params.get('y') * ax_dist['y'])
    length_fit = space.params.get('z') - (bx.params.get('z') * ax_dist['z'])

    max_items_in_axis = depth_fit + height_fit + length_fit \
                        if min([depth_fit, height_fit, length_fit]) > 0 else 99999999

    fit = ax_dist[ax[0]] * ax_dist[ax[1]]

    return {
            'max_items': max_items_in_axis,
            'fit': fit,
            'x_axis': ax_dist['x'],
            'y_axis': ax_dist['y'],
            'z_axis': ax_dist['z']
    }

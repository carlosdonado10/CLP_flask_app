from itertools import permutations
import pandas as pd
from math import floor
from application.Utils.CLP_Algorithm.classes import Space


def reset_counters():

    return {
            'xy': {
                'x': 0,
                'y': 0
            },
            'xz': {
                'x': 0,
                'z': 0
            },
            'yx': {
                'y': 0,
                'x': 0
            },
            'yz': {
                'y': 0,
                'z': 0
            },
            'zx': {
                'z': 0,
                'x': 0
            },
            'zy': {
                'z': 0,
                'y': 0
            }
            }


def get_container_params(x: float, y: float, z: float):
    return({
        'x1': 0,
        'x2': x,
        'y1': 0,
        'y2': y,
        'z1': 0,
        'z2': z
    })


def get_box_coords(space, box, counter, ax):
    x1 = space.x1 if ax != 'zy' else 0
    x1 += counter[ax]['x'] if 'x' in ax else 0

    y1 = space.y2 if 'y' in ax else space.y
    y1 -= counter[ax]['y'] if 'y' in ax else 0
    y1 -= box.y

    z1 = space.z1
    z1 += counter[ax]['z'] if 'z' in ax else 0

    return ({
        'x1': x1,
        'y1': y1,
        'z1': z1,
        'x2': x1 + box.x,
        'y2': y1 + box.y,
        'z2': z1 + box.z,
        'x': box.x,
        'y': box.y,
        'z': box.z,
        'id': box.id
    })


def get_auxiliary_box_params(box_list, auxiliary_box=None):
    resp = {}
    resp['id'] = 'auxiliary box'
    resp['x1'] = min([min(box_list, key=lambda x: x.x1).x1[0], auxiliary_box.x1[0] if auxiliary_box is not None else 1e9])
    resp['y1'] = min([min(box_list, key=lambda x: x.y1).y1[0], auxiliary_box.y1[0] if auxiliary_box is not None else 1e9])
    resp['z1'] = min([min(box_list, key=lambda x: x.z1).z1[0], auxiliary_box.z1[0] if auxiliary_box is not None else 1e9])
    resp['x2'] = max([max(box_list, key=lambda x: x.x2).x2[0], auxiliary_box.x2[0] if auxiliary_box is not None else 0])
    resp['y2'] = max([max(box_list, key=lambda x: x.y2).y2[0], auxiliary_box.y2[0] if auxiliary_box is not None else 0])
    resp['z2'] = max([max(box_list, key=lambda x: x.z2).z2[0], auxiliary_box.z2[0] if auxiliary_box is not None else 0])
    resp['x'] = abs(resp['x2'] - resp['x1'])
    resp['y'] = abs(resp['y2'] - resp['y1'])
    resp['z'] = abs(resp['z2'] - resp['z1'])

    return resp


def select_space(space_list: list):
    return max(space_list, key=lambda x: x.y2)


def max_items_left(item_list: list):
    return len(max(item_list, key=lambda x: len(x)))


def calculate_fits(space, bx, ax, num_items):
    rotation_fits = []
    ax_dist = {}
    cond = True
    while bx.rotate():
        missing_axis = ''.join(list(set(['x', 'y', 'z'])-set(ax)))

        ax_dist[ax[0]] = min([floor(space.params.get(ax[0]) / bx.params.get(ax[0])), num_items])
        ax_dist[ax[1]] = min([floor(space.params.get(ax[1]) / bx.params.get(ax[1])), floor(num_items / ax_dist[ax[0]])]) \
                        if ax_dist[ax[0]] > 0 else 0
        ax_dist[missing_axis] = 1

        depth_fit = space.params.get('x') - (bx.params.get('x') * ax_dist['x'])
        height_fit = space.params.get('y') - (bx.params.get('y') * ax_dist['y'])
        length_fit = space.params.get('z') - (bx.params.get('z') * ax_dist['z'])

        max_items_in_axis = ax_dist[ax[0]] * ax_dist[ax[1]]

        fit = depth_fit + height_fit + length_fit \
            if min([depth_fit, height_fit, length_fit]) >= 0 and max_items_in_axis > 0 else 1e9

        rotation_fits.append({
            'max_items': max_items_in_axis,
            'fit': fit,
            'ax_dist': ax_dist,
            'rotation': bx.cur_rot
    })



    return rotation_fits


# TODO: Esta función está horrible
def generate_spaces(space, auxiliary_box, num_iter):
    space_list = []
    params = {}
    if auxiliary_box.y1[0] >= space.y1:
        params.update({'id': f'{num_iter}a'})
        params.update({'x1': space.x1})
        params.update({'x2': space.x2})
        params.update({'y1': space.y1})
        params.update({'y2': auxiliary_box.y1[0]})
        params.update({'z1': space.z1})
        params.update({'z2': space.z2})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})

        space_list.append(Space(**params))

    if auxiliary_box.x2[0] <= space.x2:
        params.update({'id': f'{num_iter}b'})
        params.update({'x1': auxiliary_box.x2[0]})
        params.update({'x2': space.x2})
        params.update({'y1': space.y1})
        params.update({'y2': space.y2})
        params.update({'z1': space.z1})
        params.update({'z2': space.z2})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})

        space_list.append(Space(**params))

    if auxiliary_box.z2[0] <= space.z2:
        params.update({'id': f'{num_iter}c'})
        params.update({'x1': auxiliary_box.x1[0]})
        params.update({'x2': auxiliary_box.x2[0]})
        params.update({'y1': auxiliary_box.y1[0]})
        params.update({'y2': auxiliary_box.y2[0]})
        params.update({'z1': auxiliary_box.z2[0]})
        params.update({'z2': space.z2})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})

        space_list.append(Space(**params))

    if auxiliary_box.y2[0] <= space.y2:
        params.update({'id': f'{num_iter}d'})
        params.update({'x1': space.x1})
        params.update({'x2': space.x2})
        params.update({'y1': auxiliary_box.y2[0]})
        params.update({'y2': space.y2})
        params.update({'z1': space.z1})
        params.update({'z2': space.z2})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})

        space_list.append(Space(**params))

    if auxiliary_box.x1[0] >= space.x1:
        params.update({'id': f'{num_iter}e'})
        params.update({'x1': space.x1})
        params.update({'x2': auxiliary_box.x1[0]})
        params.update({'y1': space.y2})
        params.update({'y2': space.y2})
        params.update({'z1': space.z1})
        params.update({'z2': space.z2})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})
        space_list.append(Space(**params))

    if auxiliary_box.z1[0] >= space.z1:
        params.update({'id': f'{num_iter}f'})
        params.update({'x1': auxiliary_box.x1[0]})
        params.update({'x2': auxiliary_box.x2[0]})
        params.update({'y1': auxiliary_box.y1[0]})
        params.update({'y2': auxiliary_box.y1[0]})
        params.update({'z1': space.z1})
        params.update({'z2': auxiliary_box.z1[0]})
        params.update({'x': abs(params['x2'] - params['x1'])})
        params.update({'y': abs(params['y2'] - params['y1'])})
        params.update({'z': abs(params['z2'] - params['z1'])})

        space_list.append(Space(**params))

    return space_list


def update_spaces(space_list, auxiliary_box, item_list, num_iter):
    pop_list = []
    space_list_copy = space_list.copy()
    for idx, sp in enumerate(space_list_copy):
        if auxiliary_box.is_in_space(sp):
            sp_list = generate_spaces(sp, auxiliary_box, num_iter)
            for new_space in sp_list:
                if new_space.a_box_fits(item_list):
                    space_list.append(new_space)
            pop_list.append(idx)


        elif not sp.a_box_fits(item_list):
            pop_list.append(idx)

        print(idx)
    sp_list = [sp for idx, sp in enumerate(space_list) if idx not in pop_list]
    return sp_list

def allocated_by_type(allocated_list):
    alloc = {}
    for bx in allocated_list:
        alloc[bx.type]+=1
    return alloc

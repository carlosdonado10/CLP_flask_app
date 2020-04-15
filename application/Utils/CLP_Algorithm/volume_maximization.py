from itertools import permutations

from application.Utils.CLP_Algorithm.classes import Box, Space, AllocatedBox
from application.Utils.CLP_Algorithm.clp_utils import get_container_params, max_items_left, select_space, calculate_fits, \
    get_auxiliary_box_params, reset_counters, get_box_coords, update_spaces, allocated_by_type
from json import dumps
#TODO: Enviar cosas a clp_utils y convertir en una clase

problem_params = [
    {
        'num_items': 100,
        'x': 50,
        'y': 30,
        'z': 60
    },
    {
        'num_items': 100,
        'x': 40,
        'y': 50,
        'z': 30
    },
    {
        'num_items': 100,
        'x': 90,
        'y': 40,
        'z': 50
    },
    {
        'num_items': 100,
        'x': 30,
        'y': 80,
        'z': 20
    }
]
container_params = get_container_params(233, 587, 220)


def volume_maximization(problem_params, container_params):
    space_list = []
    item_list = []
    allocated_list = []
    container = Space('container', **container_params)
    space_list.append(container)
    auxiliary_container = None
    id_ = 0
    for idx,i in enumerate(problem_params):
        lista = []
        for j in range(i.get('num_items')):
            id_ += 1
            i.update({'id': id_,
                      'type': idx})
            lista.append(Box(**i))
        item_list.append(lista)

    num_iter = 0
    while max_items_left(item_list) > 0 and len(space_list) > 0:
        num_iter += 1
        selected_space = select_space(space_list)
        allocated_volume = 0

        for idx, itm in enumerate(item_list):
            results = {}
            if len(itm) == 0:
                continue

            dimensions = ['x', 'y', 'z']
            for ax in list(permutations(dimensions, 2)):
                missing_axis = ''.join(set(dimensions) - set(ax))
                results.update({''.join(ax): calculate_fits(selected_space, itm[0], ax, len(itm))})

            mejorFit = 1e9
            mayor_cantidad = 0
            for key in results.keys():
                if results[key]['fit'] < mejorFit and results[key]['max_items'] >= mayor_cantidad:
                    best_choice_local = results[key]
                    best_choice_local.update({'chosen_ax': key})
                    mayor_cantidad = results[key]['max_items']
                    mejorFit = results[key]['fit']

            if mayor_cantidad * itm[0].volume > allocated_volume:
                best_choice = best_choice_local
                tipo_elegido = idx
                allocated_volume = mayor_cantidad * itm[0].volume

        counters = reset_counters()
        temp_allocated_list = []
        remove_boxes = []
        ax = ''.join(best_choice['chosen_ax'])
        for idx, bx in enumerate(item_list[tipo_elegido]):
            if idx >= best_choice['max_items']:
                break
            al_params = get_box_coords(selected_space, item_list[tipo_elegido][idx], counters, ax)
            al_params.update({'type': bx.type,
                              'num_iter': num_iter})
            al_bx = AllocatedBox(**al_params)
            allocated_list.append(al_bx)
            temp_allocated_list.append(al_bx)
            remove_boxes.append(bx)

            if (idx + 1) % best_choice['ax_dist'][ax[:1]] == 0:
                counters[ax][ax[-1:]] += bx.params.get(ax[1:])
                counters[ax][ax[:1]] = 0
            else:
                counters[ax][ax[:1]] += bx.params.get(ax[:-1])
        print('//------------------------------------------//-----------------------------------------------//')
        print(f"Iteration: {num_iter} \nmax items: {best_choice['max_items']}\ntipo_elegido: {tipo_elegido}\nEspacio: {selected_space}")
        item_list[tipo_elegido] = list(set(item_list[tipo_elegido]) - set(remove_boxes))
        auxiliary_params = get_auxiliary_box_params(temp_allocated_list, None)
        auxiliary_container = AllocatedBox(**auxiliary_params)
        allocated_list.append(auxiliary_container)

        space_list = update_spaces(space_list, auxiliary_container, item_list, num_iter)
        space_list = sorted(space_list, key=lambda x: x.id, reverse=False)
        print('iter done')
    allocated_list_dict = [i.params for i in allocated_list if i.id != 'auxiliary box']

    utilization = sum(map(lambda x: x.volume if x.id != 'auxiliary box' else 0, allocated_list))/container.volume

    cord = []
    for bx in allocated_list:
        cord.append([bx.id, bx.x1, bx.x2, bx.y1, bx.y2, bx.z1, bx.z2])

    return allocated_list, utilization, dumps(container.params), dumps(allocated_list_dict)

# al,_,_,_ = volume_maximization(problem_params, container_params)

# allocated_by_type(al)
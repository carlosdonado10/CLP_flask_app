from app.Utils.CLP_Algorithm.classes import Box, Space, AllocatedBox
from app.Utils.CLP_Algorithm.clp_utils import get_container_params, max_items_left, select_space, calculate_fits
import pandas as pd
from itertools import permutations
from math import floor
## Inicializar Algorítmos
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
espacios = []
item_list = []

container_params = get_container_params(233, 587, 220)
container = Space('container', **container_params)

espacios.append(container)

id_ = 0
for i in problem_params:
    lista = []
    for j in range(i.get('num_items')):
        id_ += 1
        i.update({'id': id_})
        lista.append(Box(**i))
    item_list.append(lista)

while max_items_left(item_list) > 0 and len(espacios):
    selected_space = select_space(espacios)
    allocated_volume = 0

    for idx, i in enumerate(item_list):
        results = {}
        if len(i) > 0:
            dimensions = ['x', 'y', 'z']
            for ax in list(permutations(dimensions, 2)):
                missing_axis = ''.join(set(dimensions) - set(ax))
                results.update({''.join(ax): calculate_fits(selected_space, i[0], ax, len(i))})

        mejorFit = 1e9
        mayor_cantidad = 0
        for key in results.keys():
            if results[key]['fit'] < mejorFit and results[key]['max_items'] >= mayor_cantidad:
                best_choice = results[key]

        if mayor_cantidad * i[0].volume > allocated_volume:
            tipo_elegido = idx
            allocated_volume = mayor_cantidad * i[0].volume

    auxiliary_container = AllocatedBox()

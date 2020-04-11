from json import dumps
# TODO: Incluir visualizaciones en las clases
# TODO: Crear clases para las listas ¿que contienen métodos de visualización?
class Box(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')
        self.volume = self.x*self.y*self.z
        self.params = {
            'id': kwargs.get('id'),
            'type': kwargs.get('type'),
            'x': kwargs.get('x'),
            'y': kwargs.get('y'),
            'z': kwargs.get('z')
        }

    def __repr__(self):
        return f"""box : {self.id}"""


class AllocatedBox(Box):
    def __init__(self, **kwargs):
        self.x2 = kwargs.get('x2'),
        self.y1 = kwargs.get('y1'),
        self.y2 = kwargs.get('y2'),
        self.x1 = kwargs.get('x1'),
        self.z1 = kwargs.get('z1'),
        self.z2 = kwargs.get('z2'),
        self.iteration = kwargs.get('num_iter')
        Box.__init__(self, **kwargs)

    def is_in_space(self, space):
        return not (space.x1 >= self.x2[0] or space.x2 <= self.x1[0] or space.y1 >= self.y2[0] or space.y2 <= self.y1[0] or \
               space.z1 >= self.z2[0] or space.z2 <= self.z1[0])

    def __repr__(self):
        return dumps({
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "x1": self.x1[0],
            "y1": self.y1[0],
            "z1": self.z1[0],
            'iteration': self.iteration
        })

class Space(object):
    def __init__(self, item_id="", **kwargs):
        self.id = item_id if len(item_id) > 0 else kwargs.get('id')
        self.x1, self.x2, self.y1, self.y2, self.z1, self.z2 = tuple((kwargs.get('x1'), kwargs.get('x2'), kwargs.get('y1'), kwargs.get('y2'), kwargs.get('z1'), kwargs.get('z2')))
        self.x = abs(self.x1-self.x2)
        self.y = abs(self.y1-self.y2)
        self.z = abs(self.z1-self.z2)
        self.volume = self.x*self.y*self.z
        self.params = {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    def __repr__(self):
        return f"""space:{self.id}"""

    def a_box_fits(self, item_list):
        for itms in item_list:
            if len(itms) > 0:
                if (itms[0].x <= self.x and itms[0].y <= self.y and itms[0].z <= self.z):
                    return True
        return False

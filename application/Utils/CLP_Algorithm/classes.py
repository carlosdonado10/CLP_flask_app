from json import dumps
from itertools import permutations

rotations = list()

class Box(object):
    def __init__(self, **kwargs):

        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')
        self.original_dims = (self.x, self.y, self.z)
        self.rotations = permutations(['x', 'y', 'z'],3)
        self.cur_rot = tuple()
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

    def rotate(self):
        try:
            rot = self.rotations.__next__()
            self.x = getattr(self, rot[0])
            self.y = getattr(self, rot[1])
            self.z = getattr(self, rot[2])
            self.cur_rot = rot
            return True
        except:
            self.rotations = permutations(['x', 'y', 'z'],3)
            return False

    def undo_rotations(self):
        self.x = self.original_dims[0]
        self.y = self.original_dims[1]
        self.z = self.original_dims[2]

    def rotate_to(self, orientation:tuple):
        self.x = getattr(self, orientation[0])
        self.y = getattr(self, orientation[1])
        self.z = getattr(self, orientation[2])


class AllocatedBox(Box):
    def __init__(self, **kwargs):
        Box.__init__(self, **kwargs)
        self.x2 = kwargs.get('x2'),
        self.y1 = kwargs.get('y1'),
        self.y2 = kwargs.get('y2'),
        self.x1 = kwargs.get('x1'),
        self.z1 = kwargs.get('z1'),
        self.z2 = kwargs.get('z2'),
        self.iteration = kwargs.get('num_iter')
        self.params.update({
            'x1': self.x1[0],
            'x2': self.x2[0],
            'y1': self.y1[0],
            'y2': self.y2[0],
            'z1': self.z1[0],
            'z2': self.z2[0],
            'volume': self.volume,
            'iteration': self.iteration
        })



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
            'volume': self.volume,
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
            'z': self.z,
            'volume': self.volume
        }

    def __repr__(self):
        return f"""space:{self.id}"""

    def a_box_fits(self, item_list):
        for itms in item_list:
            if len(itms) > 0:
                if (itms[0].x <= self.x and itms[0].y <= self.y and itms[0].z <= self.z):
                    return True
        return False


class Box:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')
        self.volume = self.x*self.y*self.z
        self.params = {
            'x': kwargs.get('x'),
            'y': kwargs.get('y'),
            'z': kwargs.get('z')
        }

    def __repr__(self):
        return f"""box : {self.id}"""


class AllocatedBox(Box):
    def __init__(self, kwargs):
        Box.__init__(**kwargs)
        self.x1, self.x2, self.y1, self.y2, self.z1, self.z2 = kwargs.get('coord_tuple')


class Space(object):
    def __init__(self, item_id, **kwargs):
        self.id = item_id
        self.x1, self.x2, self.y1, self.y2, self.z1, self.z2 = tuple((kwargs.get('x1'), kwargs.get('x2'), kwargs.get('y1'), kwargs.get('y2'), kwargs.get('z1'), kwargs.get('z2')))
        self.x = abs(self.x1-self.x2)
        self.y = abs(self.y1-self.y2)
        self.z = abs(self.z1-self.z2)
        self.params = {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    def __repr__(self):
        return f"""space : {self.id}"""

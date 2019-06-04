import hdf5plugin
import h5py
import numpy as np

class AlembicReader():
    def __init__(self,input_dir,time_step):
        self.input_dir = input_dir
        self.time_step = time_step

    def alembic_reader(self):
        errors = []
        points = []
        _min_curve, _max_curve = self.get_curve_count()
        with h5py.File(self.input_dir,'r') as f:
            for p in [f'ABC/hairSystem1OutputCurves/curve{i}/curveShape{i}/.prop/.geom/P.smpi/{self.time_step:04}' for i in range(_min_curve,_max_curve)]:
                try:
                    points.append(f[p].value)        
                except KeyError as e:
                    errors.append(e)
            if errors == []:
                return points, "ok"
            else:
                return [], errors

    def get_curve_count(self):
        key = []
        with h5py.File(self.input_dir,'r') as f:
            for k in f['ABC/hairSystem1OutputCurves'].keys():
                if k == '.prop':
                    pass
                else:
                    key.append(int(k.strip('curve')))
        return min(key), max(key)
    
    def get_bounding_volume(self):
        errors = []
        with h5py.File(self.input_dir,'r') as f:
            try:
                self._child_bnds = dict(f['ABC/.prop/.childBnds.smpi'].attrs.items())
            except KeyError as e:
                errors.append(e)
            if errors == []:
                return self._child_bnds[f'{self.time_step:04}'], "ok"
            else:
                return [], errors      

def main():
    ar = AlembicReader('../data/30000abc.abc',1)
    print(ar.alembic_reader())

if __name__ == "__main__":
    main()
import AlembicReader as ar
import SplineToPoints as sp
import Octree as oc
import GetDistance as gd
import numpy as np
import pandas as pd
import csv

def main():
    '''
    a, 読み込み
    b, 点群に変換
    c, 八分木に格納
    d, それぞれの空間に含まれる点間の距離を求める．
    '''
    hdfpath = '../data/sample_hdf5.abc'
    output = "../output/sample_hdf5.csv"
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['timestep','collision'])
        for t in range(1,120):
            abc = ar.AlembicReader(hdfpath,t)
            pos,ok = abc.alembic_reader()
            if ok != 'ok':
                print(ok)
                print ('Error: Cannot read file.')
                break
            bnds,ok = abc.get_bounding_volume()
            if ok != 'ok':
                print(ok)
                print ('Error: Cannot read file.')
                break       

            spl = sp.SplineToPoints(pos)
            points = spl.spline_to_points()

            _oct = oc.Octree(points,bnds)
            tree = _oct.output()

            dis = gd.GetDistance(tree,points,0.1)
            collision = dis.get_collison_count()

            print (t,collision)
            writer.writerow([t,collision])

    

if __name__ == '__main__':
    main()

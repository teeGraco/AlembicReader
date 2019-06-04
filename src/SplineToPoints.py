# for test
import hdf5plugin
import h5py
# 3次のBSpline関数
from scipy.interpolate import splprep,splev
import numpy as np
# 描画関数(draw)用に定義
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SplineToPoints():
    # 入力は3*10の制御点をndarray化したものをspline数だけリスト化したlist object.
    def __init__(self,li,points=50):
        self.points_positions = li
        self.points = points
        self.sp_points = []
        
    # 入力の制御点から，3次のBSpline曲線を構築し，その上の50点をpickupする関数．
    def spline_to_points(self):
        for arr in self.points_positions:
            point = np.reshape(arr,(3,10),order='F')
            okay = np.where(np.abs(np.diff(point[0])) + np.abs(np.diff(point[1])) + np.abs(np.diff(point[2])) > 0)
            pointf = [np.r_[point[0][okay], point[0][-1]],np.r_[point[1][okay], point[1][-1]],np.r_[point[2][okay], point[2][-1]]]
            # 同じ制御点がある場合は情報を排除せねばならない．
            print(pointf)
            tck,u = splprep(pointf,k=3,quiet=1)
            params = np.linspace(u[0], u[-1], num=self.points, endpoint=True)
            # 出力は，values[0] -> x, values[1] -> y, values[2] -> zが格納されている．
            values = splev(params, tck)
            self.sp_points.append(values)
        return self.sp_points
    
    # 表示用の関数
    def draw(self, num=0):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(xs=self.sp_points[num][0], ys=self.sp_points[num][1], zs=self.sp_points[num][2],
                color='deeppink', label='cubic spline')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.legend()
        plt.show()
    
def main():
    arr = []
    with h5py.File('../data/30000abc.abc','r') as f:
        arr.append(f['ABC/hairSystem1OutputCurves/curve32333/curveShape32333/.prop/.geom/P.smpi/0030'].value)
    sp = SplineToPoints(arr)
    sp.spline_to_points()
    sp.draw()

if __name__ == '__main__':
    main()

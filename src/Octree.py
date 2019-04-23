'''
x,y,z方向全てにbinary treeを構成する．
そのアドレスを最下層のノードにオブジェクトとして持たせたい．

近傍探索をラクにするために，モートンオーダーを利用する．

オブジェクトをどうやって定義するかという問題があって，
第m番splineの第nポイントというのを，(m,n)のtupleで持たせても良いかもしれない．

今回，八分木で必要な要件は，
① 構築(挿入)
② 探索
だけで，削除・更新は要件に含まれない．
強いて言えば，全削除はメモリ領域の解放のために必要かもしれない．

depthとデータセットを与えることで，
a,"該当のノードに当てはめるべきオブジェクトが存在しない"
b,"depthの最下層までたどり着いた"
のどちらかになるまで，全てのオブジェクトを導入していく．

Bounding Volumeを有効活用する．
'''
class Octree():
    def __init__(self,_point_set,_bnds_volume,depth=3):
        self.depth = depth
        self._point_set = _point_set
        self._bnds_volume = _bnds_volume
        self._tree = {}
    
    def get_morton_order(self,points,basis,bit=0,depth=0):
        if depth > self.depth:
            return bit

        else:
            depth += 1
            bit = bit << 3
            x,y,z = points
            bx,by,bz = basis

            if x < bx:
                bx = bx / 2
            else:
                bx = bx * 3 / 2
                bit += 4

            if y < by:
                by = by / 2
            else:
                by = by * 3 / 2
                bit += 2

            if z < bz:
                bz = bz / 2
            else:
                bz = bz * 3 / 2
                bit += 1

            return self.get_morton_order(points,(bx,by,bz),bit,depth)

    
    def develop_tree(self):
        for m, points in enumerate(self._point_set):
            for n, (x, y, z) in enumerate(zip(points[0],points[1],points[2])):
                bx = (self._bnds_volume[3] + self._bnds_volume[0]) / 2
                by = (self._bnds_volume[4] + self._bnds_volume[1]) / 2
                bz = (self._bnds_volume[5] + self._bnds_volume[2]) / 2
                bit = self.get_morton_order((x,y,z),(bx,by,bz))
                if bit in self._tree:
                    self._tree[bit].append((m,n))
                else:
                    self._tree[bit] = [(m,n)]
    
    def output(self):
        self.develop_tree()
        return self._tree
    
    def print_all(self):
        print (self.depth)
        print (self._bnds_volume)
        print (self._point_set)
        print (self._tree)

def main():
    points = [[[0,2,3,2,3,4,3,2,1],[3,4,2,5,3,4,6,1,5],[0,4,3,6,4,2,1,5,6]],[[1,2,3,4,5,6,7,8,9],[2,4,6,8,1,3,5,7,9],[3,6,9,1,4,7,2,5,9]]]
    bounds = [0,0,0,9,9,9]

    oc = Octree(points,bounds,1)

    oc.develop_tree()
    oc.print_all()

if __name__ == '__main__':
    main()
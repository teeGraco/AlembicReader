import numpy as np
import pandas as pd

class GetDistance():
    def __init__(self,dic,points,delta):
        self._tree = dic
        self._points = points
        self.delta = delta
        self.collision = set()

    def get_collision_set(self):
        for _,v in self._tree.items():
            if len(v) <= 1:
                pass

            else:
                _arr = []
                d = {}
                
                # 1st ... valueから点の取得
                # 2nd ... [x,y,z]を1レコードとするpandas Dataframeに書き込み
                # 3rd ... カーネルを用いた距離計算をする．
                # 4th ... 距離がある値よりも小さくなっているレコードのm値をsetに組み込み

                for k,(m,n) in enumerate(v):
                    _arr.append([self._points[m][0][n],self._points[m][1][n],self._points[m][2][n]])
                    d[k] = m

                # 要素間の距離を算出
                nparr = np.array(_arr)
                all_diffs = np.expand_dims(nparr, axis=1) - np.expand_dims(nparr, axis=0)
                _distance = np.sqrt(np.sum(all_diffs ** 2, axis=-1))
	
                # Dataframe型に変更して，deltaよりも距離が小さい部分を抽出
                df = pd.DataFrame(_distance)
                stacked_df = df.stack()
                res = list(stacked_df[stacked_df < self.delta].index)

                for (i,j) in zip(res[0],res[1]):
                    if i >= j:
                        # i > jとi < jは対称性から同じなので省略，i = jは当然距離がないので省略
                        pass
                    else:
                        if d[i] != d[j]:
                            self.collision.add((min(d[i],d[j]),max(d[i],d[j])))
                        else:
                            pass
        return self.collision
    
    def get_collison_count(self):
        self.get_collision_set()
        return len(self.collision)

def main():
    print ("This class is to detect collision between splines.")


if __name__ == "__main__":
    main()



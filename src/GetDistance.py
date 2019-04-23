class GetDistance():
    def __init__(self,dic,points):
        self._tree = dic
        self._points = points
    
    def collision_detection(self):
        count = 0
        for k,v in self._tree.items():
            if len(v) <= 1:
                pass
            else:
                # 1st ... valueから点の取得
                # 2nd ... [x,y,z]を1レコードとするpandas Dataframeに書き込み
                # 3rd ... カーネルを用いた距離計算をする．
                # 4th ... 距離がある値よりも小さくなっているレコードのカウントを実施する．
                pass
        return count
    

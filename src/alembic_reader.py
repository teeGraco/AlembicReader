import hdf5plugin
import h5py
import pandas as pd
import numpy as np

hdfpath = '../data/sample_hdf5.abc'

wpath = '../data/positions.csv'

dif_file = '../data/diff3.csv'

def PrintOnlyDataset(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(name)
        print(obj.value)


counter = 0
errors = []


idx = ['curve','timestep']
for i in range(10):
    idx.append('x' + str(i))
    idx.append('y' + str(i))
    idx.append('z' + str(i))

print (idx)

df = pd.DataFrame(columns=idx)

## Fileの存在チェック
'''
with h5py.File(hdfpath,'r') as f:
    for p in [f'ABC/hairSystem1OutputCurves/curve{i}/curveShape{i}/.prop/.geom/P.smpi/{j:04}' for i in range(245,489) for j in range(1,120)]:
        try:
            f[p]           
        except KeyError as e:
            counter += 1
            errors.append(e)
            print(e)

if counter == 0:
    print('Every files found.')
else:
    print('Some Error Occered.')
    print (errors)
''' 

# Fileの書き込み
if len(errors) == 0:
    print('File Write Start................')
    with open(wpath, mode='w') as fw:
        with h5py.File(hdfpath,'r') as f:
            for i in range(245,489):
                for j in range(1,120):
                    try:
                        li = [i, j]
                        li = li + f['ABC/hairSystem1OutputCurves/curve{0}/curveShape{0}/.prop/.geom/P.smpi/{1}'.format(i,'{:04}'.format(j))].value.tolist()
                        df = df.append(pd.Series(li, index = idx),ignore_index=True)
                    except KeyError as e:
                        print(e)

# df.astype({'curve':int, 'timestep':int}).to_csv(wpath)

df1 = df[df.timestep == 3]
df2 = df1.loc[:,['x0','y0','z0']]

# arr = df2.as_matrix()
arrv = df2.values()

# 距離演算
all_diffs = np.expand_dims(arrv, axis=1) - np.expand_dims(arrv, axis=0)
degree_distance = np.sqrt(np.sum(all_diffs ** 2, axis=-1))


print (np.amin(degree_distance))

with open(dif_file,mode='w') as f:
    np.savetxt(f,degree_distance,fmt='%.3e')

print ("DONE")





# 💪 Muscle-synergy ⚡

## 例

### 筋シナジーの計算
```py
import EMG
import numpy as np

filter_fs = (10, 15)
Es = EMG.p("/home/user/datas/EMG", *filter_fs)

C, W, vaf, vafm = EMG.calc_muscle_synergy(Es)
```

### 筋シナジーの表示
```py
EMG.plot_synergy(W)
```

### 筋シナジーの活動度表示
```py
EMG.plot_synergy_activities(C, ct=1.5)
```

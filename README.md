# 💪 Muscle-synergy ⚡

## For examples

```py
import EMG
import numpy as np

Es = EMG.p(EMG.get("/mnt/j/EMG"))

vaf = None
vafm = None

C, W = EMG.calc_muscle_synergy(Es, vaf, vafm)
```

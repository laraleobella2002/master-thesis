import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


path = "C:\\Users\\nawal\\Downloads\\data_1.csv"
df = pd.read_csv(path)

condition = "Monocular_C"
subset = df[df["block"] == condition]

plt.plot(subset["trial"], subset["offset"])
plt.xlabel("Trial")
plt.ylabel("Offset")
plt.title(condition)
plt.show()

reversals = []
last_diff = None

for i in range(1, len(offsets)):
    diff = offsets[i] - offsets[i-1]

    if last_diff is not None:
        if diff * last_diff < 0:
            reversals.append(offsets[i-1])

    if diff != 0:
        last_diff = diff

threshold = np.mean(reversals[-8:])
print(f"Estimated threshold for {condition}: {threshold}")

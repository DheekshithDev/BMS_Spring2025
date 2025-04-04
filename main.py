import numpy as np
import pandas as pd

# print([r := 10*x for x in np.arange(0, 1.25, 0.25)])


df = pd.read_csv("assets/simulation_results_m1.csv")
print(df.describe())
# print(df.head(50))

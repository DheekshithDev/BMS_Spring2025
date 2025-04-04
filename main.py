import numpy as np
import pandas as pd

# print([r := 10*x for x in np.arange(0, 1.25, 0.25)])


df = pd.read_csv("assets/simulation_results_M2.csv")
# print(df.describe())
print(df.loc[(df['k1'] == 200) & (df['k2'] == 5) & (df['top_X_percent'] == 0.07)])
# print(df)
# print(df.head(50))

import os
import sys
import math
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#formula: ma = F_d + F_r - T
#a: deceleration
#m: mass of car
#T: traction force, pushing car forward (0 in coastdown)
#F_d: aerodynamical drag, assume 0
#F_r: drivetrain resistance, variable to be tested

#revised formula: F_r = ma

#order:
#read csv file
#determine deceleration based on speed
#multiply by mass

#constants
mass = 100 #kg

#directory to access csv files from
directory = '.'

#column titles
time = 'time (seconds)'
a_f = 'accelerometer X (m/sec^2 highlighted)' #forward
a_v = 'accelerometer Y (m/sec^2 highlighted)' #vertical
a_l = 'accelerometer Z (m/sec^2 highlighted)' #lateral
v_f = 'v_forward'

csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and os.path.isfile(os.path.join(directory, f))]
calibration_files = [f for f in os.listdir(directory + '/calibration') if f.endswith('.csv') and os.path.isfile(os.path.join(directory + '/calibration', f))]

if not csv_files:
    print("No CSV files found in directory")
    sys.exit()

if calibration_files:
    print('calibration file(s) present')

first_csv_file = os.path.join(directory, csv_files[0])
df = pd.read_csv(first_csv_file)

# make columns numeric
df[time] = pd.to_numeric(df[time], errors='coerce')
df[a_f] = pd.to_numeric(df[a_f], errors='coerce')
df = df.dropna(subset=[time, a_f]).sort_values(time)

print(df.head())

# Finding velocity
dt = df[time].diff().fillna(0.0)
v0 = 0.0  # initial speed
df[v_f] = v0 + (df[a_f] * dt).cumsum()

# If positive X is forward and coastdown acceleration is negative, |F_r| = m*|a|
df['F_r (N)'] = -mass * (df[a_f])  # flip sign if your forward accel is negative during coastdown

print(df[[time, a_f, 'F_r (N)']].head())

plt.figure()
plt.plot(df[time], df[v_f])
plt.xlabel('time')
plt.ylabel('velocity')
plt.title('velocity / time')
plt.tight_layout()
plt.show()

plt.figure()
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
a_forward = 'accelerometer X (m/sec^2 highlighted)' #forward
a_vertical = 'accelerometer Y (m/sec^2 highlighted)' #vertical
a_lateral = 'accelerometer Z (m/sec^2 highlighted)' #lateral
v_forward = 'v_forward'
pitch_rad = 'pitch_rad'
pitch_deg = 'pitch_deg'

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
df[a_forward] = pd.to_numeric(df[a_forward], errors='coerce')
df = df.dropna(subset=[time, a_forward]).sort_values(time)

# account for gravity
g = 9.81

ratio = (-df[a_vertical] / g).clip(-1, 1)
df[pitch_rad] = np.arcsin(ratio) + (math.pi/2)
df[pitch_deg] = np.degrees(df[pitch_rad])

#df['pitch'] = math.acos(df[a_vertical]/g)

print(df.head())

# Finding velocity
df = df.dropna(subset=[time, a_forward]).sort_values(time)

dt = df[time].diff().fillna(0.0)
v0 = 0.0  # set your initial speed here
df[v_forward] = v0 + (df[a_forward] * dt).cumsum()

# If positive X is forward and coastdown acceleration is negative, |F_r| = m*|a|
df['F_r (N)'] = mass * (df[a_forward])  # flip sign if your forward accel is negative during coastdown

print(df[[time, a_forward, 'F_r (N)']].head())

plt.figure()
plt.plot(df[time], df[pitch_deg])
plt.xlabel('Velocity (m/s)')
plt.ylabel('Forward acceleration (m/s²)')
plt.title('Forward acceleration over time')
plt.tight_layout()
plt.show()

plt.figure()
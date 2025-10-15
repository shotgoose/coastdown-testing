import os
import math
import networkx
import pandas as pd

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
starting_speed = 10 #m/s

#directory to access csv files from
directory = '.'

csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and os.path.isfile(os.path.join(directory, f))]

if csv_files:
    first_csv_file = os.path.join(directory, csv_files[0])
    df = pd.read_csv(first_csv_file)
    print(df.head())
else:
    print("No CSV files found in directory")

# if df:
#     df['dv'] = df['a'] * df['t']
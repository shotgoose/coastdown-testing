import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

# constants
MASS = 250 #kg
WHEEL_DIAMETER = 58.42 #cm

# filepaths
SOURCE_FOLDER = "csv-data"
DESTINATION_FOLDER = "coastdown-data"
DIRECTORY = os.getcwd()
INPUT_PATH = os.path.join(DIRECTORY, SOURCE_FOLDER)
OUTPUT_PATH = os.path.join(DIRECTORY, DESTINATION_FOLDER)

def process_file(filename):
    # read file while skipping comments
    df = pd.read_csv(filename, comment="#")

    # keep desired data
    desired_data = ["Time", "RR_Wheel,Speed"]
    df = df[desired_data]

    # rename columns for convenience
    column_names = {"Time" : "time", "RR_Wheel,Speed" : "wheel_rpm"}
    df = df.rename(columns=column_names)

    # determine car velocity (m/s)
    df["velocity"] = df["wheel_rpm"] * ((math.pi * WHEEL_DIAMETER) / 60 / 100)
    df["velocity"] = df["velocity"].rolling(window=100).mean()
    
    # numerically derive for acceleration (m/s^2)
    dv = df["velocity"].diff()
    dt = df["time"].diff()
    df["acceleration"] = (dv / dt).rolling(window=50).mean()

    # drivetrain resistance (N) - only positive values are kept
    df["F_r"] = (MASS * (-df["acceleration"])).clip(lower=0)
    df["F_r"] = df["F_r"].rolling(window=600).mean()

    
    return df

    # return pd.DataFrame({

    # })

# function that iterates all files to process
def iterate_files():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    csv_files = [f for f in os.listdir(INPUT_PATH) if f.lower().endswith(".csv")]
    print(csv_files)
    index = 0
    total = len(csv_files)

    for filename in csv_files:
        # find file name
        input = os.path.join(INPUT_PATH, filename)

        # process file
        df = process_file(input)

        # output
        base, ext = os.path.splitext(filename)
        out_name = f"{base}_converted{ext}"
        output_path = os.path.join(OUTPUT_PATH, out_name)
        df.to_csv(output_path, index=False)

        # message 
        index += 1
        print(str(index) + "/" + str(total) + ": " + filename + " converted to " + out_name)

def graph_data(filename):
    # read file while skipping comments
    df = pd.read_csv(filename, comment="#")

    plt.figure()
    plt.plot(df["time"], df["F_r"])
    plt.xlabel("time")
    plt.ylabel("resistance (N)")
    plt.title("time" + ' vs. ' + "drivetrain resistance")
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(df["time"], df["velocity"])
    plt.xlabel("time")
    plt.ylabel("velocity m/s")
    plt.title("time" + ' vs. ' + "velocity")
    plt.tight_layout()
    plt.show()

#iterate_files()
graph_data(os.path.join(OUTPUT_PATH, "RR-Coastdown-2WD-1_converted.csv"))
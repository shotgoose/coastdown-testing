# generates proof of concept data. NOT REAL DATA
import pandas as pd
import numpy as np

rng = np.random.default_rng(2025)
g = 9.81
fs = 62.5
dt = 1 / fs
v0 = 8.0
CdA_over_m = 0.015
a_roll = 0.12

T_max = 40.0
t = np.round(np.arange(0, T_max + dt / 2, dt), 3)

v = np.zeros_like(t)
v[0] = v0
ax = np.zeros_like(t)
for i in range(1, len(t)):
    a_model = -(CdA_over_m * v[i - 1] ** 2 + a_roll)
    a_noise = rng.normal(0, 0.05) + 0.04 * np.sin(7.5 * t[i]) + 0.02 * np.sin(19.0 * t[i] + 0.6)
    ax[i] = a_model + a_noise
    v[i] = max(0.0, v[i - 1] + ax[i] * dt)
    if v[i] <= 0.05 and t[i] > 2.0:
        t = t[: i + 1]
        ax = ax[: i + 1]
        v = v[: i + 1]
        break

pitch = -0.02 * (ax - ax.min()) / (abs(ax.min()) + 1e-6)
ay = -g + pitch + rng.normal(0, 0.05, size=t.size)

az = 0.05 * np.sin(0.5 * t + 0.8) + 0.03 * np.sin(5.2 * t) + rng.normal(0, 0.07, size=t.size)

df = pd.DataFrame({
    "time (seconds)": t,
    "accelerometer X (m/sec^2 highlighted)": np.round(ax, 2),
    "accelerometer Y (m/sec^2 highlighted)": np.round(ay, 2),
    "accelerometer Z (m/sec^2 highlighted)": np.round(az, 2),
})

df.to_csv("poc_accel_250kg_8ms_coastdown_Z0.csv", index=False)
print("Saved to poc_accel_250kg_8ms_coastdown_Z0.csv")
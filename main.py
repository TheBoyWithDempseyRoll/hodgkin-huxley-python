import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

C_m = 1.0

g_Na = 120.0
g_K = 36.0
g_L = 0.3

E_Na = 50.0
E_K = -77.0
E_L = -54.387

T = 50.0
dt = 0.01
time = np.arange(0, T, dt)

def alpha_m(V):
    return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))

def beta_m(V):
    return 4.0 * np.exp(-(V +65.0)/18.0)

def alpha_h(V):
    return 0.07 * np.exp(-(V +65.0)/20.0)

def beta_h(V):
    return 1 / (1+ np.exp(-(V +35.0)/10.0))

def alpha_n(V):
    return (0.01 * (V + 55.0)) / (1.0 - np.exp(-(V + 55.0)/10.0))

def beta_n(V):
    return 0.125 * np.exp(-(V +65.0)/80.0)

def hodgkin_huxley(state, t):
    V, m, h, n = state

    I_inj = 10.0 * (t > 10) - 10.0 * (t > 40)

    I_Na = g_Na * (m**3) * h * (V - E_Na)

    I_K = g_K * (n**4) * (V - E_K)

    I_L = g_L * (V - E_L)

    dVdt = (I_inj - I_Na - I_K - I_L) / C_m

    dmdt = alpha_m(V) * (1 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1 - n) - beta_n(V) * n

    return [dVdt, dmdt, dhdt, dndt]

V0 = -65.0
m0 = 0.0529
h0 = 0.5961
n0 = 0.3177

state0 = [V0, m0, h0, n0]

solution = odeint(hodgkin_huxley, state0, time)

V = solution[:,0]

plt.figure(figsize=(10,6))

plt.plot(time, V, label="Membran Voltage (V)")
plt.title("Hodgkin Huxley Model")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (mV)")
plt.axhline(y=-65, color="r", linestyle="--", label="Resting (-65mV)")
plt.legend()

plt.show()
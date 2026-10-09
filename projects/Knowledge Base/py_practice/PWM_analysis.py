import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Parameters
# ============================================================

Vdc = 800.0
Vm = 325.0
f0 = 50.0

R = 1.0
L = 10e-3

w0 = 2*np.pi*f0
T0 = 1/f0


# ============================================================
# IDEAL STEADY-STATE SINUSOIDAL CURRENT
#
# L di/dt + R i = Vm sin(w0 t)
#
# i_ss(t) = A sin(w0 t) + B cos(w0 t)
# ============================================================

A = Vm*R / (R**2 + (w0*L)**2)
B = -Vm*w0*L / (R**2 + (w0*L)**2)

Ipk = np.sqrt(A**2 + B**2)
Irms_ideal = Ipk / np.sqrt(2)


def i_ideal_ss(t):
    return A*np.sin(w0*t) + B*np.cos(w0*t)


# ============================================================
# EXACT propagation through a constant-voltage interval
# ============================================================

def propagate(i0, v, dt):
    """
    Exact solution of

        L di/dt + R i = v

    for constant v over dt.
    """
    a = np.exp(-R*dt/L)

    return i0*a + (v/R)*(1-a)


# ============================================================
# Generate PWM intervals for one fundamental cycle
#
# Each switching interval:
#
#   +Vdc/2 for D*Ts
#   -Vdc/2 for (1-D)*Ts
#
# Duty is continuous / real-valued.
# ============================================================

def pwm_intervals(n):

    fs = n*f0
    Ts = 1/fs

    intervals = []

    for m in range(n):

        t0 = m*Ts
        t1 = (m+1)*Ts
        tc = 0.5*(t0+t1)

        # Continuous sinusoidal reference
        vref = Vm*np.sin(w0*tc)

        # Average voltage:
        #
        # Vavg = D*(+Vdc/2) + (1-D)*(-Vdc/2)
        #      = (2D-1)Vdc/2
        #
        # Hence:
        #
        # D = 0.5 + Vref/Vdc
        D = 0.5 + vref/Vdc

        if not (0 <= D <= 1):
            raise ValueError(
                f"Overmodulation at n={n}: D={D}"
            )

        ton = D*Ts
        toff = Ts-ton

        # +Vdc/2 segment
        if ton > 0:
            intervals.append(
                (t0, t0+ton, +Vdc/2)
            )

        # -Vdc/2 segment
        if toff > 0:
            intervals.append(
                (t0+ton, t1, -Vdc/2)
            )

    return intervals


# ============================================================
# Find periodic steady-state starting current
#
# Over the entire fundamental period:
#
# i(T0) = a*i(0) + b
#
# Periodic steady state requires:
#
# i(T0) = i(0)
#
# => i(0) = b/(1-a)
# ============================================================

def steady_state_initial_current(intervals):

    i = 0.0

    for t0, t1, v in intervals:

        dt = t1-t0
        i = propagate(i, v, dt)

    i_end_from_zero = i

    # Since every interval has the same R/L,
    # total attenuation over T0 is:
    a = np.exp(-R*T0/L)

    i_start = i_end_from_zero / (1-a)

    return i_start


# ============================================================
# Accurate SSE using Gauss-Legendre quadrature
# ============================================================

# Number of quadrature points per constant-voltage interval.
# This is NOT duty-cycle discretization.
Nq = 16

xg, wg = np.polynomial.legendre.leggauss(Nq)


def calculate_sse(n):

    intervals = pwm_intervals(n)

    # Periodic steady-state current at t=0
    i = steady_state_initial_current(intervals)

    SSE = 0.0

    for t0, t1, v in intervals:

        dt = t1-t0

        # Map Gauss-Legendre nodes to [t0,t1]
        t = 0.5*(t0+t1) + 0.5*dt*xg

        # Local time since beginning of interval
        tau = t-t0

        # Exact PWM current inside interval
        ipwm = (
            i*np.exp(-R*tau/L)
            + (v/R)*(1-np.exp(-R*tau/L))
        )

        # Ideal steady-state sinusoidal current
        iref = i_ideal_ss(t)

        error = ipwm-iref

        # Integral over this interval
        SSE += 0.5*dt*np.sum(wg*error**2)

        # Exact current at interval end
        i = propagate(i, v, dt)

    RMS_error = np.sqrt(SSE/T0)

    return SSE, RMS_error, i


# ============================================================
# Run n = 2^k
# ============================================================

results = []

for k in range(1, 11):

    n = 2**k

    SSE, RMS_error, i_end = calculate_sse(n)

    results.append({
        "k": k,
        "n": n,
        "switching_frequency_Hz": n*f0,
        "SSE_A2_s": SSE,
        "RMS_error_A": RMS_error,
        "error_percent": 100*RMS_error/Irms_ideal,
        "periodicity_error_A": i_end
    })


df = pd.DataFrame(results)

print("\nIdeal steady-state current:")
print(f"Peak RMS current = {Ipk:.6f} A")
print(f"RMS current      = {Irms_ideal:.6f} A")

print("\nResults:")
print(df.to_string(index=False))


# ============================================================
# Convergence exponent
#
# SSE ~ C / n^p
# ============================================================

# Use the asymptotic region n >= 32
fit = df[df["n"] >= 32]

p_sse, logC_sse = np.polyfit(
    np.log(fit["n"]),
    np.log(fit["SSE_A2_s"]),
    1
)

p_rms, logC_rms = np.polyfit(
    np.log(fit["n"]),
    np.log(fit["RMS_error_A"]),
    1
)

print("\nConvergence:")
print(f"SSE exponent      = {-p_sse:.6f}")
print(f"RMS-error exponent = {-p_rms:.6f}")


# ============================================================
# Plot SSE
# ============================================================

plt.figure(figsize=(8,5))

plt.loglog(
    df["n"],
    df["SSE_A2_s"],
    "o-"
)

plt.xlabel("n")
plt.ylabel("SSE [A²·s]")
plt.title("Steady-State PWM Current SSE")
plt.grid(True, which="both")
plt.tight_layout()
plt.show()


# ============================================================
# Plot RMS error
# ============================================================

plt.figure(figsize=(8,5))

plt.loglog(
    df["n"],
    df["RMS_error_A"],
    "o-"
)

plt.xlabel("n")
plt.ylabel("RMS current error [A]")
plt.title("Steady-State RMS Current Error")
plt.grid(True, which="both")
plt.tight_layout()
plt.show()


# ============================================================
# Plot percentage error
# ============================================================

plt.figure(figsize=(8,5))

plt.loglog(
    df["n"],
    df["error_percent"],
    "o-"
)

plt.xlabel("n")
plt.ylabel("RMS error [% of ideal RMS current]")
plt.title("Steady-State Relative Current Error")
plt.grid(True, which="both")
plt.tight_layout()
plt.show()

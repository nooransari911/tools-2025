import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial.legendre import leggauss


# ============================================================
# PHYSICAL PARAMETERS
# ============================================================

Vdc = 800.0          # DC bus voltage [V]
Vm = 325.0           # Fundamental voltage amplitude [V]
f0 = 50.0            # Fundamental frequency [Hz]

R = 1.0              # Inductor resistance [ohm]
L = 10e-3            # Inductance [H]

w0 = 2 * np.pi * f0
T0 = 1 / f0


# ============================================================
# IDEAL STEADY-STATE CURRENT
#
# L di/dt + R i = Vm sin(wt)
#
# i_ideal(t) = A sin(wt) + B cos(wt)
# ============================================================

A = Vm * R / (R**2 + (w0 * L)**2)
B = -Vm * w0 * L / (R**2 + (w0 * L)**2)

Ipk_ideal = np.sqrt(A**2 + B**2)
Irms_ideal = Ipk_ideal / np.sqrt(2)


def i_ideal_ss(t):
    return (
        A * np.sin(w0 * t)
        + B * np.cos(w0 * t)
    )


# ============================================================
# EXACT RL PROPAGATION FOR CONSTANT VOLTAGE
# ============================================================

def propagate(i0, v, dt):
    """
    Exact solution over interval dt for:

        L di/dt + R i = v
    """

    a = np.exp(-R * dt / L)

    return i0 * a + (v / R) * (1 - a)


# ============================================================
# DUTY RESOLUTION
# ============================================================

MODES = {
    "infinite": "Infinite duty resolution",
    "fixed": "Fixed 256-step duty resolution",
    "degrading": "Resolution halves whenever fs doubles",
}

FIXED_STEPS = 256

# Degrading-resolution reference point:
# n=2 -> 100 Hz -> 256 duty steps.
DEGRADING_REFERENCE_N = 2


def get_duty_steps(n, mode):
    """
    Return number of duty-cycle steps.

    infinite:
        None

    fixed:
        256 steps at every frequency

    degrading:
        N_D * f_s = constant
        therefore N_D halves whenever f_s doubles.
    """

    if mode == "infinite":
        return None

    if mode == "fixed":
        return FIXED_STEPS

    if mode == "degrading":
        steps = FIXED_STEPS * DEGRADING_REFERENCE_N / n

        # Physical PWM resolution must be an integer.
        # Never allow fewer than one duty step.
        return max(1, int(round(steps)))

    raise ValueError(f"Unknown mode: {mode}")


# ============================================================
# DUTY QUANTIZATION
# ============================================================

def quantize_duty(D, n_steps):
    """
    Quantize duty cycle to n_steps across [0,1].

    Infinite resolution is handled by passing None.
    """

    if n_steps is None:
        return D

    Dq = np.round(D * n_steps) / n_steps

    return np.clip(Dq, 0.0, 1.0)


# ============================================================
# CONSTRUCT ONE FUNDAMENTAL PERIOD OF PWM
# ============================================================

def build_pwm_intervals(n, mode):

    fs = n * f0
    Ts = 1 / fs

    n_steps = get_duty_steps(n, mode)

    intervals = []

    for m in range(n):

        t0 = m * Ts
        t1 = (m + 1) * Ts

        # Midpoint sampling of sinusoidal modulation
        tc = 0.5 * (t0 + t1)

        # Ideal continuous duty
        D_ideal = (
            0.5
            + (Vm / Vdc) * np.sin(w0 * tc)
        )

        # Finite-resolution PWM
        D_actual = quantize_duty(
            D_ideal,
            n_steps
        )

        ton = D_actual * Ts
        toff = Ts - ton

        # +Vdc/2 during ON
        if ton > 0:
            intervals.append(
                (t0, t0 + ton, +Vdc / 2)
            )

        # -Vdc/2 during OFF
        if toff > 0:
            intervals.append(
                (t0 + ton, t1, -Vdc / 2)
            )

    return intervals, n_steps


# ============================================================
# PERIODIC STEADY-STATE INITIAL CURRENT
#
# We solve:
#
#     i(T0) = i(0)
#
# rather than imposing i(0)=0.
# ============================================================

def periodic_initial_current(intervals):

    # First propagate from i(0)=0
    i = 0.0

    for t0, t1, v in intervals:

        dt = t1 - t0

        i = propagate(i, v, dt)

    i_T_from_zero = i

    # Overall RL decay over one fundamental period
    alpha = np.exp(-R * T0 / L)

    # Fixed point:
    #
    # i_T = alpha*i_0 + beta
    # i_T = i_0
    #
    # => i_0 = beta/(1-alpha)

    i0 = i_T_from_zero / (1 - alpha)

    return i0


# ============================================================
# GAUSS-LEGENDRE QUADRATURE
#
# This evaluates the continuous SSE accurately.
# It is NOT PWM/duty-cycle discretization.
# ============================================================

N_QUAD = 20

xg, wg = leggauss(N_QUAD)


# ============================================================
# CALCULATE ONE CASE
# ============================================================

def calculate_case(n, mode):

    intervals, n_steps = build_pwm_intervals(
        n,
        mode
    )

    # Periodic steady-state starting current
    i0 = periodic_initial_current(intervals)

    i = i0

    SSE = 0.0

    for t0, t1, v in intervals:

        dt = t1 - t0

        # Map Gauss-Legendre nodes onto [t0,t1]
        t = (
            0.5 * (t0 + t1)
            + 0.5 * dt * xg
        )

        tau = t - t0

        # Exact PWM current inside interval
        i_pwm = (
            i * np.exp(-R * tau / L)
            + (v / R)
            * (1 - np.exp(-R * tau / L))
        )

        # Ideal steady-state sinusoidal current
        i_ref = i_ideal_ss(t)

        error = i_pwm - i_ref

        # Integral of error^2
        SSE += (
            0.5
            * dt
            * np.sum(wg * error**2)
        )

        # Current at end of interval
        i = propagate(i, v, dt)

    # RMS error over one complete fundamental cycle
    RMS_error = np.sqrt(SSE / T0)

    # Relative RMS error
    error_percent = (
        100
        * RMS_error
        / Irms_ideal
    )

    # Correct periodicity metric
    periodicity_error = i - i0

    return {
        "SSE_A2_s": SSE,
        "RMS_error_A": RMS_error,
        "error_percent": error_percent,
        "duty_steps": n_steps,
        "periodicity_error_A": periodicity_error,
    }


# ============================================================
# RUN ALL CASES
# ============================================================

rows = []

for k in range(1, 11):

    n = 2**k
    fs = n * f0

    for mode in MODES:

        result = calculate_case(n, mode)

        rows.append({
            "k": k,
            "n": n,
            "switching_frequency_Hz": fs,
            "mode": mode,
            **result
        })


df = pd.DataFrame(rows)


# ============================================================
# DISPLAY
# ============================================================

print("\nIdeal steady-state current")
print("--------------------------------")
print(f"Peak current : {Ipk_ideal:.6f} A")
print(f"RMS current  : {Irms_ideal:.6f} A")

print("\nResults")
print("--------------------------------")

print(
    df[
        [
            "k",
            "n",
            "switching_frequency_Hz",
            "mode",
            "duty_steps",
            "SSE_A2_s",
            "RMS_error_A",
            "error_percent",
            "periodicity_error_A",
        ]
    ].to_string(index=False)
)


# ============================================================
# PLOTS
# ============================================================

labels = {
    "infinite": "Infinite resolution",
    "fixed": "Fixed 256 steps",
    "degrading": "Degrading resolution",
}


# ------------------------------------------------------------
# RMS ERROR
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for mode in MODES:

    d = df[df["mode"] == mode]

    plt.loglog(
        d["switching_frequency_Hz"],
        d["RMS_error_A"],
        "o-",
        label=labels[mode]
    )

plt.xlabel("Switching frequency [Hz]")
plt.ylabel("RMS current error [A]")
plt.title("Steady-State Current Error")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# RELATIVE ERROR
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for mode in MODES:

    d = df[df["mode"] == mode]

    plt.loglog(
        d["switching_frequency_Hz"],
        d["error_percent"],
        "o-",
        label=labels[mode]
    )

plt.xlabel("Switching frequency [Hz]")
plt.ylabel("RMS error [%]")
plt.title("Relative Steady-State Current Error")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# SSE
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for mode in MODES:

    d = df[df["mode"] == mode]

    plt.loglog(
        d["switching_frequency_Hz"],
        d["SSE_A2_s"],
        "o-",
        label=labels[mode]
    )

plt.xlabel("Switching frequency [Hz]")
plt.ylabel("SSE [A²·s]")
plt.title("Steady-State Current SSE")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# DUTY RESOLUTION
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for mode in ["fixed", "degrading"]:

    d = df[df["mode"] == mode]

    plt.semilogx(
        d["switching_frequency_Hz"],
        d["duty_steps"],
        "o-",
        label=labels[mode]
    )

plt.xlabel("Switching frequency [Hz]")
plt.ylabel("Available duty steps")
plt.title("Duty-Cycle Resolution")
plt.grid(True, which="both")
plt.legend()
plt.tight_layout()
plt.show()

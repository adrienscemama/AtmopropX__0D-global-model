import numpy as np
from scipy.constants import pi, e, k, epsilon_0 as eps_0, c, m_e
from scipy.special import jv
from scipy.optimize import fsolve

SIGMA_I = 1e-18 # Review this for iodine

def u_B(T_e, m_i):
    return np.sqrt(k * T_e / m_i)

def h_L(n_g, L):
    lambda_i = 1/(n_g * SIGMA_I)
    return 0.86 / np.sqrt(3 + (L / (2 * lambda_i)))

def h_R(n_g, R):
    lambda_i = 1/(n_g * SIGMA_I)
    return 0.8 / np.sqrt(4 + (R / lambda_i))

def maxwellian_flux_speed(T, m):
    # TODO : what is it, where does it come from, does it always hold true
    return np.sqrt((8 * k * T) / (pi * m))

def pressure(T, Q, v, A_out):
    """Calculates pressure in steady state without any plasma.
    T : Temperature in steady state
    Q : inflow rate in the chamber
    v : mean velocity of gas in steady state
    A_out : Effective area for which the gas can leave the chamber"""
    return (4 * k * T * Q) / (v * A_out)

def A_eff(n_g, R, L):
    return (2 * h_R(n_g, R) * pi * R * L) + (2 * h_L(n_g, L) * pi * R**2)

def A_eff_1(n_g, R, L, beta_i):
    return 2 * h_R(n_g, R) * pi * R * L + (2 - beta_i) * h_L(n_g, L) * pi * R**2

def eps_p(tab_c , tab_eps):
    """ Cauculates eps_p from the already calculated eps_i and c_i for each ion"""
    def equation(tab_c , tab_eps , x):
        sum = 0
        for i in(range(len(tab_c_i))):
            sum += tab_c[i](tab_eps[i]-1)/(tab_eps[i] + 2*x))
        sum += (1-x)/(3*x)
    return fsolve(equation, 1)

def R_ind(R, L, N, omega, n_e, n_g, K_el):
    ep = eps_p(omega, n_e, n_g, K_el)
    k_p = (omega / c) * np.sqrt(ep)
    a = 2 * pi * N**2 / (L * omega * eps_0)
    b = 1j * k_p * R * jv(1, k_p * R) / (ep * jv(0, k_p * R))

    return a * np.real(b)

#!/usr/bin/env python
"""
norm_main.py =>

This file calls 2 functions from the compiled C library `norm.so`.
The function prototypes are:

    *** double norm(double x, double mu, double sigma)

    *** void cdf_array(double mu, double sigma, int n,
                        double* input_array, double* output_array)

"""
import ctypes
import numpy as np
from scipy.stats import norm

# suppress scientific notation =>
np.set_printoptions(suppress=True)

# full path to shared library =>
LIB_PATH = "E:/Repos/Extensions/norm.so"

# bind reference to shared library `norm.so` =>
normlib = ctypes.cdll.LoadLibrary(LIB_PATH)


# specify argument datatypes for norm and cdf_array =>
normlib.norm_cdf.argtypes  = [ctypes.c_double,
                              ctypes.c_double,
                              ctypes.c_double]

normlib.cdf_array.argtypes = [ctypes.c_double,
                              ctypes.c_double,
                              ctypes.c_int,
                              ctypes.POINTER(ctypes.c_double),
                              ctypes.POINTER(ctypes.c_double)]



# specify return datatypes for norm and cdf_array;
# cdf_array declared as `void` =>
normlib.norm_cdf.restype  = ctypes.c_double
normlib.cdf_array.restype = None


# use scipy.stats to generate 10 standard normal random
# variates; this will be `input_arr` - we also initialize
# `output_arr` to all zeros, and set the random seed in
# numpy for reproducibility =>
np.random.seed(516)
mu         = 0
sigma      = 1.
n          = 10
input_arr  = norm.rvs(loc=mu, scale=sigma, size=n)
output_arr = np.zeros(n, np.float_)

# Initialize ctypes-compatible versions of mu, sigma, n
# input_arr and output_arr =>
ct_mu         = ctypes.c_double(mu)
ct_sigma      = ctypes.c_double(sigma)
ct_n          = ctypes.c_int(n)
ct_input_arr  = np.ctypeslib.as_ctypes(input_arr)
ct_output_arr = np.ctypeslib.as_ctypes(output_arr)

print("\nNormal variates w/ mean {} and standard deviation {}:\n".format(mu,sigma))
print(input_arr)

print("\noutput_arr before passing to cdf_array:\n")
print(output_arr)

# Call `normlib.cdf_array` from C library =>
normlib.cdf_array(ct_mu, ct_sigma, ct_n, ct_input_arr, ct_output_arr)

print("\noutput_arr after passing to cdf_array:\n")
print(output_arr)

# compare results returned by cdf_array to scipy's norm.cdf =>
spcdfs = norm.cdf(input_arr, loc=mu, scale=sigma)
print("\nscipy-evaluated CDFs:\n")
print(spcdfs)

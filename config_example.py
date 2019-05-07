grid_steps = 641  #: Transverse grid size in cells
grid_step_size = .025  #: Transverse grid step size in plasma units

xi_step_size = .005  #: Step size in time-space coordinate xi
xi_steps = int(3000 // xi_step_size)  #: Amount of xi steps


field_solver_subtraction_trick = 1  #: 0 for Laplace eqn., Helmholtz otherwise
field_solver_variant_A = True  #: Use Variant A or Variant B for Ex, Ey, Bx, By

reflect_padding_steps = 5  #: Plasma reflection <-> field calculation boundaries
plasma_padding_steps = 10  #: Plasma placement <-> field calculation boundaries

plasma_coarseness = 3  #: Square root of the amount of cells per coarse particle
plasma_fineness = 2  #: Square root of the amount of fine particles per cell


from numpy import cos, exp, pi, sqrt

def beam(xi_i, x, y):
    xi = -xi_i * xi_step_size
    COMPRESS, BOOST, SIGMA, SHIFT = 1, 1, 1, 0
    if xi < -2 * sqrt(2 * pi) / COMPRESS:
        return 0
    r = sqrt(x**2 + (y - SHIFT)**2)
    return (.05 * BOOST * exp(-.5 * (r / SIGMA)**2) *
            (1 - cos(xi * COMPRESS * sqrt(pi / 2))))

gpu_index = 0  #: Index of the GPU that should perform the calculations

diagnostics_each_N_steps = int(1 / xi_step_size)  #: Diagnostics calls rarity
diagnostics_wants_numpy_arrays = True  #: Wrap GPUArrays into GPUArraysView

# Some sloppy example diagnostics

Ez_00_history = []
max_zn = 0
def diagnostics(config, xi_i, state):
    global Ez_00_history, max_zn

    import lcode
    import scipy.ndimage, scipy.signal
    import numpy as np

    xi = -xi_i * config.xi_step_size

    ro = state.ro  # Unpack once to prevent copying ro several times

    lcode.savepng('transverse', 'ro', xi, ro, vmin=-0.1, vmax=0.1, cmap='bwr')

    # Calculate some high-frequency noise metric
    bl = scipy.ndimage.gaussian_filter(ro, sigma=(.25 / config.grid_step_size))
    zn = np.abs(ro - bl).mean() / 4.23045376e-04
    max_zn = max(max_zn, zn)

    # Copy the entire Ez array, and only use the center cell value
    Ez_00 = state.Ez[config.grid_steps // 2, config.grid_steps // 2]
    Ez_00_history.append(Ez_00)

    # Display some information on relative on-axis Ez peak heights
    Ez_00_array = np.array(Ez_00_history)
    peak_indices = scipy.signal.argrelmax(Ez_00_array)[0]
    if peak_indices.size:
        peak_values = Ez_00_array[peak_indices]
        rel_deviations_perc = 100 * (peak_values / peak_values[0] - 1)
        peaks_info = f'{peak_values[-1]:0.4e} {rel_deviations_perc[-1]:+0.2f}%'
    else:
        peaks_info = '...'

    print(f'xi={xi:+.4f} {Ez_00:+.4e}|{peaks_info}|zn={max_zn:.3f}')


if __name__ == '__main__':  # If executed directly, run LCODE with this config
    import sys, lcode; lcode.main(sys.modules[__name__])
    # Or, if you want to, write out all the main loop in here

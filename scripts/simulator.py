"""
Simulator: Sersic + Exp
=======================

This script simulates `Imaging` of a galaxy using light profiles where:

 - The galaxy's bulge is a `Sersic`.
 - The galaxy's disk is an `Exponential`.
"""

from pathlib import Path

import autogalaxy as ag
import autogalaxy.plot as aplt


# Dataset path
dataset_type = "imaging"
dataset_name = "simple"
dataset_path = Path("dataset", dataset_type, dataset_name)
dataset_path.mkdir(parents=True, exist_ok=True)


# Grid
grid = ag.Grid2D.uniform(
    shape_native=(100, 100),
    pixel_scales=0.1,
)

# Over-sampling
over_sample_size = ag.util.over_sample.over_sample_size_via_radial_bins_from(
    grid=grid,
    sub_size_list=[32, 8, 2],
    radial_list=[0.3, 0.6],
    centre_list=[(0.0, 0.0)],
)

grid = grid.apply_over_sampling(over_sample_size=over_sample_size)


# PSF
psf = ag.Kernel2D.from_gaussian(
    shape_native=(11, 11),
    sigma=0.1,
    pixel_scales=grid.pixel_scales,
)


# Simulator
simulator = ag.SimulatorImaging(
    exposure_time=300.0,
    psf=psf,
    background_sky_level=0.1,
    add_poisson_noise_to_data=True,
)


# Galaxy
galaxy = ag.Galaxy(
    redshift=0.5,
    bulge=ag.lp.Sersic(
        centre=(0.0, 0.0),
        ell_comps=ag.convert.ell_comps_from(axis_ratio=0.9, angle=45.0),
        intensity=1.0,
        effective_radius=0.6,
        sersic_index=3.0,
    ),
    disk=ag.lp.Exponential(
        centre=(0.0, 0.0),
        ell_comps=ag.convert.ell_comps_from(axis_ratio=0.7, angle=30.0),
        intensity=0.5,
        effective_radius=1.6,
    ),
)

galaxies = ag.Galaxies(galaxies=[galaxy])


# Plot galaxy image before simulation
image = galaxies.image_2d_from(grid=grid)
aplt.Array2DPlotter(array=image).figure_2d()


# Simulate imaging dataset
dataset = simulator.via_galaxies_from(
    galaxies=galaxies,
    grid=grid,
)


# Plot simulated dataset
aplt.ImagingPlotter(dataset=dataset).subplot_dataset()


# Output FITS files
dataset.output_to_fits(
    data_path=dataset_path / "data.fits",
    psf_path=dataset_path / "psf.fits",
    noise_map_path=dataset_path / "noise_map.fits",
    overwrite=True,
)


# Save PNGs
mat_plot = aplt.MatPlot2D(
    output=aplt.Output(path=dataset_path, format="png")
)

aplt.ImagingPlotter(
    dataset=dataset,
    mat_plot_2d=mat_plot,
).subplot_dataset()

aplt.Array2DPlotter(
    array=dataset.data,
    mat_plot_2d=mat_plot,
).figure_2d()


# This may vary a bit by version, so keep it protected
try:
    aplt.GalaxiesPlotter(
        galaxies=galaxies,
        grid=grid,
        mat_plot_2d=mat_plot,
    ).subplot_galaxies()
except Exception as e:
    print("Galaxies subplot skipped:", e)


# Save galaxies object to JSON
ag.output_to_json(
    obj=galaxies,
    file_path=dataset_path / "galaxies.json",
)

print(f"Dataset written to: {dataset_path}")

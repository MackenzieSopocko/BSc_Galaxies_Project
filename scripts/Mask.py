"""
GUI Preprocessing: Mask
=======================

This tool allows one to mask a bespoke mask for a given image of a galaxy using an interactive GUI. This mask
can then be loaded before a pipeline is run and passed to that pipeline so as to become the default masked used by a
search (if a mask function is not passed to that search).
"""

from pathlib import Path
import autogalaxy as ag
import autogalaxy.plot as aplt
import numpy as np

dataset_name = "simple"
dataset_path = Path("dataset") / "imaging" / dataset_name

pixel_scales = 0.1

data = ag.Array2D.from_fits(
    file_path=dataset_path / "data.fits",
    pixel_scales=pixel_scales,
)

scribbler = ag.Scribbler(image=data.native)
mask = scribbler.show_mask()
mask = ag.Mask2D(mask=np.invert(mask), pixel_scales=pixel_scales)

array_plotter = aplt.Array2DPlotter(
    array=data,
    mat_plot_2d=aplt.MatPlot2D(
        title=aplt.Title(label="Data")
    ),
)
array_plotter.figure_2d()

array_plotter = aplt.Array2DPlotter(
    array=data,
    mat_plot_2d=aplt.MatPlot2D(
        title=aplt.Title(label="Data"),
        output=aplt.Output(
            path=dataset_path,
            filename="mask_gui",
            format="png",
        ),
    ),
)
array_plotter.figure_2d()

mask.output_to_fits(
    file_path=Path(dataset_path, "mask_gui.fits"),
    overwrite=True,
)

import numpy as np

"""
GUI Preprocessing: Lens Light Centre
====================================

This tool allows one to input the galaxy light centre(s) of a galaxy(es) via a GUI, which can be used as a fixed
value in pipelines.
"""

from pathlib import Path
import autogalaxy as ag
import autogalaxy.plot as aplt
from matplotlib import pyplot as plt

dataset_name = "simple__sersic"
dataset_path = Path("dataset") / "imaging" / dataset_name

pixel_scales = 0.1

data = ag.Array2D.from_fits(
    file_path=dataset_path / "data.fits",
    pixel_scales=pixel_scales,
)

search_box_size = 5

clicker = ag.Clicker(
    image=data,
    pixel_scales=pixel_scales,
    search_box_size=search_box_size,
)

n_y, n_x = data.shape_native
hw = int(n_x / 2) * pixel_scales
ext = [-hw, hw, -hw, hw]

fig = plt.figure(figsize=(14, 14))
plt.imshow(data.native, cmap="jet", extent=ext)
plt.colorbar()
cid = fig.canvas.mpl_connect("button_press_event", clicker.onclick)
plt.show()
fig.canvas.mpl_disconnect(cid)
plt.close(fig)

light_centres = ag.Grid2DIrregular(values=clicker.click_list)

positions = [np.array(light_centres)] if len(clicker.click_list) > 0 else None

visuals_2d = aplt.Visuals2D(positions=positions)

array_plotter = aplt.Array2DPlotter(
    array=data,
    visuals_2d=visuals_2d,
    mat_plot_2d=aplt.MatPlot2D(title=aplt.Title(label="Data")),
)
array_plotter.figure_2d()

mat_plot = aplt.MatPlot2D(
    title=aplt.Title(label="Data"),
    output=aplt.Output(
        path=dataset_path,
        filename="light_centres",
        format="png",
    ),
)

array_plotter = aplt.Array2DPlotter(
    array=data,
    visuals_2d=visuals_2d,
    mat_plot_2d=mat_plot,
)
array_plotter.figure_2d()

ag.output_to_json(
    obj=light_centres,
    file_path=Path(dataset_path, "light_centre.json"),
)

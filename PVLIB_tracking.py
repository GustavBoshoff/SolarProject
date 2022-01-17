"""
Discontinuous Tracking
======================

Example of a custom Mount class.
"""

# %%
# Many real-world tracking arrays adjust their position in discrete steps
# rather than through continuous movement. This example shows how to model
# this discontinuous tracking by implementing a custom Mount class.

from pvlib import tracking, pvsystem, location, modelchain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import matplotlib.pyplot as plt
import pandas as pd


# %%
# We'll define our custom Mount by extending
# :py:class:`~pvlib.pvsystem.SingleAxisTrackerMount` for convenience.
# Another approach would be to extend ``AbstractMount`` directly; see
# the source code of :py:class:`~pvlib.pvsystem.SingleAxisTrackerMount`
# and :py:class:`~pvlib.pvsystem.FixedMount` for how that is done.
array_kwargs = dict(
    module_parameters=dict(pdc0=1, gamma_pdc=-0.004),
    temperature_model_parameters=dict(a=-3.56, b=-0.075, deltaT=3)
)

class DualAxisTrackerMount(pvsystem.AbstractMount):
    def get_orientation(self, solar_zenith, solar_azimuth):
        # no rotation limits, no backtracking
        return {'surface_tilt': solar_zenith, 'surface_azimuth': solar_azimuth}



class DiscontinuousTrackerMount(pvsystem.SingleAxisTrackerMount):
    # inherit from SingleAxisTrackerMount so that we get the
    # constructor and tracking attributes (axis_tilt etc) automatically

    def get_orientation(self, solar_zenith, solar_azimuth):
        # Different trackers update at different rates; in this example we'll
        # assume a relatively slow update interval of 15 minutes to make the
        # effect more visually apparent.
        zenith_subset = solar_zenith.resample('1min').first()
        azimuth_subset = solar_azimuth.resample('1min').first()
        axis_tilt=0
        tracking_data_15min = tracking.singleaxis(
            zenith_subset, azimuth_subset,
            axis_tilt, self.axis_azimuth,
            self.max_angle, self.backtrack,
            self.gcr, self.cross_axis_tilt
        )
        # propagate the 15-minute positions to 1-minute stair-stepped values:
        tracking_data_1min = tracking_data_15min.reindex(solar_zenith.index,
                                                         method='ffill')
        return tracking_data_1min


# %%
# Let's take a look at the tracker rotation curve it produces:
times = pd.date_range('2019-01-01 06:00', '2019-01-01 18:00', freq='5min',
                      tz='Etc/GMT+5')
loc = location.Location(40, -80)
solpos = loc.get_solarposition(times)
mount = DiscontinuousTrackerMount(axis_azimuth=180, gcr=0.4)
tracker_data = mount.get_orientation(solpos.apparent_zenith, solpos.azimuth)
# tracker_data['tracker_theta'].plot()
# plt.ylabel('Tracker Rotation [degree]')
# plt.show()
#fixed panel fixedmount(tilt,azimuth)
array = pvsystem.Array(pvsystem.FixedMount(0, 0),
                   **array_kwargs)
system_fixed = pvsystem.PVSystem(arrays=[array], inverter_parameters=dict(pdc0=3))
mc_fixed = modelchain.ModelChain(system_fixed, loc, aoi_model='physical',
                           spectral_model='no_loss')
weather = loc.get_clearsky(times)
mc_fixed.run_model(weather)

array = pvsystem.Array(
    mount=DualAxisTrackerMount(),
    module_parameters=dict(pdc0=1, gamma_pdc=-0.004, b=0.05),
    temperature_model_parameters=dict(a=-3.56, b=-0.075, deltaT=3))
system = pvsystem.PVSystem(arrays=[array], inverter_parameters=dict(pdc0=3))
mc_dual = modelchain.ModelChain(system, loc, spectral_model='no_loss')
weather = loc.get_clearsky(times)
mc_dual.run_model(weather)


# %%
# With our custom tracking logic defined, we can create the corresponding
# Array and PVSystem, and then run a ModelChain as usual:


module_parameters = {'pdc0': 1, 'gamma_pdc': -0.004, 'b': 0.05}
array2 = pvsystem.Array(mount=mount, module_parameters=module_parameters,
                       temperature_model_parameters=dict(a=-3.56, b=-0.075, deltaT=3))
system = pvsystem.PVSystem(arrays=[array2], inverter_parameters={'pdc0': 1})
mc = modelchain.ModelChain(system, loc, spectral_model='no_loss')

# simple simulated weather, just to show the effect of discrete tracking
weather = loc.get_clearsky(times)
mc.run_model(weather)

fig, axes = plt.subplots(2, 1, sharex=True)
mc.results.effective_irradiance.plot(ax=axes[0])
axes[0].set_ylabel('Effective Irradiance [W/m^2]')
#fixed axis plot
mc_fixed.results.ac.plot(ax=axes[1], label = 'fixed')
#single axis plot
mc.results.ac.plot(ax=axes[1],label = 'Single')
#_Dual Axis plot
mc_dual.results.ac.plot(ax=axes[1], label = 'Dual')
plt.ylabel('Output Power')
axes[1].set_ylabel('AC Power')
fig.show()
plt.legend()
axes[1].legend()
plt.show()
# %%
# The effect of discontinuous tracking creates a "jagged" effect in the
# simulated plane-of-array irradiance, which then propagates through to
# the AC power output.

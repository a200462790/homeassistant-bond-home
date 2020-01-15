"""Bond Home Fan Integration"""
from homeassistant.components.cover import (CoverDevice)
import logging
DOMAIN = 'bond'

# Import the device class from the component that you want to support

_LOGGER = logging.getLogger(__name__)

BOND_SHADE_TYPE = 'MS'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Bond Fan platform"""
    # Setup connection with devices/cloud
    bond = hass.data[DOMAIN]['bond_hub']

    # Add devices
    for device_id in bond.getDeviceIds():
        device_properties = bond.getDevice(device_id)
        if device_properties['type'] == BOND_SHADE_TYPE:
            add_entities([BondShade(bond, device_id, device_properties)])

class BondShade(CoverDevice):
    """Representation of an Bond Shade"""

    def __init__(self, bond, device_id, device_properties):
        """Initialize a Bond Fan"""
        self._bond = bond
        self._deviceId = device_id

        bondProperties = device_properties

        self._name = bondProperties['name']
        self._state = None

    def close_cover(self, **kwargs):
        """Close the cover."""
        self._bond.closeShade(self._deviceId)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self._bond.holdShade(self._deviceId)

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._bond.openShade(self._deviceId)

    @property
    def current_cover_position(self):
        """Return the current position of cover shutter."""
        if self._state is not None:
            return int(self._state * 100)
        return None

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return bool(self._state == 0)

    @property
    def name(self):
        """Return the display name of this fan"""
        return self._name

    def update(self):
        """Fetch new state data for this fan
        This is the only method that should fetch new data for Home Assistant
        """
        bondState = self._bond.getDeviceState(self._deviceId)
        self._state = bondState['open']

from applications.system.dispatches import dispatches as system_dispatches
from applications.shell.dispatches import dispatches as shell_dispatches
from applications.thermostat.dispatches import dispatches as thermostat_dispatches

UTILS_DISPATCHES = [
    system_dispatches,
    shell_dispatches,
    thermostat_dispatches,
]





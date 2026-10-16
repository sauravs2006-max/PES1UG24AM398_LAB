"""Smart home device controller.

Adds devices to rooms, switches them on and off, sets the thermostat within
a safe range, lists devices by room, reports power use and saves the home
state to a JSON file.
"""
import json
import os
import subprocess  # nosec B404 - needed by run_scene, input is validated

HUB_HOST = os.environ.get("HUB_HOST", "127.0.0.1")
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_PASSWORD = os.environ.get("HUB_PASSWORD")
MIN_TEMP = 16
MAX_TEMP = 30
SCENES_DIR = "scenes"
devices = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device. Every device gets its own settings dict."""
    devices[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": {} if settings is None else dict(settings),
    }


def toggle_device(device_name):
    """Flip a device on/off. Return the new state, or None if unknown."""
    if device_name in devices:
        devices[device_name]["on"] = not devices[device_name]["on"]
        return devices[device_name]["on"]
    print("Device not found:", device_name)
    return None


def set_temperature(device_name, value):
    """Set a thermostat, clamped to the safe range. Return True on success."""
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, MIN_TEMP), MAX_TEMP)
    return True


def devices_in_room(room):
    """Return the names of all devices in the given room."""
    return [name for name, info in devices.items() if info["room"] == room]


def power_usage():
    """Return the total power draw (W) of all devices that are on."""
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)


def save_state(file_name="home_state.json"):
    """Write the current home state to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(devices, file, indent=2)


def hub_address():
    """Return the hub address as host:port."""
    return f"{HUB_HOST}:{HUB_PORT}"


def run_scene(scene_script):
    """Run a script from the scenes folder. Return its exit code or None."""
    script = os.path.basename(scene_script)
    path = os.path.join(SCENES_DIR, script)
    if script != scene_script or not os.path.isfile(path):
        print("Scene not found:", scene_script)
        return None
    # Fixed argument list, no shell, validated file name
    return subprocess.call(["/bin/bash", path])  # nosec B603


def main():
    """Run a short demonstration of the controller."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    on_now = [name for name, info in devices.items() if info["on"]]
    print("Devices on:", on_now)
    save_state()


if __name__ == "__main__":
    main()

"""
ip_address and port are just used for the default values in the UI, they can be changed there.
"""

settings: dict = {
    "ip_address": "127.0.0.1",
    "port": 999,
    "api_version": "1",
    "device_id": "Rapsodo MLM2PRO",
    "units": "Yards"
}

"""
index 0 — Club Speed (units: mph) — typical club head speed for that club.
index 1 — Ball Speed (units: mph) — typical ball speed off the club.
index 2 — Launch Angle (units: degrees) — vertical launch angle of the ball.
index 3 — Spin Rate (units: rpm) — total spin applied to the ball.
index 4 — Carry Distance (units: yards) — expected carry distance for that club.
"""
club_data: dict[str, list[int]] = {
    "DR": [105, 155, 12, 2500, 250],
    "3w": [100, 145, 14, 3250, 230],
    "5w": [95, 140, 16, 3750, 215],
    "4i": [85, 125, 17, 4500, 195],
    "5i": [80, 120, 18, 5000, 180],
    "6i": [75, 115, 19, 5500, 170],
    "7i": [72, 110, 20, 6000, 160],
    "8i": [68, 105, 23, 6500, 150],
    "9i": [65, 100, 26, 7500, 140],
    "PW": [62, 90, 28, 8500, 130],
    "GW": [60, 85, 31, 9000, 110],
    "SW": [58, 80, 34, 10000, 100],
    "LW": [45, 75, 37, 10500, 90],
    "PT": [0, 0, 0, 0, 0],
}

from bt3562_client import BT3562Client
from range_checker import check
from config import CONFIG

class TestEngine:
    def __init__(self):
        self.device = BT3562Client(CONFIG["ip"])
        self.points = CONFIG["points"]

    def run(self, module_id):
        results = []
        details = []

        for p in self.points:
            raw = self.device.read()
            v, ir = map(float, raw.split(","))

            status, _ = check(p, v, ir)

            results.append(status)
            details.append({
                "Module": module_id,
                "Point": p,
                "Voltage": v,
                "IR(mΩ)": ir,
                "Status": status
            })

        final = "PASS" if "FAIL" not in results else "FAIL"

        return final, details
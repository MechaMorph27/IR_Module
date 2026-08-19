from config import CONFIG


def check(point, v, ir):
    l = CONFIG["limits"]

    if point == "Module":
        v_ok = l["module_v_min"] <= v <= l["module_v_max"]
        ir_ok = l["module_ir_min"] <= ir <= l["module_ir_max"]
    else:
        v_ok = l["cell_v_min"] <= v <= l["cell_v_max"]
        ir_ok = l["cell_ir_min"] <= ir <= l["cell_ir_max"]

    if v_ok and ir_ok:
        return "PASS", ""
    elif not v_ok and not ir_ok:
        return "FAIL", "V & IR FAIL"
    elif not v_ok:
        return "FAIL", "VOLTAGE FAIL"
    else:
        return "FAIL", "IR FAIL"
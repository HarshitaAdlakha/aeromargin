"""Deliberately wrong answers, each built with a specific mistake a practitioner would recognise.
validate_graders.py checks that every one of them FAILS its task's grader.
Each function returns {label: answer_dict}."""
import importlib.util
import math
from pathlib import Path

TASKS = Path(__file__).resolve().parent.parent / "tasks"


def _sol(task_id):
    spec = importlib.util.spec_from_file_location("s_" + task_id[:2], TASKS / task_id / "solution.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def t01():
    s = _sol("01-oblique-lug-fitting")
    out = {}
    def ans(pu, ms_lug, label):
        th = math.radians(s.ANGLE_DEG)
        pin = s.PIN_FSU * 2 * math.pi / 4 * s.PIN_D ** 2 / pu - 1
        out[label] = {"ultimate_design_load_lbf": round(pu, 1), "axial_component_lbf": round(pu * math.cos(th), 1),
                      "transverse_component_lbf": round(pu * math.sin(th), 1), "ms_lug_oblique": round(ms_lug, 4),
                      "ms_pin_shear": round(pin, 4), "governing_check": "lug_oblique",
                      "verdict": "pass" if min(ms_lug, pin) >= 0 else "fail"}
    th = math.radians(s.ANGLE_DEG)
    def ms(pu, exp):
        ra, rt = pu * math.cos(th) / s.P_AXIAL_ALLOW, pu * math.sin(th) / s.P_TRANS_ALLOW
        if exp is None:
            return min(1 / ra, 1 / rt) - 1
        return 1 / (ra ** exp + rt ** exp) ** (1 / exp) - 1
    pu = s.P_LIMIT * 1.5 * 1.15
    ans(pu, ms(pu, None), "components checked separately (no interaction)")
    ans(pu, ms(pu, 2.0), "quadratic interaction instead of the 1.6 exponent")
    ans(s.P_LIMIT * 1.5, ms(s.P_LIMIT * 1.5, 1.6), "fitting factor dropped")
    return out


def t02():
    s = _sol("02-short-strut-buckling")
    r = s.solve()
    idia = s.OD - 2 * s.WALL
    a = math.pi / 4 * (s.OD ** 2 - idia ** 2)
    fe = math.pi ** 2 * s.E / r["slenderness_ratio"] ** 2
    ms = fe * a / (s.P_LIMIT * 1.5) - 1
    return {"Euler used because Euler stress < Fcy": {**r, "regime": "euler", "critical_stress_psi": round(fe),
            "critical_load_lbf": round(fe * a), "ms": round(ms, 4), "verdict": "pass"}}


def t03():
    s = _sol("03-cas-to-tas-stratosphere")
    r = s.solve()
    out = {}
    a_isa = math.sqrt(1.4 * s.R * 216.65) / s.KT
    out["ISA temperature used for speed of sound"] = {**r, "oat_k": 216.65, "tas_kt": round(r["mach"] * a_isa, 1)}
    # incompressible: TAS = CAS / sqrt(sigma)
    sigma = (r["static_pressure_pa"] / (s.R * r["oat_k"])) / 1.225
    out["incompressible CAS/sqrt(sigma)"] = {**r, "tas_kt": round(250 / math.sqrt(sigma), 1)}
    out["density altitude by 120 ft per deg C rule"] = {**r, "density_altitude_ft": 41_000 + 120 * 10}
    # troposphere lapse law extrapolated above 11 km
    h = 41_000 * s.FT
    p_bad = s.P0 * (1 - s.LAPSE * h / s.T0) ** (s.G0 / (s.R * s.LAPSE))
    qc = s.P0 * ((1 + 0.2 * (250 / s.A0_KT) ** 2) ** 3.5 - 1)
    m_bad = math.sqrt(5 * ((qc / p_bad + 1) ** (2 / 7) - 1))
    out["troposphere law above the tropopause"] = {**r, "static_pressure_pa": round(p_bad), "mach": round(m_bad, 4),
                                                   "tas_kt": round(m_bad * math.sqrt(1.4 * s.R * 226.65) / s.KT, 1)}
    return out


def t04():
    s = _sol("04-weight-balance-fuel-burn")
    r = s.solve()
    ramp = s.RAMP_FUEL_GAL * s.FUEL_DENSITY
    arm = s.fuel_moment(s.RAMP_FUEL_GAL) / ramp
    zw = sum(i[0] for i in s.ITEMS)
    zm = sum(i[0] * i[1] for i in s.ITEMS)
    cg = lambda f: ((zm + f * arm) / (zw + f) - s.LEMAC) / s.MAC * 100
    return {"constant fuel arm (ramp value)": {**r, "takeoff_cg_pct_mac": round(cg(ramp - 200), 2),
            "landing_cg_pct_mac": round(cg(ramp - 2800), 2), "landing_within_limits": True},
            "taxi fuel not deducted": {**r, "takeoff_weight_lb": r["takeoff_weight_lb"] + 200,
            "landing_weight_lb": r["landing_weight_lb"] + 200}}


def t05():
    s = _sol("05-rainflow-fatigue-life")
    r = {k: v for k, v in s.solve().items() if not k.startswith("_")}
    rv = s.reversals(s.HISTORY)
    d = 0.0
    for a, b in zip(rv, rv[1:]):
        q = s.sa_eq(max(a, b), min(a, b))
        if q >= s.S_CUTOFF:
            d += 0.5 / (q / s.A_SN) ** (1 / s.B_SN)
    out = {"reversals counted in order as half cycles (GAG cycle missed)":
           {"cycles_per_flight": 6, "largest_cycle_max_ksi": 24, "largest_cycle_min_ksi": 9,
            "damage_per_flight": d, "life_flights": round(1 / d)}}
    d2 = 0.0
    for c in s.solve()["_cycles"]:
        q = (c[0] - c[1]) / 2
        if q >= s.S_CUTOFF:
            d2 += 1 / (q / s.A_SN) ** (1 / s.B_SN)
    out["no Goodman mean-stress correction"] = {**r, "damage_per_flight": d2, "life_flights": round(1 / d2)}
    return out


def t06():
    s = _sol("06-takeoff-true-wind")
    r = s.solve()
    out = {}
    for label, wind_mag in [("METAR wind treated as magnetic", 260.0), ("variation applied the wrong way", 275.0)]:
        hw = 14 * math.cos(math.radians(wind_mag - 178))
        gr, tot = s.corrected(1750.0, hw)
        out[label] = {"pressure_altitude_ft": 1750, "headwind_component_kt": round(hw, 2), "ground_roll_ft": round(gr),
                      "total_over_50ft_ft": round(tot), "required_runway_ft": round(tot * 1.25),
                      "meets_company_rule": tot * 1.25 <= 2500}
    gr0, tot0 = s.table_at(1750.0, 27.0)
    f = 1 - 0.1 * r["headwind_component_kt"] / 9
    tot_bad = tot0 * f * 1.15
    out["grass +15% of total distance"] = {**r, "total_over_50ft_ft": round(tot_bad), "required_runway_ft": round(tot_bad * 1.25),
                                           "meets_company_rule": tot_bad * 1.25 <= 2500}
    out["NOTAM missed: published 2,700 ft used instead of 2,500 ft TORA"] = {**r, "meets_company_rule": r["required_runway_ft"] <= 2700}
    return out


def t07():
    s = _sol("07-gust-light-weight")
    r = s.solve()
    return {"VA not reduced at light weight": {**r, "va_min_weight_keas": 130.0},
            "assumed heavy weight is critical": {**r, "n_gust_min_weight": r["n_gust_max_weight"],
                                                 "design_n_min_weight": 3.8, "governing_min_weight": "maneuver"}}


def t08():
    s = _sol("08-eccentric-mixed-bolt-group")
    p, x = s.P_ULT, s.X_LOAD
    t = p * (x - 1.5)
    j = 6 * 1.5 ** 2 + 4 * 2.5 ** 2
    f = math.hypot(t * 2.5 / j, p / 6 + t * 1.5 / j)
    ms = s.FSU * math.pi / 4 * s.D_RIGHT ** 2 / f - 1
    return {"bolts treated as equal (geometric centroid)": {"centroid_x_in": 1.5, "eccentricity_in": x - 1.5, "critical_bolt": "R1",
            "critical_bolt_load_lbf": round(f, 1), "min_ms": round(ms, 4), "verdict": "fail"},
            "most-loaded bolt taken as critical": {**s.solve(), "critical_bolt": "L1", "critical_bolt_load_lbf": 2862.3, "min_ms": 0.6292}}


def t09():
    s = _sol("09-inverted-taper-spar-web")
    out = {}
    for label, v in [("textbook Resal relief applied (wrong sign for this taper)", s.V - 2 * s.M / s.H * s.SLOPE),
                     ("taper ignored", s.V)]:
        tau = v / (s.H * s.T_WEB)
        ms = s.FSU / tau - 1
        out[label] = {"web_shear_lbf": round(v, 1), "web_tau_psi": round(tau), "ms": round(ms, 4),
                      "verdict": "pass" if ms >= 0 else "fail"}
    return out


def t10():
    s = _sol("10-z-section-unsymmetric-bending")
    r = s.solve()
    ix = r["ix_in4"]
    simple = {k: round(-s.MOMENT * y / ix) for k, (x, y) in s.POINTS.items()}
    return {"sigma = My/I (product of inertia ignored)": {**r, "ixy_in4": 0.0, "stress_A_psi": simple["A"], "stress_B_psi": simple["B"],
            "stress_C_psi": simple["C"], "stress_D_psi": simple["D"], "max_abs_stress_psi": max(abs(v) for v in simple.values())},
            "unsymmetric formula with the sign of Ixy flipped": {**r, "stress_A_psi": r["stress_B_psi"] - r["stress_A_psi"] + r["stress_B_psi"],
            "stress_B_psi": r["stress_B_psi"]}}


TRAPS = {"09": t09, "10": t10, "01": t01, "02": t02, "03": t03, "04": t04, "05": t05, "06": t06, "07": t07, "08": t08}


def traps_for(task_id):
    out = TRAPS[task_id[:2]]()
    return {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in out.items()}

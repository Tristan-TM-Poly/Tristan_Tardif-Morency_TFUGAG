from __future__ import annotations

from dataclasses import dataclass
from math import pi, e as EULER, sqrt


@dataclass(frozen=True)
class ConstantEntry:
    key: str
    symbol: str
    name: str
    domain: str
    value: float | str
    unit: str
    status: str
    formula: str = ""


@dataclass(frozen=True)
class UnknownConstantSlot:
    key: str
    symbol: str
    name: str
    domain: str
    constraints: tuple[str, ...]
    candidate_family: str


class TFUGAConstantAtlas:
    def constants(self) -> tuple[ConstantEntry, ...]:
        return (
            ConstantEntry("c", "c", "speed of light", "SI", 299792458.0, "m/s", "exact"),
            ConstantEntry("h", "h", "Planck constant", "SI", 6.62607015e-34, "J s", "exact"),
            ConstantEntry("e", "e", "elementary charge", "SI", 1.602176634e-19, "C", "exact"),
            ConstantEntry("k_B", "k_B", "Boltzmann constant", "SI", 1.380649e-23, "J/K", "exact"),
            ConstantEntry("N_A", "N_A", "Avogadro constant", "SI", 6.02214076e23, "mol^-1", "exact"),
            ConstantEntry("G", "G", "Newtonian gravitational constant", "gravity", 6.67430e-11, "m^3 kg^-1 s^-2", "measured"),
            ConstantEntry("alpha", "alpha", "fine-structure constant", "dimensionless", 7.2973525643e-3, "1", "measured"),
            ConstantEntry("m_e", "m_e", "electron mass", "particle", 9.1093837139e-31, "kg", "measured"),
            ConstantEntry("H0", "H_0", "Hubble constant Planck seed", "cosmology", 67.4, "km/s/Mpc", "model_fit"),
            ConstantEntry("Omega_m", "Omega_m", "matter density parameter", "cosmology", 0.315, "1", "model_fit"),
            ConstantEntry("pi", "pi", "pi", "math", pi, "1", "exact"),
            ConstantEntry("phi", "phi", "golden ratio", "math", (1 + sqrt(5)) / 2, "1", "exact"),
        )

    def unknown_slots(self) -> tuple[UnknownConstantSlot, ...]:
        return (
            UnknownConstantSlot("dark_matter_mass", "m_DM", "dark matter mass/coupling", "cosmology", ("positive", "fits relic density"), "symmetry gap"),
            UnknownConstantSlot("dark_energy_w", "w(z)", "dark energy equation of state", "cosmology", ("near -1 today", "fits CMB/BAO/SN"), "fractal vacuum action"),
            UnknownConstantSlot("quantum_gravity_scale", "Lambda_QG", "quantum gravity scale", "gravity", ("Planck domain", "recover GR/QFT"), "HGFM curvature residue"),
        )

    def by_key(self) -> dict[str, ConstantEntry]:
        return {c.key: c for c in self.constants()}

    def derived(self) -> dict[str, float]:
        c = self.by_key()
        h = float(c["h"].value)
        speed = float(c["c"].value)
        g = float(c["G"].value)
        hbar = h / (2 * pi)
        return {
            "hbar": hbar,
            "planck_length": sqrt(hbar * g / speed**3),
            "planck_time": sqrt(hbar * g / speed**5),
            "planck_mass": sqrt(hbar * speed / g),
            "gas_constant": float(c["N_A"].value) * float(c["k_B"].value),
        }

    def dimensionless_targets(self) -> tuple[ConstantEntry, ...]:
        return tuple(c for c in self.constants() if c.unit == "1")

    def markdown(self) -> str:
        lines = ["# TFUGA Constant Atlas", "", "mode: known_derived_unknown_oak", ""]
        for c in self.constants():
            lines.append(f"- `{c.symbol}` {c.name}: `{c.value}` `{c.unit}` status `{c.status}`")
        lines.append("\n## Unknown slots")
        for u in self.unknown_slots():
            lines.append(f"- `{u.symbol}` {u.name}: {u.candidate_family}")
        lines.append("\nOAK invariant: constants -> formulas -> candidates -> falsifiable predictions -> official comparison")
        return "\n".join(lines) + "\n"

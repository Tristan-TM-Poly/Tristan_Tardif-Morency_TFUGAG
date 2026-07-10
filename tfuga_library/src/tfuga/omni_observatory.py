from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev


@dataclass(frozen=True)
class BandSet:
    name: str
    bands: dict[str, tuple[float, ...]]


@dataclass(frozen=True)
class Spectrum:
    name: str
    wavelength: tuple[float, ...]
    flux: tuple[float, ...]


@dataclass(frozen=True)
class FeatureReport:
    name: str
    kind: str
    features: dict[str, float]
    oak_score: float


class AITOmniObservatory:
    def sources(self) -> tuple[str, ...]:
        return (
            "NASA Earthdata",
            "Copernicus Data Space",
            "USGS Landsat",
            "MAST",
            "SDSS",
            "ESA Gaia",
        )

    def stats(self, values: tuple[float, ...]) -> dict[str, float]:
        data = tuple(float(v) for v in values)
        if not data:
            return {"mean": 0.0, "std": 0.0}
        return {"mean": round(mean(data), 6), "std": round(pstdev(data), 6) if len(data) > 1 else 0.0}

    def nd(self, a: tuple[float, ...], b: tuple[float, ...]) -> float:
        vals = []
        for x, y in zip(a, b):
            denom = x + y
            if abs(denom) > 1e-12:
                vals.append((x - y) / denom)
        return round(mean(vals), 6) if vals else 0.0

    def image(self, image: BandSet) -> FeatureReport:
        features: dict[str, float] = {}
        for band, values in image.bands.items():
            for key, value in self.stats(values).items():
                features[f"{band}_{key}"] = value
        if "nir" in image.bands and "red" in image.bands:
            features["ndvi"] = self.nd(image.bands["nir"], image.bands["red"])
        if "green" in image.bands and "nir" in image.bands:
            features["ndwi"] = self.nd(image.bands["green"], image.bands["nir"])
        if "nir" in image.bands and "swir" in image.bands:
            features["nbr"] = self.nd(image.bands["nir"], image.bands["swir"])
        return FeatureReport(image.name, "image", features, min(10.0, len(features)))

    def spectrum(self, spectrum: Spectrum) -> FeatureReport:
        if len(spectrum.wavelength) != len(spectrum.flux) or not spectrum.flux:
            return FeatureReport(spectrum.name, "spectrum", {"valid": 0.0}, 0.0)
        flux = tuple(float(v) for v in spectrum.flux)
        wave = tuple(float(v) for v in spectrum.wavelength)
        peak = wave[flux.index(max(flux))]
        area = sum((wave[i] - wave[i - 1]) * (flux[i] + flux[i - 1]) * 0.5 for i in range(1, len(wave)))
        features = {"peak_wavelength": round(peak, 6), "integrated_flux": round(area, 6), **self.stats(flux)}
        return FeatureReport(spectrum.name, "spectrum", features, min(10.0, len(features) * 2.0))

    def markdown(self, images: tuple[BandSet, ...], spectra: tuple[Spectrum, ...]) -> str:
        lines = ["# AIT Omni Observatory", "", "mode: open_data_analysis_packet", ""]
        for report in [self.image(item) for item in images] + [self.spectrum(item) for item in spectra]:
            lines.append(f"- `{report.name}` kind `{report.kind}` oak `{report.oak_score}`")
        return "\n".join(lines).strip() + "\n"

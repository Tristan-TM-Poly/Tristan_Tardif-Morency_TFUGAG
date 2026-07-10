from tfuga.omni_observatory import AITOmniObservatory, BandSet, Spectrum


def test_omni_observatory_image_and_spectrum():
    p = AITOmniObservatory()
    image = p.image(BandSet("img", {"nir": (0.5, 0.6), "red": (0.1, 0.2), "green": (0.2, 0.25)}))
    spectrum = p.spectrum(Spectrum("spec", (1, 2, 3), (1, 3, 2)))
    assert image.features["ndvi"] > 0
    assert spectrum.features["peak_wavelength"] == 2
    assert "NASA Earthdata" in p.sources()

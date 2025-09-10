from backend.utils.image_utils import choose_contrast_color


def test_contrast_dark():
    fill, stroke = choose_contrast_color((10, 10, 10))
    assert fill == "#ffffff"
    assert stroke == "#000000"


def test_contrast_light():
    fill, stroke = choose_contrast_color((240, 240, 240))
    assert fill == "#000000"
    assert stroke == "#ffffff"

# Shared fixtures, available to every test in the project.
# pytest auto-discovers this file by name

from types import SimpleNamespace
import pytest
from ninja_jwt.tokens import RefreshToken

from apps.game.models import Layer, Level, LevelType, Mascot
from apps.game.models import Unit
from apps.users.models import User


@pytest.fixture
def user(db):
    
    return User.objects.create_user(email="player@example.com", password="pw12345678")


@pytest.fixture
def admin(db): # creates supseruser with every perm

    return User.objects.create_superuser(email="admin@example.com", password="pw12345678")


@pytest.fixture
def auth_headers(user):
   
    token = RefreshToken.for_user(user).access_token
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

@pytest.fixture
def unit_typing():
    return Unit.objects.create(sort_order=1, layer=Layer.TYPING, title = "Typing Journey", title_font_size = 24, background_asset_path = "bg_typing.png")
@pytest.fixture
def unit_ed_1():
    return Unit.objects.create(sort_order = 1, layer = Layer.EDUCATION, title = "LEVEL 1",title_font_size = 24, background_asset_path = "bg_ed1.png")
@pytest.fixture
def unit_ed_2():
    return Unit.objects.create(sort_order = 2, layer = Layer.EDUCATION, title = "LEVEL 2",title_font_size = 24, background_asset_path = "bg_ed2.png")

@pytest.fixture
def mascot_camel():
    return Mascot.objects.create(name = "Camel", idle_asset_path = "camel_idle.png", zero_star_asset_path = "camel_0.png", one_star_asset_path = "camel_1.png", two_star_asset_path = "camel_2.png", three_star_asset_path = "camel_3.png")

@pytest.fixture
def mascot_sheep():
    return Mascot.objects.create(name = "sheep", idle_asset_path = "sheep_idle.png", zero_star_asset_path = "sheep_0.png", one_star_asset_path = "sheep_1.png", two_star_asset_path = "sheep_2.png", three_star_asset_path = "sheep_3.png")

# --- Levels ---

@pytest.fixture
def level_typing_desert(unit_typing, mascot_camel):
    return Level.objects.create(
        sort_order=1,
        unit=unit_typing,
        layer=Layer.TYPING,
        title="TAKLAMAKAN DESERT",
        level_type="typing-desert",
        level_props={},
        mascot=mascot_camel,
        splash_background_asset_path="typing-levels/typing-level/background-taklamakan",  # truncated in screenshot
        splash_button_color=12868116,
        splash_button_text_color=16769724,
        splash_level_font_color=13205828,
        splash_level_title_color=7029022,
        show_mascot_on_splash=True,
    )


@pytest.fixture
def level_typing_sandstorm(unit_typing, mascot_camel):
    return Level.objects.create(
        sort_order=2,
        unit=unit_typing,
        layer=Layer.TYPING,
        title="TAKLAMAKAN SANDSTORM",
        level_type="typing-sandstorm",
        level_props={},
        mascot=mascot_camel,
        splash_background_asset_path="typing-levels/typing-level/background-sandstorm",  # truncated in screenshot
        splash_button_color=12868116,
        splash_button_text_color=16769724,
        splash_level_font_color=12868116,
        splash_level_title_color=7029022,
        show_mascot_on_splash=False,
    )


@pytest.fixture
def level_ed1_letter_grid(unit_ed_1, mascot_sheep):
    return Level.objects.create(
        sort_order=1,
        unit=unit_ed_1,
        layer=Layer.EDUCATION,
        title=None,
        level_type=LevelType.EDUCATION_LETTER_GRID,  # "education-letter-grid"
        level_props={"letters": ["ئا", "ئە", "ب"]},  # PLACEHOLDER — real array truncated in screenshot
        mascot=mascot_sheep,
        splash_background_asset_path="education-levels/education-level-map/background",  # truncated
        splash_button_color=7903299,
        splash_button_text_color=16777215,
        splash_level_font_color=16777215,
        splash_level_title_color=16777215,
        show_mascot_on_splash=True,
    )


@pytest.fixture
def level_ed1_bubble(unit_ed_1, mascot_sheep):
    return Level.objects.create(
        sort_order=2,
        unit=unit_ed_1,
        layer=Layer.EDUCATION,
        title=None,
        level_type="education-bubble",
        level_props={"letters": ["ئا", "ئە", "ب"]},  # PLACEHOLDER — real array truncated in screenshot
        mascot=mascot_sheep,
        splash_background_asset_path="education-levels/education-level-map/background",  # truncated
        splash_button_color=7903299,
        splash_button_text_color=16777215,
        splash_level_font_color=16777215,
        splash_level_title_color=16777215,
        show_mascot_on_splash=True,
    )


@pytest.fixture
def level_ed2_letter_grid(unit_ed_2, mascot_sheep):
    return Level.objects.create(
        sort_order=1,
        unit=unit_ed_2,
        layer=Layer.EDUCATION,
        title=None,
        level_type=LevelType.EDUCATION_LETTER_GRID,  # "education-letter-grid"
        level_props={"letters": ["ج", "چ", "خ"]},  # PLACEHOLDER — real array truncated in screenshot
        mascot=mascot_sheep,
        splash_background_asset_path="education-levels/education-level-map/background",  # truncated
        splash_button_color=4889428,
        splash_button_text_color=16777215,
        splash_level_font_color=16777215,
        splash_level_title_color=16777215,
        show_mascot_on_splash=False,
    )



# -- seeded set --
@pytest.fixture
def seed(
    user,
    auth_headers,
    unit_typing,
    unit_ed_1,
    unit_ed_2,
    mascot_camel,
    mascot_sheep,
    level_typing_desert,
    level_typing_sandstorm,
    level_ed1_letter_grid,
    level_ed1_bubble,
    level_ed2_letter_grid,
):
    return SimpleNamespace(
        user=user,
        auth_headers=auth_headers,
        unit_typing=unit_typing,
        unit_ed_1=unit_ed_1,
        unit_ed_2=unit_ed_2,
        mascot_camel=mascot_camel,
        mascot_sheep=mascot_sheep,
        level_typing_desert=level_typing_desert,
        level_typing_sandstorm=level_typing_sandstorm,
        level_ed1_letter_grid=level_ed1_letter_grid,
        level_ed1_bubble=level_ed1_bubble,
        level_ed2_letter_grid=level_ed2_letter_grid,
    )
    


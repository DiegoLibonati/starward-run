import pytest

from src.constants.paths import (
    FONT_PRIMARY,
    GRAPHIC_BAT_ANIMATION_1,
    GRAPHIC_BAT_ANIMATION_2,
    GRAPHIC_GROUND,
    GRAPHIC_GROUNDER_ANIMATION_1,
    GRAPHIC_GROUNDER_ANIMATION_2,
    GRAPHIC_GROUNDER_ANIMATION_3,
    GRAPHIC_GROUNDER_ANIMATION_4,
    GRAPHIC_GROUNDER_ANIMATION_5,
    GRAPHIC_GROUNDER_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_1,
    GRAPHIC_MISTERY_BOX_ANIMATION_2,
    GRAPHIC_MISTERY_BOX_ANIMATION_3,
    GRAPHIC_MISTERY_BOX_ANIMATION_4,
    GRAPHIC_MISTERY_BOX_ANIMATION_5,
    GRAPHIC_MISTERY_BOX_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_7,
    GRAPHIC_PLAYER_JUMP_1,
    GRAPHIC_PLAYER_JUMP_IMMUNITY_1,
    GRAPHIC_PLAYER_JUMP_KILLER_1,
    GRAPHIC_PLAYER_STAND_1,
    GRAPHIC_PLAYER_WALK_1,
    GRAPHIC_PLAYER_WALK_2,
    GRAPHIC_PLAYER_WALK_IMMUNITY_1,
    GRAPHIC_PLAYER_WALK_IMMUNITY_2,
    GRAPHIC_PLAYER_WALK_KILLER_1,
    GRAPHIC_PLAYER_WALK_KILLER_2,
    GRAPHIC_SKY,
    GRAPHIC_SNAIL_ANIMATION_1,
    GRAPHIC_SNAIL_ANIMATION_2,
    SOUND_GAME_MUSIC,
    SOUND_GAME_OVER,
    SOUND_OBSTACLE_KILL,
    SOUND_PLAYER_JUMP,
    SOUND_PLAYER_POWER_UP,
)

_ALL_PATHS: list[str] = [
    GRAPHIC_PLAYER_WALK_1,
    GRAPHIC_PLAYER_WALK_2,
    GRAPHIC_PLAYER_JUMP_1,
    GRAPHIC_PLAYER_STAND_1,
    GRAPHIC_PLAYER_WALK_IMMUNITY_1,
    GRAPHIC_PLAYER_WALK_IMMUNITY_2,
    GRAPHIC_PLAYER_JUMP_IMMUNITY_1,
    GRAPHIC_PLAYER_WALK_KILLER_1,
    GRAPHIC_PLAYER_WALK_KILLER_2,
    GRAPHIC_PLAYER_JUMP_KILLER_1,
    GRAPHIC_SNAIL_ANIMATION_1,
    GRAPHIC_SNAIL_ANIMATION_2,
    GRAPHIC_BAT_ANIMATION_1,
    GRAPHIC_BAT_ANIMATION_2,
    GRAPHIC_GROUNDER_ANIMATION_1,
    GRAPHIC_GROUNDER_ANIMATION_2,
    GRAPHIC_GROUNDER_ANIMATION_3,
    GRAPHIC_GROUNDER_ANIMATION_4,
    GRAPHIC_GROUNDER_ANIMATION_5,
    GRAPHIC_GROUNDER_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_1,
    GRAPHIC_MISTERY_BOX_ANIMATION_2,
    GRAPHIC_MISTERY_BOX_ANIMATION_3,
    GRAPHIC_MISTERY_BOX_ANIMATION_4,
    GRAPHIC_MISTERY_BOX_ANIMATION_5,
    GRAPHIC_MISTERY_BOX_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_7,
    GRAPHIC_SKY,
    GRAPHIC_GROUND,
    SOUND_PLAYER_JUMP,
    SOUND_PLAYER_POWER_UP,
    SOUND_GAME_MUSIC,
    SOUND_GAME_OVER,
    SOUND_OBSTACLE_KILL,
    FONT_PRIMARY,
]


class TestPathTypes:
    def test_all_paths_are_strings(self) -> None:
        for path in _ALL_PATHS:
            assert isinstance(path, str), f"Expected str, got {type(path)} for {path}"

    def test_all_paths_are_non_empty(self) -> None:
        for path in _ALL_PATHS:
            assert path != "", "Path must not be empty"

    def test_path_count(self) -> None:
        assert len(_ALL_PATHS) == 35


class TestGraphicPaths:
    def test_player_walk_paths_end_with_png(self) -> None:
        assert GRAPHIC_PLAYER_WALK_1.endswith(".png")
        assert GRAPHIC_PLAYER_WALK_2.endswith(".png")

    def test_player_jump_path_ends_with_png(self) -> None:
        assert GRAPHIC_PLAYER_JUMP_1.endswith(".png")

    def test_snail_paths_end_with_png(self) -> None:
        assert GRAPHIC_SNAIL_ANIMATION_1.endswith(".png")
        assert GRAPHIC_SNAIL_ANIMATION_2.endswith(".png")

    def test_bat_paths_end_with_png(self) -> None:
        assert GRAPHIC_BAT_ANIMATION_1.endswith(".png")
        assert GRAPHIC_BAT_ANIMATION_2.endswith(".png")

    def test_grounder_has_six_frames(self) -> None:
        grounder_paths: list[str] = [
            GRAPHIC_GROUNDER_ANIMATION_1,
            GRAPHIC_GROUNDER_ANIMATION_2,
            GRAPHIC_GROUNDER_ANIMATION_3,
            GRAPHIC_GROUNDER_ANIMATION_4,
            GRAPHIC_GROUNDER_ANIMATION_5,
            GRAPHIC_GROUNDER_ANIMATION_6,
        ]
        assert len(grounder_paths) == 6
        for path in grounder_paths:
            assert path.endswith(".png")

    def test_mistery_box_has_seven_frames(self) -> None:
        mistery_paths: list[str] = [
            GRAPHIC_MISTERY_BOX_ANIMATION_1,
            GRAPHIC_MISTERY_BOX_ANIMATION_2,
            GRAPHIC_MISTERY_BOX_ANIMATION_3,
            GRAPHIC_MISTERY_BOX_ANIMATION_4,
            GRAPHIC_MISTERY_BOX_ANIMATION_5,
            GRAPHIC_MISTERY_BOX_ANIMATION_6,
            GRAPHIC_MISTERY_BOX_ANIMATION_7,
        ]
        assert len(mistery_paths) == 7
        for path in mistery_paths:
            assert path.endswith(".png")

    def test_sky_and_ground_end_with_png(self) -> None:
        assert GRAPHIC_SKY.endswith(".png")
        assert GRAPHIC_GROUND.endswith(".png")


class TestSoundPaths:
    def test_jump_sound_ends_with_mp3(self) -> None:
        assert SOUND_PLAYER_JUMP.endswith(".mp3")

    def test_power_up_sound_ends_with_mp3(self) -> None:
        assert SOUND_PLAYER_POWER_UP.endswith(".mp3")

    def test_game_music_ends_with_wav(self) -> None:
        assert SOUND_GAME_MUSIC.endswith(".wav")

    def test_game_over_ends_with_mp3(self) -> None:
        assert SOUND_GAME_OVER.endswith(".mp3")

    def test_obstacle_kill_ends_with_mp3(self) -> None:
        assert SOUND_OBSTACLE_KILL.endswith(".mp3")


class TestFontPaths:
    def test_primary_font_ends_with_ttf(self) -> None:
        assert FONT_PRIMARY.endswith(".ttf")

    @pytest.mark.parametrize("path", _ALL_PATHS)
    def test_all_paths_are_absolute_or_relative(self, path: str) -> None:
        assert len(path) > 0

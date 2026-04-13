import pytest

from src.constants import paths


class TestPaths:
    @pytest.mark.unit
    def test_graphic_player_walk_1_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_PLAYER_WALK_1, str)

    @pytest.mark.unit
    def test_graphic_player_walk_2_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_PLAYER_WALK_2, str)

    @pytest.mark.unit
    def test_graphic_player_jump_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_PLAYER_JUMP_1, str)

    @pytest.mark.unit
    def test_graphic_player_stand_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_PLAYER_STAND_1, str)

    @pytest.mark.unit
    def test_graphic_snail_frames_are_strings(self) -> None:
        assert isinstance(paths.GRAPHIC_SNAIL_ANIMATION_1, str)
        assert isinstance(paths.GRAPHIC_SNAIL_ANIMATION_2, str)

    @pytest.mark.unit
    def test_graphic_bat_frames_are_strings(self) -> None:
        assert isinstance(paths.GRAPHIC_BAT_ANIMATION_1, str)
        assert isinstance(paths.GRAPHIC_BAT_ANIMATION_2, str)

    @pytest.mark.unit
    def test_graphic_grounder_has_six_frames(self) -> None:
        grounder_paths: list[str] = [
            paths.GRAPHIC_GROUNDER_ANIMATION_1,
            paths.GRAPHIC_GROUNDER_ANIMATION_2,
            paths.GRAPHIC_GROUNDER_ANIMATION_3,
            paths.GRAPHIC_GROUNDER_ANIMATION_4,
            paths.GRAPHIC_GROUNDER_ANIMATION_5,
            paths.GRAPHIC_GROUNDER_ANIMATION_6,
        ]
        assert len(grounder_paths) == 6
        assert all(isinstance(p, str) for p in grounder_paths)

    @pytest.mark.unit
    def test_graphic_mistery_box_has_seven_frames(self) -> None:
        box_paths: list[str] = [
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_1,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_2,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_3,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_4,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_5,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_6,
            paths.GRAPHIC_MISTERY_BOX_ANIMATION_7,
        ]
        assert len(box_paths) == 7
        assert all(isinstance(p, str) for p in box_paths)

    @pytest.mark.unit
    def test_graphic_sky_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_SKY, str)

    @pytest.mark.unit
    def test_graphic_ground_is_string(self) -> None:
        assert isinstance(paths.GRAPHIC_GROUND, str)

    @pytest.mark.unit
    def test_sound_player_jump_is_string(self) -> None:
        assert isinstance(paths.SOUND_PLAYER_JUMP, str)

    @pytest.mark.unit
    def test_sound_player_power_up_is_string(self) -> None:
        assert isinstance(paths.SOUND_PLAYER_POWER_UP, str)

    @pytest.mark.unit
    def test_sound_game_music_is_string(self) -> None:
        assert isinstance(paths.SOUND_GAME_MUSIC, str)

    @pytest.mark.unit
    def test_sound_game_over_is_string(self) -> None:
        assert isinstance(paths.SOUND_GAME_OVER, str)

    @pytest.mark.unit
    def test_sound_obstacle_kill_is_string(self) -> None:
        assert isinstance(paths.SOUND_OBSTACLE_KILL, str)

    @pytest.mark.unit
    def test_font_primary_is_string(self) -> None:
        assert isinstance(paths.FONT_PRIMARY, str)

    @pytest.mark.unit
    def test_all_graphic_paths_contain_assets(self) -> None:
        graphic_paths: list[str] = [
            paths.GRAPHIC_PLAYER_WALK_1,
            paths.GRAPHIC_SKY,
            paths.GRAPHIC_GROUND,
            paths.GRAPHIC_BAT_ANIMATION_1,
            paths.GRAPHIC_SNAIL_ANIMATION_1,
        ]
        assert all("assets" in p for p in graphic_paths)

    @pytest.mark.unit
    def test_all_sound_paths_contain_assets(self) -> None:
        sound_paths: list[str] = [
            paths.SOUND_PLAYER_JUMP,
            paths.SOUND_GAME_MUSIC,
            paths.SOUND_GAME_OVER,
            paths.SOUND_OBSTACLE_KILL,
        ]
        assert all("assets" in p for p in sound_paths)

    @pytest.mark.unit
    def test_immunity_walk_frames_differ_from_normal(self) -> None:
        assert paths.GRAPHIC_PLAYER_WALK_1 != paths.GRAPHIC_PLAYER_WALK_IMMUNITY_1

    @pytest.mark.unit
    def test_killer_walk_frames_differ_from_normal(self) -> None:
        assert paths.GRAPHIC_PLAYER_WALK_1 != paths.GRAPHIC_PLAYER_WALK_KILLER_1

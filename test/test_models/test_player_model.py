import pygame

from src.models.player_model import PlayerModel

_GROUND_Y: int = 300
_X_RIGHT_LIMIT: int = 735


class TestPlayerModelInit:
    def test_is_sprite(self, player: PlayerModel) -> None:
        assert isinstance(player, pygame.sprite.Sprite)

    def test_initial_gravity_is_zero(self, player: PlayerModel) -> None:
        assert player._gravity == 0

    def test_initial_walk_index_is_zero(self, player: PlayerModel) -> None:
        assert player._walk_index == 0.0

    def test_initial_position_midbottom(self, player: PlayerModel) -> None:
        assert player.rect.midbottom == (80, _GROUND_Y)

    def test_image_is_surface(self, player: PlayerModel) -> None:
        assert isinstance(player.image, pygame.Surface)

    def test_rect_is_rect(self, player: PlayerModel) -> None:
        assert isinstance(player.rect, pygame.Rect)

    def test_walk_frames_has_two_frames(self, player: PlayerModel) -> None:
        assert len(player._walk_frames) == 2

    def test_skins_has_three_entries(self, player: PlayerModel) -> None:
        assert set(player._skins.keys()) == {"normal", "immunity", "killer"}


class TestPlayerModelIsJump:
    def test_not_jumping_when_on_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y
        assert player.is_jump is False

    def test_is_jumping_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 10
        assert player.is_jump is True

    def test_is_jump_returns_bool(self, player: PlayerModel) -> None:
        assert isinstance(player.is_jump, bool)

    def test_boundary_on_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y
        assert player.is_jump is False

    def test_boundary_one_pixel_above(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 1
        assert player.is_jump is True


class TestPlayerModelApplyGravity:
    def test_gravity_increases_when_airborne(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 50
        player._gravity = 5
        player._apply_gravity()
        assert player._gravity == 6

    def test_gravity_resets_to_zero_on_landing(self, player: PlayerModel) -> None:
        player._gravity = 15
        player.rect.bottom = _GROUND_Y + 10
        player._apply_gravity()
        assert player._gravity == 0

    def test_player_clamped_to_ground_on_landing(self, player: PlayerModel) -> None:
        player._gravity = 15
        player.rect.bottom = _GROUND_Y + 10
        player._apply_gravity()
        assert player.rect.bottom == _GROUND_Y

    def test_player_moves_down_with_positive_gravity(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 100
        player._gravity = 5
        initial_y = player.rect.y
        player._apply_gravity()
        assert player.rect.y > initial_y

    def test_player_moves_up_with_negative_gravity(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 50
        player._gravity = -10
        initial_y = player.rect.y
        player._apply_gravity()
        assert player.rect.y < initial_y


class TestPlayerModelLimits:
    def test_clamps_left_boundary(self, player: PlayerModel) -> None:
        player.rect.x = -50
        player._limits()
        assert player.rect.x == 0

    def test_clamps_right_boundary(self, player: PlayerModel) -> None:
        player.rect.x = 900
        player._limits()
        assert player.rect.x == _X_RIGHT_LIMIT

    def test_does_not_clamp_within_bounds(self, player: PlayerModel) -> None:
        player.rect.x = 400
        player._limits()
        assert player.rect.x == 400

    def test_exactly_at_zero_is_not_clamped(self, player: PlayerModel) -> None:
        player.rect.x = 0
        player._limits()
        assert player.rect.x == 0

    def test_exactly_at_right_limit_is_not_clamped(self, player: PlayerModel) -> None:
        player.rect.x = _X_RIGHT_LIMIT
        player._limits()
        assert player.rect.x == _X_RIGHT_LIMIT


class TestPlayerModelChangeSkin:
    def test_change_to_immunity_updates_walk_frames(self, player: PlayerModel) -> None:
        player.change_skin_player("immunity")
        assert player._walk_frames is player._skins["immunity"][0]

    def test_change_to_immunity_updates_jump_frame(self, player: PlayerModel) -> None:
        player.change_skin_player("immunity")
        assert player._jump_frame is player._skins["immunity"][1]

    def test_change_to_killer_updates_walk_frames(self, player: PlayerModel) -> None:
        player.change_skin_player("killer")
        assert player._walk_frames is player._skins["killer"][0]

    def test_change_to_killer_updates_jump_frame(self, player: PlayerModel) -> None:
        player.change_skin_player("killer")
        assert player._jump_frame is player._skins["killer"][1]

    def test_change_to_normal_with_empty_string(self, player: PlayerModel) -> None:
        player.change_skin_player("killer")
        player.change_skin_player("")
        assert player._walk_frames is player._skins["normal"][0]

    def test_change_to_normal_explicitly(self, player: PlayerModel) -> None:
        player.change_skin_player("immunity")
        player.change_skin_player("normal")
        assert player._walk_frames is player._skins["normal"][0]

    def test_unknown_power_falls_back_to_normal(self, player: PlayerModel) -> None:
        player.change_skin_player("unknown_power")
        assert player._walk_frames is player._skins["normal"][0]

    def test_walk_frames_has_two_surfaces_after_change(self, player: PlayerModel) -> None:
        player.change_skin_player("immunity")
        assert len(player._walk_frames) == 2
        for frame in player._walk_frames:
            assert isinstance(frame, pygame.Surface)

from random import choice, randint
from sys import exit

import pygame

from src.configs.default_config import DefaultConfig
from src.constants.paths import (
    FONT_PRIMARY,
    GRAPHIC_GROUND,
    GRAPHIC_PLAYER_STAND_1,
    GRAPHIC_SKY,
    SOUND_GAME_MUSIC,
    SOUND_GAME_OVER,
    SOUND_OBSTACLE_KILL,
)
from src.constants.vars import get_obstacles
from src.models.player_model import PlayerModel
from src.models.power_model import PowerModel

# Display
_SCREEN_WIDTH: int = 800
_SCREEN_HEIGHT: int = 400
_FPS: int = 60
_GROUND_Y: int = 300
_FONT_SIZE: int = 50

# Colors
_COLOR_TITLE: tuple[int, int, int] = (111, 196, 169)
_COLOR_SCORE: tuple[int, int, int] = (64, 64, 64)
_COLOR_BG_MENU: tuple[int, int, int] = (94, 129, 162)

# Custom events
_EVENT_OBSTACLE: int = pygame.USEREVENT + 1
_EVENT_POWER: int = pygame.USEREVENT + 2

# Timers (ms)
_OBSTACLE_TIMER_MS: int = 1500
_POWER_TIMER_MIN_MS: int = 15000
_POWER_TIMER_MAX_MS: int = 30000

# Score thresholds to unlock obstacles
_SCORE_UNLOCK_BAT: int = 10
_SCORE_UNLOCK_GROUNDER: int = 20

# Audio
_BG_MUSIC_VOLUME: float = 0.1


class InterfaceGame:
    def __init__(self, config: DefaultConfig) -> None:
        pygame.init()

        self._config = config

        self._title: str = "StarwardRun"
        self._game_started: bool = False
        self._score: int = 0
        self._start_time: int = 0
        self._obstacles_spawn: set[str] = set()
        self._power: PowerModel | None = None

        pygame.display.set_caption(self._title)
        self._screen = pygame.display.set_mode((_SCREEN_WIDTH, _SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        self._player_single_group = pygame.sprite.GroupSingle()
        self._power_single_group = pygame.sprite.GroupSingle()
        self._obstacle_group = pygame.sprite.Group()
        self._bg_music: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_GAME_MUSIC)
        self._game_over_music: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_GAME_OVER)
        self._obstacle_kill: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_OBSTACLE_KILL)
        self._primary_font = pygame.font.Font(FONT_PRIMARY, _FONT_SIZE)

        self._player_stand_surface = pygame.transform.scale2x(pygame.image.load(GRAPHIC_PLAYER_STAND_1).convert_alpha())
        self._sky_surface = pygame.image.load(GRAPHIC_SKY).convert()
        self._ground_surface = pygame.image.load(GRAPHIC_GROUND).convert()
        self._game_title_surface = self._primary_font.render(self._title, False, _COLOR_TITLE)
        self._reset_game_surface = self._primary_font.render("Reset game with SPACE", False, _COLOR_TITLE)
        self._player_stand_surface_rect = self._player_stand_surface.get_rect(center=(_SCREEN_WIDTH // 2, 200))
        self._game_title_surface_rect = self._game_title_surface.get_rect(center=(_SCREEN_WIDTH // 2, 50))
        self._reset_game_surface_rect = self._reset_game_surface.get_rect(center=(_SCREEN_WIDTH // 2, 350))

        self._config_game()

    @property
    def title(self) -> str:
        return self._title

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    @property
    def game_started(self) -> bool:
        return self._game_started

    @property
    def score(self) -> int:
        return self._score

    @property
    def start_time(self) -> int:
        return self._start_time

    @property
    def obstacles_spawn(self) -> set[str]:
        return self._obstacles_spawn

    @property
    def player_single_group(self) -> pygame.sprite.GroupSingle:
        return self._player_single_group

    @property
    def player(self) -> PlayerModel | None:
        sprites = self._player_single_group.sprites()
        return sprites[0] if sprites else None

    @property
    def power_single_group(self) -> pygame.sprite.GroupSingle:
        return self._power_single_group

    @property
    def power(self) -> PowerModel | None:
        return self._power

    @property
    def obstacle_group(self) -> pygame.sprite.Group:
        return self._obstacle_group

    @property
    def clock(self) -> pygame.time.Clock:
        return self._clock

    def _config_game(self) -> None:
        self._bg_music.set_volume(_BG_MUSIC_VOLUME)
        self._set_custom_events()
        self._player_single_group.add(PlayerModel())

    def _set_custom_events(self) -> None:
        pygame.time.set_timer(_EVENT_OBSTACLE, _OBSTACLE_TIMER_MS)
        pygame.time.set_timer(_EVENT_POWER, randint(_POWER_TIMER_MIN_MS, _POWER_TIMER_MAX_MS))

    def _reset_game(self) -> None:
        self._obstacles_spawn = set()
        self._power = None
        self._power_single_group.empty()
        self._player_single_group.empty()
        self._player_single_group.add(PlayerModel())

    def _compute_score(self) -> int:
        return (pygame.time.get_ticks() - self._start_time) // 1000

    def _display_score(self) -> None:
        surface = self._primary_font.render(f"Score: {self._score}", False, _COLOR_SCORE)
        self._screen.blit(surface, surface.get_rect(center=(_SCREEN_WIDTH // 2, 50)))

    def _update_obstacle_pool(self) -> None:
        self._obstacles_spawn.add("snail")
        if self._score >= _SCORE_UNLOCK_BAT:
            self._obstacles_spawn.add("bat")
        if self._score >= _SCORE_UNLOCK_GROUNDER:
            self._obstacles_spawn.add("grounder")

    def _collision_sprite(self) -> bool:
        if self._power and self._power.current_power == "immunity":
            self._power.stop_power()
            return True

        if self._power and self._power.current_power == "killer":
            self._power.stop_power()
            colliding = pygame.sprite.spritecollide(self._player_single_group.sprite, self._obstacle_group, False)
            if colliding:
                self._obstacle_kill.play()
                colliding[0].kill()
                return True

        if pygame.sprite.spritecollide(self._player_single_group.sprite, self._obstacle_group, False):
            self._obstacle_group.empty()
            self._power_single_group.empty()
            self._game_over_music.play()
            self._bg_music.stop()
            return False

        return True

    def _render_menu(self) -> None:
        self._screen.fill(_COLOR_BG_MENU)
        self._screen.blit(self._player_stand_surface, self._player_stand_surface_rect)
        self._screen.blit(self._game_title_surface, self._game_title_surface_rect)
        self._screen.blit(self._reset_game_surface, self._reset_game_surface_rect)

        if self._score:
            final_score_surface = self._primary_font.render(f"Score: {self._score}", False, _COLOR_TITLE)
            self._screen.blit(
                final_score_surface,
                final_score_surface.get_rect(center=(_SCREEN_WIDTH // 2, 80)),
            )

    def _render_game(self) -> None:
        self._screen.blit(self._sky_surface, (0, 0))
        self._screen.blit(self._ground_surface, (0, _GROUND_Y))

        self._score = self._compute_score()
        self._display_score()

        self._player_single_group.draw(surface=self._screen)
        self._player_single_group.update()

        if self._power:
            self._player_single_group.sprite.change_skin_player(power=self._power.current_power)

        self._obstacle_group.draw(surface=self._screen)
        self._obstacle_group.update(score=self._score)

        self._power_single_group.draw(surface=self._screen)
        self._power_single_group.update(player=self._player_single_group)

        self._game_started = self._collision_sprite()

    def game_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if not self._game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._reset_game()
                    self._game_started = True
                    self._start_time = pygame.time.get_ticks()
                    self._bg_music.play(loops=-1)
                    self._game_over_music.stop()

                if self._game_started and event.type == _EVENT_OBSTACLE:
                    self._update_obstacle_pool()
                    obstacle = get_obstacles().get(choice(list(self._obstacles_spawn)))
                    self._obstacle_group.add(obstacle)

                if self._game_started and event.type == _EVENT_POWER:
                    self._power = PowerModel()
                    self._power_single_group.add(self._power)

            if self._game_started:
                self._render_game()
            else:
                self._render_menu()

            pygame.display.update()
            self._clock.tick(_FPS)

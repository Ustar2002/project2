#level.py

import pygame
from platform import Platform
from enemy import Enemy, EnemyType2
from puzzle import MovableBlock
from boss import Boss
from trap import Trap
from item import Item
from flag import Flag
from star import Star

class Level:
    def __init__(self, level_data, gravity_manager):
        self.gravity_manager = gravity_manager
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemies_type2 = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.puzzles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.flag = None
        self.boss = None
        self.stars = pygame.sprite.Group()  

        self.load_level(level_data)

    def load_level(self, level_data):
        # 플랫폼 로드
        for plat_data in level_data['platforms']:
            platform = Platform(*plat_data)
            self.platforms.add(platform)

        # 적 로드
        for enemy_data in level_data['enemies']:
            enemy = Enemy(enemy_data[0], enemy_data[1], self.gravity_manager)
            self.enemies.add(enemy)

        for enemy_data in level_data.get('enemies_type2', []):
            enemy = EnemyType2(enemy_data[0], enemy_data[1], self.gravity_manager)
            self.enemies_type2.add(enemy)

        # 아이템 로드
        for item_data in level_data.get('items', []):
            item = Item(item_data[0], item_data[1])
            self.items.add(item)

        # 퍼즐 블록 로드
        for puzzle_data in level_data['puzzles']:
            block = MovableBlock(*puzzle_data)
            self.puzzles.add(block)

        # 트랩 로드
        for trap_data in level_data.get('traps', []):
            trap = Trap(*trap_data)
            self.traps.add(trap)

        # 보스 로드
        if level_data.get('is_boss_level', False):
            boss_position = level_data.get('boss_position', (0, 0))
            self.boss = Boss(boss_position[0], boss_position[1], self.gravity_manager)

        # 깃발 로드
        if 'flag_position' in level_data:
            flag_position = level_data['flag_position']
            self.flag = Flag(flag_position[0], flag_position[1])

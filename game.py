import random
import math

class Player:
    def __init__(self, name, player_class, health, stamina, armor, damage, experience):
        self.name = name
        self.player_class = player_class
        self.health = health
        self.stamina = stamina
        self.armor = armor
        self.damage = damage
        self.experience = experience
        self.x = 1  # Начальная координата X
        self.y = 1  # Начальная координата Y

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y

    def attack(self, enemy):
        damage_dealt = self.damage - enemy.get_damage_reduction()
        if damage_dealt > 0:
            enemy.take_damage(damage_dealt)
        print(f"{self.name} нанес {damage_dealt} урона {enemy.name}. Оставшееся здоровье: {enemy.health}")

    def take_damage(self, damage):
        damage_received = damage - self.get_damage_reduction(damage)
        if damage_received > 0:
            self.health -= damage_received
        print(f"{self.name} получил {damage_received} урона. Оставшееся здоровье: {self.health}")

    def get_damage_reduction(self, damage):
        k = 0.1  # Коэффициент уменьшающейся эффективности
        return damage * (1 - math.exp(-k * self.armor))

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Класс: {self.player_class}\n"
                f"Здоровье: {self.health}\n"
                f"Выносливость: {self.stamina}\n"
                f"Броня: {self.armor}\n"
                f"Урон: {self.damage}\n"
                f"Опыт: {self.experience}")

class Enemy:
    def __init__(self, name, health, armor, damage):
        self.name = name
        self.health = health
        self.armor = armor
        self.damage = damage
        self.x = 0
        self.y = 0

    def attack(self, player):
        damage_dealt = self.damage - player.get_damage_reduction(self.damage)
        if damage_dealt > 0:
            player.take_damage(damage_dealt)
        print(f"{self.name} нанес {damage_dealt} урона {player.name}. Оставшееся здоровье: {player.health}")

    def take_damage(self, damage):
        damage_received = damage - self.get_damage_reduction(damage)
        if damage_received > 0:
            self.health -= damage_received
        print(f"{self.name} получил {damage_received} урона. Оставшееся здоровье: {self.health}")

    def get_damage_reduction(self, damage):
        k = 0.1  # Коэффициент уменьшающейся эффективности
        return damage * (1 - math.exp(-k * self.armor))

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name} (Здоровье: {self.health}, Броня: {self.armor}, Урон: {self.damage})"

def generate_map(width, height, wall_probability=0.1):
    """
    Генерирует карту заданного размера с указанным процентом стен,
    ограниченную стенами по всем бокам.
    
    :param width: ширина карты (внутренняя часть)
    :param height: высота карты (внутренняя часть)
    :param wall_probability: вероятность появления стены в каждой клетке внутренней части
    :return: двумерный список, представляющий карту
    """
    # Создаем верхнюю и нижнюю границы карты
    top_bottom_border = ['#'] * (width + 2)
    
    # Создаем внутреннюю часть карты
    map_ = [top_bottom_border]
    for _ in range(height):
        row = ['#']
        for _ in range(width):
            if random.random() < wall_probability:
                row.append('#')
            else:
                row.append('.')
        row.append('#')
        map_.append(row)
    map_.append(top_bottom_border)
    
    return map_

def place_player_on_map(player, game_map):
    """
    Размещает игрока на карте.
    
    :param player: объект Player
    :param game_map: двумерный список, представляющий карту
    """
    game_map[player.y][player.x] = 'P'

def place_enemies_on_map(enemies, game_map):
    """
    Размещает врагов на карте.
    
    :param enemies: список объектов Enemy
    :param game_map: двумерный список, представляющий карту
    """
    for enemy in enemies:
        placed = False
        while not placed:
            x = random.randint(1, len(game_map[0]) - 2)
            y = random.randint(1, len(game_map) - 2)
            if game_map[y][x] == '.':
                game_map[y][x] = 'E'
                enemy.x = x
                enemy.y = y
                placed = True

def print_map(map_, player_info):
    """
    Печатает карту и информацию о игроке в консоли.
    
    :param map_: двумерный список, представляющий карту
    :param player_info: строка с информацией о игроке
    """
    max_map_height = len(map_)
    player_info_lines = player_info.split('\n')
    max_info_height = len(player_info_lines)
    
    for i in range(max_map_height):
        map_row = ''.join(map_[i])
        info_row = player_info_lines[i] if i < max_info_height else ''
        print(f"{map_row} | {info_row}")

def clear_player_from_map(player, game_map):
    """
    Удаляет игрока с текущей позиции на карте.
    
    :param player: объект Player
    :param game_map: двумерный список, представляющий карту
    """
    game_map[player.y][player.x] = '.'

def clear_enemy_from_map(enemy, game_map):
    """
    Удаляет врага с текущей позиции на карте.
    
    :param enemy: объект Enemy
    :param game_map: двумерный список, представляющий карту
    """
    game_map[enemy.y][enemy.x] = '.'

def choose_class():
    """
    Позволяет игроку выбрать класс.
    
    :return: выбранный класс и бонусы
    """
    classes = {
        'рыцарь': {'health': 50, 'stamina': 20, 'armor': 10, 'damage': 5},
        'варвар': {'health': 100, 'stamina': 0, 'armor': 0, 'damage': 10},
        'самурай': {'health': 30, 'stamina': 50, 'armor': 5, 'damage': 15}
    }
    
    print("Выберите класс:")
    for cls in classes:
        print(f"- {cls}")
    
    while True:
        choice = input("Введите класс: ").strip().lower()
        if choice in classes:
            return choice, classes[choice]
        else:
            print("Неверный класс, попробуйте снова.")

def generate_enemies(width, height, num_enemies):
    """
    Генерирует список врагов.
    
    :param width: ширина карты (внутренняя часть)
    :param height: высота карты (внутренняя часть)
    :param num_enemies: количество врагов
    :return: список объектов Enemy
    """
    enemies = []
    for _ in range(num_enemies):
        enemy_type = random.choice(['орк', 'гоблин', 'тролль'])
        if enemy_type == 'орк':
            enemies.append(Enemy(name='Орк', health=50, armor=5, damage=10))
        elif enemy_type == 'гоблин':
            enemies.append(Enemy(name='Гоблин', health=30, armor=2, damage=5))
        elif enemy_type == 'тролль':
            enemies.append(Enemy(name='Тролль', health=70, armor=10, damage=15))
    return enemies

if __name__ == "__main__":
    # Запрос размеров карты у пользователя
    width = int(input("Введите ширину карты (внутренняя часть): "))
    height = int(input("Введите высоту карты (внутренняя часть): "))
    
    # Выбор класса игрока
    player_class, bonuses = choose_class()
    
    # Создание игрока с бонусами
    player = Player(
        name=input("Введите имя игрока: "),
        player_class=player_class,
        health=100 + bonuses['health'],
        stamina=100 + bonuses['stamina'],
        armor=10 + bonuses['armor'],
        damage=30 + bonuses['damage'],
        experience=0
    )
    
    # Генерация карты
    game_map = generate_map(width, height)
    
    # Генерация врагов
    num_enemies = int(input("Введите количество врагов: "))
    enemies = generate_enemies(width, height, num_enemies)
    
    # Размещение игрока и врагов на карте
    place_player_on_map(player, game_map)
    place_enemies_on_map(enemies, game_map)
    
    # Основной цикл игры
    while True:
        player_info = str(player)
        print_map(game_map, player_info)
        
        # Проверка столкновений с врагами
        for enemy in enemies[:]:  # Используем enemies[:] для итерации по копии списка
            if player.x == enemy.x and player.y == enemy.y:
                print(f"\nВы встретили {enemy.name}!")
                while player.is_alive() and enemy.is_alive():
                    action = input("Введите действие (a - атаковать, r - убежать): ").strip().lower()
                    if action == 'a':
                        player.attack(enemy)
                        if enemy.is_alive():
                            enemy.attack(player)
                    elif action == 'r':
                        print(f"{player.name} побежал от {enemy.name}.")
                        break
                    else:
                        print("Неизвестное действие")
                    
                    if not player.is_alive():
                        print(f"{player.name} проиграл.")
                        exit()
                    elif not enemy.is_alive():
                        print(f"{player.name} победил {enemy.name}!")
                        player.experience += 10
                        clear_enemy_from_map(enemy, game_map)
                        enemies.remove(enemy)
                        break
        
        command = input("Введите команду (w/a/s/d для движения, q для выхода): ").strip().lower()
        if command == 'q':
            break
        elif command == 'w':
            clear_player_from_map(player, game_map)
            player.move(0, -1, game_map)
            place_player_on_map(player, game_map)
        elif command == 'a':
            clear_player_from_map(player, game_map)
            player.move(-1, 0, game_map)
            place_player_on_map(player, game_map)
        elif command == 's':
            clear_player_from_map(player, game_map)
            player.move(0, 1, game_map)
            place_player_on_map(player, game_map)
        elif command == 'd':
            clear_player_from_map(player, game_map)
            player.move(1, 0, game_map)
            place_player_on_map(player, game_map)
        else:
            print("Неизвестная команда")
        
        # Очистка экрана для обновления карты
        print("\033[H\033[J", end="")
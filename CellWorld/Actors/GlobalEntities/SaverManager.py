import json
import copy
import random
import re

class SaveManager:
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._data = self._load_data()
        
        # Стандартный шаблон для клетки
        self.cell_template = {
            "credentials": {
                "name": "",
                "color": [255, 255, 255],
                "visual_distance": 100,
                "size": 10,
                "draw_text_table": False,
                "draw_lines": False,
                "death_color": [100, 100, 100]
            },
            "physical": {
                "cell_mass": 1.0,
                "cell_min_speed": 0.0,
                "cell_max_speed": 1.0,
                "strength": 1,
                "drag_factor": 0.9,
                "is_movable": True,
                "is_gravitate": False
            },
            "life": {
                "metabolism_rate": 1.0,
                "hunger_border": 50,
                "eat_radius": 10,
                "lifetime": 1000,
                "is_mortal": True,
                "is_metabolism": True,
                "food": []
            },
            "spawner": {
                "spawn_cell_types": [],
                "spawned_start_speed": [0, 0],
                "spawn_delay": 1,
                "spawn_directions": [],
                "max_spawn_number": 1,
                "mutation_rate": 0.1,
                "crossover_rate": 0.1
            },
            "community": {
                "attached_offsets": [],
                "relationship": [],
                "friendship": []
            },
            "actions": {}
        }
        
        # Маппинг плоских ключей на вложенную структуру
        self.flat_mapping = {
            'name': ('credentials', 'name'),
            'color': ('credentials', 'color'),
            'visual_distance': ('credentials', 'visual_distance'),
            'size': ('credentials', 'size'),
            'draw_text_table': ('credentials', 'draw_text_table'),
            'draw_lines': ('credentials', 'draw_lines'),
            'death_color': ('credentials', 'death_color'),
            
            'cell_mass': ('physical', 'cell_mass'),
            'cell_min_speed': ('physical', 'cell_min_speed'),
            'cell_max_speed': ('physical', 'cell_max_speed'),
            'strength': ('physical', 'strength'),
            'drag_factor': ('physical', 'drag_factor'),
            'can_move': ('physical', 'is_movable'),
            'is_gravitate': ('physical', 'is_gravitate'),
            
            'metabolism_rate': ('life', 'metabolism_rate'),
            'hunger_border': ('life', 'hunger_border'),
            'eat_radius': ('life', 'eat_radius'),
            'lifetime': ('life', 'lifetime'),
            'is_mortal': ('life', 'is_mortal'),
            'is_metabolism': ('life', 'is_metabolism'),
            'food': ('life', 'food'),
            
            'spawn_cell_types': ('spawner', 'spawn_cell_types'),
            'spawned_start_speed': ('spawner', 'spawned_start_speed'),
            'spawn_delay': ('spawner', 'spawn_delay'),
            'spawn_directions': ('spawner', 'spawn_directions'),
            'max_spawn_number': ('spawner', 'max_spawn_number'),
            'mutation_rate': ('spawner', 'mutation_rate'),
            'crossover_rate': ('spawner', 'crossover_rate'),
            
            'attached_offsets': ('community', 'attached_offsets'),
            'relationship': ('community', 'relationship'),
            'friendship': ('community', 'friendship')
        }

    def _load_data(self):
        """Загружает данные из JSON файла"""
        try:
            with open(self._path_to_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Файл не найден")
        except json.JSONDecodeError:
            raise Exception("Ошибка чтения JSON")

    def _save_data(self):
        """Сохраняет данные в JSON файл"""
        with open(self._path_to_file, 'w') as f:
            json.dump(self._data, f, indent=2)

    def _parse_relationship_string(self, relationship_str):
        """Парсит строку отношений в формате 'клетка:отношение' или просто имена"""
        relationships = []
        
        # Разделяем по запятым
        items = [item.strip() for item in relationship_str.split(',') if item.strip()]
        
        for item in items:
            # Проверяем, есть ли двоеточие (формат "клетка:отношение")
            if ':' in item:
                cell_name, relation = item.split(':', 1)
                cell_name = cell_name.strip()
                try:
                    relation = int(relation.strip())
                except ValueError:
                    relation = 0  # Значение по умолчанию, если не число
                
                relationships.append({
                    "cell_type_name": cell_name,
                    "relation": relation,
                    "preferred_distance": 50,  # Значение по умолчанию
                    "hunger_distance": 10       # Значение по умолчанию
                })
            else:
                # Просто имя клетки без указания отношения
                relationships.append({
                    "cell_type_name": item,
                    "relation": 0,              # Значение по умолчанию
                    "preferred_distance": 50,   # Значение по умолчанию
                    "hunger_distance": 10       # Значение по умолчанию
                })
        
        return relationships

    def _parse_food_string(self, food_str):
        """Парсит строку еды в формате 'клетка:множитель' или просто имена"""
        food_items = []
        
        # Разделяем по запятым
        items = [item.strip() for item in food_str.split(',') if item.strip()]
        
        for item in items:
            # Проверяем, есть ли двоеточие (формат "клетка:множитель")
            if ':' in item:
                cell_name, multiplier = item.split(':', 1)
                cell_name = cell_name.strip()
                try:
                    multiplier = float(multiplier.strip())
                except ValueError:
                    multiplier = 1.0  # Значение по умолчанию, если не число
                
                food_items.append({
                    "cell_type_name": cell_name,
                    "stats_multiplier": multiplier
                })
            else:
                # Просто имя клетки без указания множителя
                food_items.append({
                    "cell_type_name": item,
                    "stats_multiplier": 1.0  # Значение по умолчанию
                })
        
        return food_items

    def _parse_friendship_string(self, friendship_str):
        """Парсит строку дружбы в формате 'клетка:дистанция' или просто имена"""
        friendships = []
        
        # Разделяем по запятым
        items = [item.strip() for item in friendship_str.split(',') if item.strip()]
        
        for item in items:
            # Проверяем, есть ли двоеточие (формат "клетка:дистанция")
            if ':' in item:
                cell_name, distance = item.split(':', 1)
                cell_name = cell_name.strip()
                try:
                    distance = int(distance.strip())
                except ValueError:
                    distance = 40  # Значение по умолчанию, если не число
                
                friendships.append({
                    "cell_type_name": cell_name,
                    "friend_distance": distance,
                    "is_line_need": False  # Значение по умолчанию
                })
            else:
                # Просто имя клетки без указания дистанции
                friendships.append({
                    "cell_type_name": item,
                    "friend_distance": 40,  # Значение по умолчанию
                    "is_line_need": False   # Значение по умолчанию
                })
        
        return friendships

    def _remove_cell_references(self, cell_name):
        """Удаляет все упоминания клетки из отношений других клеток"""
        for cell in self._data['cell_options']:
            # Удаляем из food
            if 'food' in cell.get('life', {}):
                cell['life']['food'] = [
                    food for food in cell['life']['food'] 
                    if food.get('cell_type_name') != cell_name
                ]
            
            # Удаляем из relationship
            if 'relationship' in cell.get('community', {}):
                cell['community']['relationship'] = [
                    rel for rel in cell['community']['relationship'] 
                    if rel.get('cell_type_name') != cell_name
                ]
            
            # Удаляем из friendship
            if 'friendship' in cell.get('community', {}):
                cell['community']['friendship'] = [
                    friend for friend in cell['community']['friendship'] 
                    if friend.get('cell_type_name') != cell_name
                ]
            
            # Удаляем из attached_offsets
            if 'attached_offsets' in cell.get('community', {}):
                cell['community']['attached_offsets'] = [
                    offset for offset in cell['community']['attached_offsets'] 
                    if offset.get('cell_type_name') != cell_name
                ]
            
            # Удаляем из spawn_cell_types
            if 'spawn_cell_types' in cell.get('spawner', {}):
                if cell_name in cell['spawner']['spawn_cell_types']:
                    cell['spawner']['spawn_cell_types'].remove(cell_name)

    def _convert_flat_to_structured(self, flat_data):
        """Преобразует плоские данные в структурированные"""
        # Создаем глубокую копию шаблона
        structured_data = copy.deepcopy(self.cell_template)
        
        # Обрабатываем специальные поля
        if 'food' in flat_data and isinstance(flat_data['food'], str):
            flat_data['food'] = self._parse_food_string(flat_data['food'])
        
        if 'relationship' in flat_data and isinstance(flat_data['relationship'], str):
            flat_data['relationship'] = self._parse_relationship_string(flat_data['relationship'])
        
        if 'friendship' in flat_data and isinstance(flat_data['friendship'], str):
            flat_data['friendship'] = self._parse_friendship_string(flat_data['friendship'])
        
        # Преобразуем плоские ключи во вложенную структуру
        for flat_key, (category, subkey) in self.flat_mapping.items():
            if flat_key in flat_data:
                # Для числовых значений преобразуем строки в числа
                if isinstance(flat_data[flat_key], str) and flat_data[flat_key].replace('.', '').replace('-', '').isdigit():
                    if '.' in flat_data[flat_key]:
                        structured_data[category][subkey] = float(flat_data[flat_key])
                    else:
                        structured_data[category][subkey] = int(flat_data[flat_key])
                else:
                    structured_data[category][subkey] = flat_data[flat_key]
        
        return structured_data

    def save_cell(self, cell_data):
        """
        Сохраняет или обновляет клетку в конфигурации
        Поддерживает как структурированные, так и плоские данные
        """
        # Определяем тип данных и преобразуем при необходимости
        if 'credentials' in cell_data and 'physical' in cell_data:
            # Это уже структурированные данные
            structured_data = cell_data
        else:
            # Это плоские данные, нужно преобразовать
            structured_data = self._convert_flat_to_structured(cell_data)
            
        structured_data['credentials']['color'] = (random.randint(1,240), random.randint(1,240), random.randint(1,240))
        # Проверяем наличие имени
        if not structured_data['credentials']['name']:
            raise ValueError("Клетка должна иметь имя")
            
        # Ищем существующую клетку с таким именем
        cell_name = structured_data['credentials']['name']
        for i, cell in enumerate(self._data['cell_options']):
            if cell['credentials']['name'] == cell_name:
                # Обновляем существующую клетку
                self._data['cell_options'][i] = structured_data
                break
        else:
            # Добавляем новую клетку если не нашли существующую
            self._data['cell_options'].append(structured_data)
            
        self._save_data()

    def del_cell(self, name):
        """Удаляет клетку по имени и все её упоминания в других клетках"""
        # Удаляем саму клетку
        self._data['cell_options'] = [
            cell for cell in self._data['cell_options'] 
            if cell['credentials']['name'] != name
        ]
        
        # Удаляем все упоминания этой клетки в других клетках
        self._remove_cell_references(name)
        
        self._save_data()

    def _update_dict(self, original, update):
        """Рекурсивно обновляет словарь"""
        for key, value in update.items():
            if (key in original and 
                isinstance(original[key], dict) and 
                isinstance(value, dict)):
                self._update_dict(original[key], value)
            else:
                original[key] = value
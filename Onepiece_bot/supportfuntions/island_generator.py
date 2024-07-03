from database import islands
import random

def generate_island(guild):
    member_count = len([member for member in guild.members if not member.bot])
    if member_count < 50:
        size = 'small'
        building_count = random.randint(5, 10)
    elif member_count < 100:
        size = 'medium'
        building_count = random.randint(10, 15)
    else:
        size = 'large'
        building_count = random.randint(15, 20)

    seas = ['East Blue', 'West Blue', 'North Blue', 'South Blue', 'Grand Line']
    sea = random.choice(seas)

    island_data = {
        '_id': guild.id,
        'name': guild.name,
        'description': f"This is the {guild.name} island.",
        'size': size,
        'sea': sea,
        'areas': [
            {
                'name': 'Main City',
                'description': f"The main city of the {guild.name} island.",
                'buildings': [
                    {
                        'name': f"Building {i}",
                        'description': f"This is Building {i} in the {guild.name} island."
                    } for i in range(1, building_count + 1)
                ],
                'roads': [],
                'tasks': []
            },
            {
                'name': 'Wilderness',
                'description': f"The wilderness surrounding the {guild.name} island.",
                'tasks': []
            }
        ],
        'quests': [],
        'resources': [],
        'enemies': []
    }

    islands.insert_one(island_data)
    return island_data


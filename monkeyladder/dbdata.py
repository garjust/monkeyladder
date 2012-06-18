from ladders.models import Ladder, LadderUser
from django.contrib.auth.models import User

USERS = {
    'vladman': {
        'password': 'password',
        'first_name': 'Vlad',
        'last_name': 'Mandrychenko',
    },
    'mike.pettypiece': {
        'password': 'password',
        'first_name': 'Mike',
        'last_name': 'Pettypiece',
        'is_staff': True,
    },
    'the_tan': {
        'password': 'password',
        'first_name': 'Tan',
        'last_name': 'Quach',
    },
    'coma': {
        'password': 'password',
        'first_name': 'Nicky',
        'last_name': 'Thompson',
        'is_staff': True,
    },
    'waffle': {
        'password': 'password',
        'first_name': 'Momo',
    },
    'mikey': {
        'password': 'password',
        'last_name': 'aedy',
    },
    'random-user': {
        'password': 'password',
        'first_name': 'A',
        'last_name': 'Anonymous',
    },
}

PONG_USERS = [('the_tan', 5), ('jagarbut', 3), ('vladman', 1), ('mike.pettypiece', 2), ('waffle', 7), ('coma', 4), ('mikey', 6),]
DOTA_USERS = [('mikey', 4), ('jagarbut', 1), ('waffle', 3), ('coma', 2),]

for user in USERS:
    User(username=user, **USERS[user]).save()

points_ladder = Ladder(name='Ping Pong At Points', rungs=25, is_private=True)
points_ladder.save()

other_ladder = Ladder(name='Dota 2 Ladder', rungs=10)
other_ladder.save()

for user in PONG_USERS:
    ladder_user = LadderUser(ladder=points_ladder, user=User.objects.filter(username=user[0])[0], rank=user[1])
    ladder_user.save()

for user in DOTA_USERS:
    ladder_user = LadderUser(ladder=other_ladder, user=User.objects.filter(username=user[0])[0], rank=user[1])
    ladder_user.save()

admin = User.objects.filter(username='jagarbut')[0]
admin.first_name = 'Justin'
admin.last_name = 'Garbutt'
admin.save()
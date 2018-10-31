''' Create test data in the database.

Usage:
    python manage.py shell
    >> execfile('create_test_data.py')
'''
import datetime

from django.contrib.auth.models import User

from tracker.models import Profile, Classification, Exercise


u = User.objects.create(username='davidr',
                        first_name='David',
                        last_name='Ross',
                        is_superuser=True,
                        email='dross78375@gmail.com')
u.set_password('Strokes_01!')
u.save()
p = Profile.objects.create(user=u,
                           height_unit='cm',
                           weight_unit='kg',
                           height=181,
                           weight=77,
                           time_zone='UTC',
                           country='GB',
                           birth_date=datetime.date(1989, 7, 17),
                           bmi=0)
p.save()
u = User.objects.create(username='test_user',
                        is_superuser=False,
                        email='example@gmail.com')
u.set_password('password')
p = Profile.objects.create(user=u,
                           height_unit='cm',
                           weight_unit='kg',
                           height=190,
                           weight=79,
                           time_zone='UTC',
                           country='GB',
                           birth_date=datetime.date(1993, 9, 21))
p.save()

push = Classification.objects.create(name='Push')
push.save()

yt_link = 'https://www.youtube.com/watch?v=IODxDxX7oi4'
push_up = Exercise.objects.create(name='Push Up',
                                  video=yt_link,
                                  type='i',
                                  classification=push,
                                  created_by=p)
push_up.save()

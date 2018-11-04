''' Create test data in the database.

Usage:
    python manage.py shell
    >> execfile('create_test_data.py')
'''
import datetime

from django.contrib.auth.models import User

from tracker.models import (
    Profile, Exercise, ExerciseInstance,
    Classification, Set, MuscleGroup
)


# Users & Profiles
u = User.objects.create(username='davidr',
                        first_name='David',
                        last_name='Ross',
                        is_superuser=True,
                        email='dross78375@gmail.com')
u.set_password('Strokes_01!')
u.save()
owner = Profile.objects.create(user=u,
                               height_unit='cm',
                               weight_unit='kg',
                               height=181,
                               weight=77,
                               time_zone='UTC',
                               country='GB',
                               birth_date=datetime.date(1989, 7, 17),
                               bmi=0)
owner.save()

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


# Classifications
push = Classification.objects.create(name='Push')
push.save()

pull = Classification.objects.create(name='Pull')
pull.save()


# Muscle Groups
lats = MuscleGroup.objects.create(group='Back',
                                  muscle='Latissimus dorsi')
lats.save()
bicep = MuscleGroup.objects.create(group='Arms',
                                   muscle='biceps brachii')
bicep.save()
traps = MuscleGroup.objects.create(group='Back',
                                   muscle='Lower trapezius')
traps.save()
pec_maj = MuscleGroup.objects.create(group='Chest',
                                     muscle='Pectoralis major')
pec_maj.save()
pec_min = MuscleGroup.objects.create(group='Chest',
                                     muscle='Pectoralis minor')
pec_min.save()


# Exercises
yt_link = 'https://www.youtube.com/watch?v=IODxDxX7oi4'
push_up = Exercise.objects.create(name='Push Up',
                                  video=yt_link,
                                  type='i',
                                  created_by=owner)
push_up.muscles.add(pec_maj, pec_min)
push_up.classification.add(push)
push_up.save()

yt_link = "https://www.youtube.com/watch?v=eGo4IYlbE5g"
pull_up = Exercise.objects.create(name='Pull Up',
                                  video=yt_link,
                                  type='i',
                                  created_by=owner)
pull_up.muscles.add(lats, bicep, traps)
pull_up.classification.add(pull)
pull_up.save()

yt_link = 'https://www.youtube.com/watch?v=2z8JmcrW-As&t=181s'
dip = Exercise.objects.create(name='Dip',
                              video=yt_link,
                              type='i',
                              created_by=owner)
dip.muscles.add(pec_maj, pec_min)
dip.classification.add(push)
dip.save()


# Sets
pu_set1 = Set.objects.create(reps=12, weight='kg=20')
pu_set2 = Set.objects.create(reps=10, weight='kg=20')
pu_set3 = Set.objects.create(reps=9, weight='kg=20')
pu_set1.save()
pu_set2.save()
pu_set3.save()

pl_set1 = Set.objects.create(reps=50)
pl_set2 = Set.objects.create(reps=40)
pl_set3 = Set.objects.create(reps=29)
pl_set1.save()
pl_set2.save()
pl_set3.save()

d_set1 = Set.objects.create(reps=15)
d_set2 = Set.objects.create(reps=14)
d_set3 = Set.objects.create(reps=12)
d_set1.save()
d_set2.save()
d_set3.save()


# Exercise Instances
pull_up_1 = ExerciseInstance.objects.create(participant=test_user,
                                            exercise=pull_up,
                                            mood='m',
                                            fatigued=False,
                                            date=datetime.date(2018, 9, 9))
pull_up_1.sets.add(pu_set1, pu_set2, pu_set3)
pull_up1.save()

pull_up_2 = ExerciseInstance.objects.create(participant=test_user,
                                            exercise=pull_up,
                                            mood='e',
                                            fatigued=False,
                                            date=datetime.date(2018, 9, 9))
pull_up_2.sets.add(pu_set1, pu_set1, pu_set2)
pull_up2.save()

pl_1 = ExerciseInstance.objects.create(participant=test_user,
                                       exercise=push_up,
                                       mood='e',
                                       fatigued=False,
                                       date=datetime.date(2018, 10, 9))
pl_1.sets.add(pl_set1, pl_set1, pl_set2)
pl_1.save()

d_1 = ExerciseInstance.objects.create(participant=test_user,
                                      exercise=dip,
                                      mood='u',
                                      fatigued=False,
                                      date=datetime.date(2018, 11, 9))
d_1.sets.add(d_set1, d_set2, d_set3)
d_1.save()

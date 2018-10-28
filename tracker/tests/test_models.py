''' All unit tests for the tracker models.'''
import datetime

from django.test import TestCase

import pytz

from tracker.models import (
    Profile, Exercise, ExerciseInstance,
    Classification, Set, MuscleGroup
)


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create test users
        cls.ninja = Profile.objects.create(
            username='ninja', first_name='Hamish',
            last_name='StankyArse', password='password',
            email='smelly_penguin_luv_sandwich@example.com',
            height='cm=198', weight='kg=90', time_zone='UTC',
            country='GB', birth_date=datetime.date(1991, 6, 19))
        superuser = Profile.objects.create(
            username='david', password='pass',
            is_superuser=True, height='cm=900', weight='kg=89')
        dummy = Profile.objects.create(
            username='dummy', password='pass',
            height='cm=900', weight='kg=89')
        # create dummy exercises
        Exercise.objects.create(name='Push Up',
                                created_by=cls.ninja)
        Exercise.objects.create(name='Plank',
                                created_by=superuser)
        Exercise.objects.create(name='Pull Up',
                                created_by=dummy)
        # create dummy exrcise instances
        ExerciseInstance.objects.create(
            participant=cls.ninja)
        ExerciseInstance.objects.create(
            participant=cls.ninja)
        ExerciseInstance.objects.create(
            participant=cls.ninja)

    def test_all_exercises(self):
        all_exercises = self.ninja.all_exercises()
        all_name = [x.name for x in all_exercises]
        self.assertIn('Push Up', all_name)
        self.assertIn('Plank', all_name)
        self.assertNotIn('Pull Up', all_name)

    def test_all_exercise_instance(self):
        all_exercise_inst = self.ninja.all_exercise_instances()
        self.assertEqual(3, len(all_exercise_inst))

    def test_height_label(self):
        field_label = self.ninja._meta.get_field('_height').verbose_name
        self.assertEquals(field_label, ' height')

    def test_weight_label(self):
        field_label = self.ninja._meta.get_field('_weight').verbose_name
        self.assertEquals(field_label, ' weight')

    def test_bmi_label(self):
        field_label = self.ninja._meta.get_field('bmi').verbose_name
        self.assertEquals(field_label, 'bmi')

    def test_country_label(self):
        field_label = self.ninja._meta.get_field('country').verbose_name
        self.assertEquals(field_label, 'country')

    def test_time_zone_label(self):
        field_label = self.ninja._meta.get_field('time_zone').verbose_name
        self.assertEquals(field_label, 'time zone')

    def test_birth_date_label(self):
        field_label = self.ninja._meta.get_field('_birth_date').verbose_name
        self.assertEquals(field_label, ' birth date')

    def test_object_name_is_username_id(self):
        ''' test __str__ produces expected string.'''
        expected_object_name = f'{self.ninja.username} - {self.ninja.pk}'
        self.assertEquals(expected_object_name, str(self.ninja))

    def test_bmi(self):
        ''' Test BMI is being calculated as expected.'''
        self.assertEquals(22.96, round(self.ninja.bmi, 2))

    def test_age(self):
        ''' Test users age is calculated correctly.'''
        day_diff = datetime.date.today() - datetime.date(1991, 6, 19)
        age = round((day_diff / 365).days)
        self.assertEquals(age, self.ninja.age)

    def test_height_conversion(self):
        ''' Test height conversion is working.'''
        self.assertEquals(6.5, round(self.ninja.height.ft, 1))

    def test_weight_conversion(self):
        ''' Test weight conversion is working.'''
        self.assertEquals(198.42, round(self.ninja.weight.lb, 2))

    # def test_get_absolute_url(self):
    #     ''' This will also fail if the urlconf is not defined.'''
    #     author = Author.objects.get(id=1)
    #     self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class TestMuscleGroup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mg = MuscleGroup.objects.create(group='Back',
                                            muscle='Latissimus dorsi')

    def test_object_name_is_username_id(self):
        ''' test __str__ produces expected string.'''
        expected_object_name = f'{self.mg.group}: {self.mg.muscle}'
        self.assertEquals(expected_object_name, str(self.mg))


class TestClassification(TestCase):
    @classmethod
    def setUpTestData(cls):
        Classification.objects.create(name='Push')

    def test_object_name_is_username_id(self):
        ''' test __str__ produces expected string.'''
        classification = Classification.objects.get(name='Push')
        expected_object_name = f'{classification.name}'
        self.assertEquals(expected_object_name, str(classification))


class TestRelationships(TestCase):
    @classmethod
    def setUpTestData(cls):
        # profile
        cls.ninja = Profile.objects.create(
            username='ninja', first_name='Hamish',
            last_name='StankyArse', password='password',
            email='smelly_penguin_luv_sandwich@example.com',
            height='cm=198', weight='kg=90', time_zone='UTC',
            country='GB', birth_date=datetime.date(1991, 6, 19))
        cls.superuser = Profile.objects.create(
            username='david', password='pass',
            is_superuser=True, height='cm=900', weight='kg=89')
        # classifications
        cls.push = Classification.objects.create(name='Push')
        cls.pull = Classification.objects.create(name='Pull')
        # muscle group
        cls.lats = MuscleGroup.objects.create(group='Back',
                                              muscle='Latissimus dorsi')
        cls.bicep = MuscleGroup.objects.create(group='Arms',
                                               muscle='biceps brachii')
        cls.traps = MuscleGroup.objects.create(group='Back',
                                               muscle='Lower trapezius')
        cls.pec_maj = MuscleGroup.objects.create(group='Chest',
                                                 muscle='Pectoralis major')
        cls.pec_min = MuscleGroup.objects.create(group='Chest',
                                                 muscle='Pectoralis minor')
        # exercises
        yt_link = 'https://www.youtube.com/watch?v=IODxDxX7oi4'
        cls.push_up = Exercise.objects.create(name='Push Up',
                                              video=yt_link,
                                              type='i',
                                              classification=cls.push,
                                              created_by=cls.ninja)
        cls.push_up.muscles.add(cls.pec_maj, cls.pec_min)
        cls.dip = Exercise.objects.create(name='Dip',
                                          video=yt_link,
                                          type='i',
                                          classification=cls.push,
                                          created_by=cls.ninja)
        cls.dip.muscles.add(cls.pec_maj, cls.pec_min)
        cls.pull_up = Exercise.objects.create(name='Pull Up',
                                              video=yt_link,
                                              type='i',
                                              classification=cls.pull,
                                              created_by=cls.superuser)
        cls.pull_up.muscles.add(cls.lats, cls.bicep, cls.traps)
        # sets
        cls.pu_set1 = Set.objects.create(reps=12, weight='kg=20')
        cls.pu_set2 = Set.objects.create(reps=10, weight='kg=20')
        cls.pu_set3 = Set.objects.create(reps=9, weight='kg=20')
        cls.pl_set1 = Set.objects.create(reps=50)
        cls.pl_set2 = Set.objects.create(reps=40)
        cls.pl_set3 = Set.objects.create(reps=29)
        cls.d_set1 = Set.objects.create(reps=15)
        cls.d_set2 = Set.objects.create(reps=14)
        cls.d_set3 = Set.objects.create(reps=12)
        # exercise instances
        cls.pull_up_1 = ExerciseInstance.objects.create(participant=cls.ninja,
                                                        exercise=cls.pull_up,
                                                        mood='m',
                                                        fatigued=False,
                                                        date=datetime.date(2018, 9, 9))
        cls.pull_up_1.sets.add(cls.pu_set1, cls.pu_set2, cls.pu_set3)
        cls.pull_up_2 = ExerciseInstance.objects.create(participant=cls.ninja,
                                                        exercise=cls.pull_up,
                                                        mood='e',
                                                        fatigued=False,
                                                        date=datetime.date(2018, 9, 9))
        cls.pull_up_2.sets.add(cls.pu_set1, cls.pu_set1, cls.pu_set2)
        cls.pl_1 = ExerciseInstance.objects.create(participant=cls.ninja,
                                                   exercise=cls.push_up,
                                                   mood='e',
                                                   fatigued=False,
                                                   date=datetime.date(2018, 10, 9))
        cls.pl_1.sets.add(cls.pl_set1, cls.pl_set1, cls.pl_set2)
        cls.d_1 = ExerciseInstance.objects.create(participant=cls.ninja,
                                                  exercise=cls.dip,
                                                  mood='u',
                                                  fatigued=False,
                                                  date=datetime.date(2018, 11, 9))
        cls.d_1.sets.add(cls.d_set1, cls.d_set2, cls.d_set3)

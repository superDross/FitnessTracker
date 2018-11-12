from django.db.models.query_utils import DeferredAttribute

from tracker.models import Set

import pandas as pd


class InstanceSetDict(object):
    ''' Transform an ExerciseInstance objects set data into a dict.'''

    def __init__(self, instance):
        self.instance = instance
        self.sets = instance.sets.all()
        self.attributes = self._get_all_set_attr()
        self.dict = {}
        self._create_dict()

    def _get_all_set_attr(self):
        ''' Get Set attributes of interest and return as a list.'''
        set_attr_keys = []
        for k, i in Set.__dict__.items():
            if isinstance(i, DeferredAttribute) and k != 'id':
                set_attr_keys.append(k.replace('_', ''))
        return set_attr_keys

    def _add_header(self):
        ''' Add set attributes as keys to the table dict.'''
        self.dict = {k.capitalize(): [] for k in self.attributes}

    def _change_keys(self):
        ''' Alters the distance and weight keys to include units.'''
        weight_unit = self.instance.participant.weight_unit
        self.dict[f'Weight ({weight_unit})'] = self.dict['Weight']
        distance_unit = self.instance.participant.distance_unit
        self.dict[f'Distance ({distance_unit})'] = self.dict['Distance']
        del self.dict['Distance']
        del self.dict['Weight']

    def _get_set_value(self, aset, attr):
        ''' Get the value of a given Set objects attribute.'''
        set_value = getattr(aset, attr)
        if set_value:
            if attr in ['weight', 'distance']:
                # get participants preffered unit of measurement and
                # return value in said unit
                unit = getattr(self.instance.participant, f'{attr}_unit')
                set_value = getattr(set_value, unit)
        else:
            set_value = None
        return set_value

    def _add_set_data(self):
        ''' Add all sets data to the dictionary'''
        for aset in self.sets:
            for attr in self.attributes:
                set_value = self._get_set_value(aset, attr)
                self.dict[attr.capitalize()].append(set_value)

    def _create_dict(self):
        self._add_header()
        self._add_set_data()
        self._change_keys()

    def to_dataframe(self):
        df = pd.DataFrame.from_dict(self.dict)
        df = df[df.columns[~df.isnull().all()]]
        df['Sets'] = df.index + 1
        df['Date'] = self.instance.date
        df['Exercise'] = self.instance.exercise.name
        df = df.set_index(['Exercise', 'Date', 'Sets'])
        return df

    def to_html(self):
        df = self.to_dataframe()
        return pd.DataFrame.to_html(df)


def exercise_instance_table(qs):
    ''' Create a HTML table from a given ExerciseInstance QuerySet'''
    # Get all instance by Exercise Type
    all_dfs = []
    for instance in qs:
        df = InstanceSetDict(instance).to_dataframe()
        all_dfs.append(df)

    big_table = pd.concat(all_dfs, sort=False).T
    big_table = big_table.fillna('-')
    return big_table.to_html()

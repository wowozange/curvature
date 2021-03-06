# Add our parent folder to our path
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import pytest
from curvature.post_processors.filter_out_ways_with_tag import FilterOutWaysWithTag
from copy import copy

@pytest.fixture
def raymond_road():
    return {
        'join_type': 'name',
        'join_data': 'Raymond Road',
        'ways': [
            { 'id': 100000,
              'tags': {   'highway': 'residential',
                          'name': 'Raymond Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 100001,
              'tags': {   'highway': 'unclassified',
                          'name': 'Raymond Road'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 100002,
              'tags': {   'highway': 'unclassified',
                          'name': 'Raymond Road',
                          'surface': 'concrete',
                          'bridge': 'yes',
                          'layer': 1},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 100004,
              'tags': {   'highway': 'unclassified',
                          'name': 'Raymond Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 100005,
              'tags': {   'highway': 'tertiary',
                          'name': 'Raymond Road',},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            }]}

# "Old Mountain Road".
# A mixture of highway types where an unclassified road becomes a track over a pass,
# then becomes an unclassified road again on the other side.
@pytest.fixture
def old_mountain_road():
    return {
        'join_type': 'name',
        'join_data': 'Old Mountain Road',
        'ways': [
            { 'id': 200000,
              'tags': {   'highway': 'unclassified',
                          'name': 'Old Mountain Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200001,
              'tags': {   'highway': 'unclassified',
                          'name': 'Old Mountain Road',
                          'surface': 'gravel'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200002,
              'tags': {   'highway': 'track',
                          'name': 'Old Mountain Road'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200003,
              'tags': {   'highway': 'track',
                          'name': 'Old Mountain Road',
                          'surface': 'concrete',
                          'bridge': 'yes',
                          'layer': 1},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200004,
              'tags': {   'highway': 'track',
                          'name': 'Old Mountain Road'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200005,
              'tags': {   'highway': 'unclassified',
                          'name': 'Old Mountain Road',
                          'surface': 'dirt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200006,
              'tags': {   'highway': 'unclassified',
                          'name': 'Old Mountain Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 200007,
              'tags': {   'highway': 'unclassified',
                          'name': 'Old Mountain Road'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            }]}

# This road is an unclassified road that has a gravel section in the middle.
@pytest.fixture
def barnes_road():
    return {
        'join_type': 'name',
        'join_data': 'Barnes Road',
        'ways': [
            { 'id': 300000,
              'tags': {   'highway': 'unclassified',
                          'name': 'Barnes Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 300001,
              'tags': {   'highway': 'unclassified',
                          'name': 'Barnes Road',
                          'surface': 'gravel'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 300002,
              'tags': {   'highway': 'unclassified',
                          'name': 'Barnes Road'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            },
            { 'id': 100004,
              'tags': {   'highway': 'unclassified',
                          'name': 'Barnes Road',
                          'surface': 'asphalt'},
              'coords': [],   # Not used in this component, leaving empty for simplicity.
              'refs': []    # Not used in this component, leaving empty for simplicity.
            }]}

@pytest.fixture
def highway_roads():
    return ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link']

@pytest.fixture
def highway_nonroads():
    return ['pedestrian', 'track', 'raceway', 'road', 'footway', 'bridleway', 'path', 'cycleway']

@pytest.fixture
def surfaces_paved():
    return ['paved', 'asphalt', 'concrete', 'paving_stones', 'cobblestone', 'concrete:plates', 'sett', 'cobblestone:flattened', 'metal', 'wood', 'bricks']

@pytest.fixture
def surfaces_unpaved():
    return ['unpaved', 'dirt', 'gravel', 'fine_gravel', 'sand', 'grass', 'ground', 'pebblestone', 'mud', 'clay', 'dirt/sand', 'soil']


def test_all_roads_arent_nonroads(raymond_road, highway_nonroads):
    data = [raymond_road]
    expected_result = [copy(raymond_road)]

    result = list(FilterOutWaysWithTag(tag='highway', values=highway_nonroads).process(data))

    assert(result == expected_result)
    assert(len(result) == 1)
    assert(len(result[0]['ways']) == 5)

def test_road_track_split(old_mountain_road, highway_nonroads):
    data = [old_mountain_road]
    expected_result = [
        {   'join_type': 'name',
            'join_data': 'Old Mountain Road',
            'ways': [   copy(old_mountain_road['ways'][0]),
                        copy(old_mountain_road['ways'][1]) ]},
        {   'join_type': 'name',
            'join_data': 'Old Mountain Road',
            'ways': [   copy(old_mountain_road['ways'][5]),
                        copy(old_mountain_road['ways'][6]),
                        copy(old_mountain_road['ways'][7]) ]}]

    result = list(FilterOutWaysWithTag(tag='highway', values=highway_nonroads).process(data))

    assert(result == expected_result)
    assert(len(result) == 2)
    assert(len(result[0]['ways']) == 2)
    assert(len(result[1]['ways']) == 3)

def test_no_surface_tag_is_paved(raymond_road, surfaces_unpaved):
    data = [raymond_road]
    expected_result = [copy(raymond_road)]

    result = list(FilterOutWaysWithTag(tag='surface', values=surfaces_unpaved).process(data))

    assert(result == expected_result)
    assert(len(result) == 1)
    assert(len(result[0]['ways']) == 5)

def test_no_surface_tag_is_unpaved(raymond_road, surfaces_unpaved):
    data = [raymond_road]
    expected_result = [
        {   'join_type': 'name',
            'join_data': 'Raymond Road',
            'ways': [   copy(raymond_road['ways'][0]) ]},
        {   'join_type': 'name',
            'join_data': 'Raymond Road',
            'ways': [   copy(raymond_road['ways'][2]),
                        copy(raymond_road['ways'][3]) ]}]

    result = list(FilterOutWaysWithTag(tag='surface', values=surfaces_unpaved, filter_out_ways_missing_tag=True).process(data))

    assert(result == expected_result)
    assert(len(result) == 2)
    assert(len(result[0]['ways']) == 1)
    assert(len(result[1]['ways']) == 2)

def test_alternating_paved_unpaved_with_unpaved_surfaces(barnes_road, surfaces_unpaved):
    data = [barnes_road]
    expected_result = [
        {   'join_type': 'name',
            'join_data': 'Barnes Road',
            'ways': [   copy(barnes_road['ways'][0]) ]},
        {   'join_type': 'name',
            'join_data': 'Barnes Road',
            'ways': [   copy(barnes_road['ways'][2]),
                        copy(barnes_road['ways'][3]) ]}]

    result = list(FilterOutWaysWithTag(tag='surface', values=surfaces_unpaved).process(data))

    assert(result == expected_result)
    assert(len(result) == 2)
    assert(len(result[0]['ways']) == 1)
    assert(len(result[1]['ways']) == 2)

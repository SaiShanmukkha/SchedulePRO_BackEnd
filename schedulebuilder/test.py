import random
from collections import defaultdict, namedtuple

TimeSlot = namedtuple('TimeSlot', ['day', 'start_hour', 'duration'])


def initialize_data(num_courses=10, num_faculty=12):
    courses = {}
    faculty = {f'F{i}': {'availability': []} for i in range(1, num_faculty + 1)}

    # Initialize courses with sections, labs, and co-requisites
    for i in range(1, num_courses + 1):
        sections = [f'S{i}-{j}' for j in range(1, random.randint(1, 4) + 1)]
        labs = [f'L{i}-{j}' for j in range(1, random.randint(0, 4) + 1)]
        courses[f'C{i}'] = {
            'sections': sections,
            'labs': labs,
            'co_requisites': []
        }

    # Assign random co-requisites for demonstration, limited to pairs for simplicity
    course_ids = list(courses.keys())
    random.shuffle(course_ids)
    for i in range(0, len(course_ids), 2):
        if i+1 < len(course_ids):  # Ensure we have a pair
            courses[course_ids[i]]['co_requisites'].append(course_ids[i+1])
            courses[course_ids[i+1]]['co_requisites'].append(course_ids[i])

    return courses, faculty



courses, faculty = initialize_data()
# print(courses)
print(faculty)
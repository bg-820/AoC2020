import fileinput
import re

lines = [line.replace('\n', '') for line in fileinput.input()]
lines.append('')

required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
optional_fields = ['cid']

four_digits = re.compile(r"^\d\d\d\d$")
height_cm_p = re.compile(r"^(\d*)cm$")
height_in_p = re.compile(r"^(\d*)in$")
hair_colour = re.compile(r"^#[0-9a-f]{6}")
eye_colours = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
pid = re.compile(r"^\d{9}$")
rules = {
    "byr": lambda x: re.search(four_digits, x) and 1920 <= int(x) <= 2002,
    "iyr": lambda x: re.search(four_digits, x) and 2010 <= int(x) <= 2020,
    "eyr": lambda x: re.search(four_digits, x) and 2020 <= int(x) <= 2030,
    "hgt": lambda x: is_valid_height(x),
    "hcl": lambda x: re.search(hair_colour, x),
    "ecl": lambda x: x in eye_colours,
    "pid": lambda x: re.search(pid, x)
}


def is_valid_height(x):
    height_cm = height_cm_p.match(x)
    if height_cm is not None and 150 <= int(height_cm.groups(0)[0]) <= 193:
        return True
    height_in = height_in_p.match(x)
    return height_in is not None and 59 <= int(height_in.groups(0)[0]) <= 76


def is_valid_passport_1(passport):
    return set(passport.keys()).issuperset(required_fields)


def is_valid_passport_2(passport):
    if not is_valid_passport_1(passport):
        return False
    for attribute_name in required_fields:
        attribute_value = passport[attribute_name]
        attribute_rule = rules[attribute_name]
        if not attribute_rule(attribute_value):
            return False
    return True


def run(passport_checker):
    current_passport = {}
    valid_passport_count = 0
    for line in lines:
        if line == "":
            if passport_checker(current_passport):
                valid_passport_count += 1
            current_passport = {}
            continue
        attributes = line.split(' ')
        for attribute in attributes:
            attribute_name, attribute_value = attribute.split(':')
            current_passport[attribute_name] = attribute_value

    return valid_passport_count


print(run(is_valid_passport_1))
print(run(is_valid_passport_2))

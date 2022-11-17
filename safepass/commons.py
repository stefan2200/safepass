import locale
import string
from sys import platform
import datetime


class Common:
    years = []
    months = []
    days = []
    seasons = [
        "summer", "winter", "spring", "fall", "zomer", "winter", "lente", "herfst"
    ]
    common_numbers = [123456, 1234, 4321, 54321, 321, 123]
    common_special = ["!", "@", "#"]
    common_words = ["password", "secret", "secure"]

    def get_year_span(self, span=2):
        current_year = datetime.datetime.now().year
        pool = [current_year]
        for x in range(1, span+1):
            pool.extend([current_year+x, current_year-x])
        self.common_numbers.extend(pool)

    def set_locale(self, new_locale="en_US"):
        if platform == 'win32':
            locale.setlocale(locale.LC_ALL, new_locale)
        else:
            locale.setlocale(locale.LC_ALL, '%s.UTF-8' % new_locale)

    def get_month_names(self, include_locale):
        pool = []
        self.set_locale()
        for m in range(1, 13):
            dt = datetime.date(year=1970, month=m, day=1)
            entry = dt.strftime("%B").lower()
            if entry not in pool:
                pool.append(entry)
        if include_locale:
            self.set_locale(new_locale=include_locale)
            for m in range(1, 13):
                dt = datetime.date(year=1970, month=m, day=1)
                entry = dt.strftime("%B").lower()
                if entry not in pool:
                    pool.append(entry)
            self.set_locale()
        self.months = pool

    def get_week_names(self, include_locale):
        pool = []
        self.set_locale()
        for m in range(1, 8):
            dt = datetime.date(year=1970, month=1, day=m)
            entry = dt.strftime("%A").lower()
            if entry not in pool:
                pool.append(entry)
        if include_locale:
            self.set_locale(new_locale=include_locale)
            for m in range(1, 8):
                dt = datetime.date(year=1970, month=1, day=m)
                entry = dt.strftime("%A").lower()
                if entry not in pool:
                    pool.append(entry)
            self.set_locale()
        self.days = pool

    def only_first_char_upper_case(self, entry):
        if entry[0] in string.ascii_uppercase:
            entry = entry[1:]
            for x in list(string.ascii_uppercase):
                if x in entry:
                    return False
            return True
        return False

    def special_in_predictable_place(self, entry):
        if entry[-1] in self.common_special:
            entry = entry[0:-1]
            for x in list(self.common_special):
                if x in entry:
                    return False
            return True
        return False

    def match_against(self, entry, selection):
        for x in selection:
            if not isinstance(x, str):
                x = str(x)
            if x in entry.lower():
                return x
        return False

    def check_common_number_sequence(self, entry):
        return self.match_against(entry, self.common_numbers)

    def contains_predictable_word(self, entry, additional_words=None):
        if additional_words:
            test_entry = self.match_against(entry, additional_words)
            if test_entry:
                return test_entry
        test_entry = self.match_against(entry, self.common_words)
        if test_entry:
            return test_entry
        test_entry = self.match_against(entry, self.months)
        if test_entry:
            return test_entry
        test_entry = self.match_against(entry, self.days)
        if test_entry:
            return test_entry
        test_entry = self.match_against(entry, self.seasons)
        if test_entry:
            return test_entry
        test_entry = self.match_against(entry, self.years)
        if test_entry:
            return test_entry
        return False

    def check_special_char_amount(self, entry):
        not_special = string.ascii_letters + string.digits
        num_special = 0
        for char in entry:
            if char not in not_special:
                num_special += 1
        return num_special

    def check_numer_amount(self, entry):
        digits = string.digits
        num_digits = 0
        for char in entry:
            if char in digits:
                num_digits += 1
        return num_digits

    def check_external_names(self, entry, input_names):
        if not input_names:
            return False
        input_names = [x.lower() for x in input_names]
        return self.match_against(entry, input_names)

    def secure_verified(self, entry):
        if len(entry) < 10:
            return False
        if len(entry) > 128:
            return False
        cr = 0
        for x in entry:
            if x in string.ascii_lowercase:
                cr += 1
                break
        for x in entry:
            if x in string.ascii_lowercase:
                cr += 1
                break
        for x in entry:
            if x in string.digits:
                cr += 1
                break
        if self.check_special_char_amount(entry) > 1:
            cr += 1
        return cr >= 3

    def __init__(self, include_locale=None, extra_words=None):
        self.get_week_names(include_locale=include_locale)
        self.get_month_names(include_locale=include_locale)
        self.get_year_span()
        if extra_words:
            self.common_words.extend(extra_words)

    def check_entry(self, entry, external_names=None, additional_words=None):
        return {
            "entry": entry,
            "length": len(entry),
            "predictable_word": self.contains_predictable_word(entry, additional_words=additional_words),
            "only_first_uppercase": self.only_first_char_upper_case(entry),
            "special_predictable_place": self.special_in_predictable_place(entry),
            "predictable_number_sequence": self.check_common_number_sequence(entry),
            "special_characters": self.check_special_char_amount(entry),
            "numbers": self.check_numer_amount(entry),
            "might_be_secure": self.secure_verified(entry),
            "contains_custom_name": self.check_external_names(entry, external_names)
        }

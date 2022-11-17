from collections import OrderedDict

from safepass.commons import Common


class Tester:
    input_pool = []
    stats = {
        "length": {},
        "unique": 0,
        "longest": 0,
        "average_length": 0,
        "shortest": 99,
        "predictable_words": {},
        "case": {
            "only_first": 0,
            "random": 0
        },
        "special_predictable": {
            "last_character": 0,
            "random": 0
        },
        "predictable_number_sequence": {},
        "contains_custom": {},
        "number_of_digits": {},
        "number_of_special": {},
        "might_be_secure": {
            "yes": 0,
            "no": 0
        }
    }
    extra_words = []

    def add_words(self, words: list):
        self.extra_words = words

    def run_on_entries(self, entries: list, include_locale=None, external_names=None, additional_words=None):
        total = []
        parser = Common(include_locale=include_locale, extra_words=self.extra_words)
        self.input_pool = entries
        for entry in entries:
            entry = entry.strip()
            result = parser.check_entry(entry, external_names=external_names, additional_words=additional_words)
            total.append(entry)
            entry_length = result["length"]
            if entry_length in self.stats["length"].keys():
                self.stats["length"][entry_length] += 1
            else:
                self.stats["length"][entry_length] = 1
            predictable_word = result.get("predictable_word", None)
            if predictable_word:
                if predictable_word in self.stats["predictable_words"]:
                    self.stats["predictable_words"][predictable_word] += 1
                else:
                    self.stats["predictable_words"][predictable_word] = 1

            numbers = result.get("numbers", None)
            if numbers:
                if numbers in self.stats["number_of_digits"]:
                    self.stats["number_of_digits"][numbers] += 1
                else:
                    self.stats["number_of_digits"][numbers] = 1

            might_be_secure = result.get("might_be_secure", None)
            if might_be_secure:
                self.stats["might_be_secure"]["yes"] += 1
            else:
                self.stats["might_be_secure"]["no"] += 1

            special = result.get("special_characters", None)
            if special:
                if special in self.stats["number_of_special"]:
                    self.stats["number_of_special"][special] += 1
                else:
                    self.stats["number_of_special"][special] = 1

            predictable_number = result.get("predictable_number_sequence", None)
            if predictable_number:
                if predictable_number in self.stats["predictable_number_sequence"]:
                    self.stats["predictable_number_sequence"][predictable_number] += 1
                else:
                    self.stats["predictable_number_sequence"][predictable_number] = 1
            custom_word = result.get("contains_custom_name", None)
            if custom_word:
                if custom_word in self.stats["contains_custom"]:
                    self.stats["contains_custom"][custom_word] += 1
                else:
                    self.stats["contains_custom"][custom_word] = 1
            if result.get("only_first_uppercase", None):
                self.stats["case"]["only_first"] += 1
            else:
                self.stats["case"]["random"] += 1
            if result.get("special_predictable_place", None):
                self.stats["special_predictable"]["last_character"] += 1
            else:
                self.stats["special_predictable"]["random"] += 1
        unique_list = []
        for x in total:
            if len(x) > self.stats['longest']:
                self.stats['longest'] = len(x)
            if len(x) < self.stats['shortest']:
                self.stats['shortest'] = len(x)
            if x not in unique_list:
                unique_list.append(x)
        self.stats['average_length'] = int(sum([len(x) for x in total]) / len([len(x) for x in total]))
        self.stats["unique"] = len(unique_list)


class TextConverter:

    @staticmethod
    def order_dict_by_value(data: dict, reverse=True):
        return OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=reverse))

    output = ""

    def write_output(self, line="", blank_lines=1):
        self.output += line
        self.output += "\n" * blank_lines

    def __init__(self, data):
        self.write_output("Average length: %d" % data.get("average_length"))
        self.write_output("Shortest length: %d" % data.get("shortest"))
        self.write_output("Longest length: %d" % data.get("longest"), blank_lines=2)
        self.write_output("Uppercase")
        self.write_output("Only first (most predictable): %d" % data['case'].get("only_first", 0))
        self.write_output("Multiple or random (less predictable): %d" % data['case'].get("random", 0), blank_lines=2)
        self.write_output("Special Characters")
        self.write_output("Last character (most predictable): %d" % data['special_predictable'].get("last_character", 0))
        self.write_output(
            "Multiple or random (less predictable): %d" % data['special_predictable'].get("random", 0), blank_lines=2
        )

        self.write_output("Number of Special Characters")
        num_special = self.order_dict_by_value(data['number_of_special'])
        for x in num_special:
            self.write_output("%d -> %d times" % (x, num_special[x]))
        self.write_output()

        self.write_output("Number of Digits")
        num_special = self.order_dict_by_value(data['number_of_digits'])
        for x in num_special:
            self.write_output("%d -> %d times" % (x, num_special[x]))
        self.write_output()

        self.write_output("Predictable Number Sequences")
        num_special = self.order_dict_by_value(data['predictable_number_sequence'])
        for x in num_special:
            self.write_output("%s -> %d times" % (x, num_special[x]))
        self.write_output()

        self.write_output("Predictable Words")
        num_special = self.order_dict_by_value(data['predictable_words'])
        for x in num_special:
            self.write_output("%s -> %d times" % (x, num_special[x]))
        self.write_output()

        if data['contains_custom']:
            self.write_output("Contains Defined Entries")
            num_special = self.order_dict_by_value(data['contains_custom'])
            for x in num_special:
                self.write_output("%s -> %d times" % (x, num_special[x]))
            self.write_output()

        self.write_output("Entry Length")
        num_special = self.order_dict_by_value(data['length'])
        for x in num_special:
            self.write_output("%d -> %d times" % (x, num_special[x]))
        self.write_output()
        self.write_output("Matches Complexity (length/uppercase/digit/lowercase/special)")
        self.write_output("Yes: %d" % data['might_be_secure'].get("yes", 0))
        self.write_output("No : %d" % data['might_be_secure'].get("no", 0))

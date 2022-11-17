import optparse
import json
import sys

from safepass.tester import Tester, TextConverter


def args_to_list(input_string, sep=",") -> list:
    """
    Parse a string into a list separated by :sep
    :param input_string:
    :param sep:
    :return:
    """
    if not input_string:
        return []
    if "," in input_string:
        return [x.strip() for x in input_string.split(sep)]
    return [input_string]


def load_file(input_file, delimiter=None):
    """
    Load an input file and preprocess the data
    :param input_file:
    :param delimiter:
    :return:
    """
    output = []
    with open(input_file, "r") as in_file:
        data = [x.strip() for x in in_file.read().strip().split("\n")]
        for entry in data:
            if delimiter and delimiter in entry:
                temp_entry = entry.split(delimiter)
                entry = delimiter.join(temp_entry[1:])
            if entry:
                output.append(entry)
    return output


def main():
    parser = optparse.OptionParser()
    parser.add_option(
        "-f", "--file", dest="in_file", default=None, help="The input file to process (required)"
    )
    parser.add_option(
        "--names", dest="names", default=None,
        help="Comma separated extra options to include (like company names)"
    )
    parser.add_option(
        "--delimiter", dest="delimiter", default=None,
        help="Delimiter to remove prefixes from entries (like domains and usernames)"
    )
    parser.add_option(
        "--locale", dest="locale", default=None,
        help="An additional locale for generating common words like days and months"
    )
    parser.add_option(
        "--text", dest="text", default=False, action="store_true",
        help="Return the output in text instead of JSON"
    )
    parser.add_option(
        "--entries", dest="entries", default=None,
        help="A list of extra common entries or words"
    )
    (options, args) = parser.parse_args()
    if not options.in_file:
        parser.print_help()
        sys.exit(0)
    entries = load_file(options.in_file, delimiter=options.delimiter)
    tester = Tester()

    if options.entries:
        tester.add_words(
            load_file(options.entries)
        )

    tester.run_on_entries(
        entries,
        include_locale=options.locale,
        external_names=args_to_list(options.names)
    )
    results = tester.stats
    if options.text:
        sys.stdout.write(TextConverter(results).output)
    else:
        sys.stdout.write(json.dumps(results))


if __name__ == "__main__":
    main()

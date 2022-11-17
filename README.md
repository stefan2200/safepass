# Safepass
Just another password security analysis tool

Installing
```shell
git clone https://github.com/stefan2200/safepass
cd safepass
python3 setup.py install
```

Example usage
```shell
safepass
Usage: safepass [options]

Options:
  -h, --help            show this help message and exit
  -f IN_FILE, --file=IN_FILE
                        The input file to process (required)
  --names=NAMES         Comma separated extra options to include (like company
                        names)
  --delimiter=DELIMITER
                        Delimiter to remove prefixes from entries (like
                        domains and usernames)
  --locale=LOCALE       An additional locale for generating common words like
                        days and months
  --text                Return the output in text instead of JSON
  --entries=ENTRIES     A list of extra common entries or words
  
  
$ safepass -f passwords.example.txt
{
   "length":{
      "10":2,
      "8":1,
      "7":1,
      "17":1,
      "28":1,
      "11":1,
      "12":1
   },
   "unique":8,
   "longest":28,
   "average_length":12,
   "shortest":7,
   "predictable_words":{
      "secure":2,
      "password":1,
      "summer":1,
      "august":1
   },
   "case":{
      "only_first":5,
      "random":3
   },
   "special_predictable":{
      "last_character":5,
      "random":3
   },
   "predictable_number_sequence":{
      "123":3,
      "2022":1,
      "321":1
   },
   "contains_custom":{
      
   },
   "number_of_digits":{
      "3":4,
      "2":1,
      "4":1
   },
   "number_of_special":{
      "1":5,
      "4":1,
      "3":1
   },
   "might_be_secure":{
      "yes":6,
      "no":2
   }
}


$ safepass -f passwords.example.txt --text --locale nl_NL --entries entries.example.txt --delimiter ":"
Average length: 10
Shortest length: 6
Longest length: 17

Uppercase
Only first (most predictable): 5
Multiple or random (less predictable): 3

Special Characters
Last character (most predictable): 5
Multiple or random (less predictable): 3

Number of Special Characters
1 -> 5 times
4 -> 1 times

Number of Digits
3 -> 4 times
2 -> 1 times
4 -> 1 times

Predictable Number Sequences
123 -> 3 times
2022 -> 1 times
321 -> 1 times

Predictable Words
secure -> 2 times
password -> 1 times
mycorp -> 1 times
summer -> 1 times
august -> 1 times

Entry Length
10 -> 2 times
8 -> 1 times
7 -> 1 times
17 -> 1 times
6 -> 1 times
11 -> 1 times
12 -> 1 times

Matches Complexity (length/uppercase/digit/lowercase/special)
Yes: 5
No : 3
```


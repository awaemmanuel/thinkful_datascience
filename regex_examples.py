'''
    Sample examples of regex in python.
    Online regex analysis of choice - https://regex101.com/#python
'''
import re

print re.match(r'.*', 'az09_&^%$\nfoo', re.DOTALL).group()
print re.match(r'.*', 'az09_&^%$\nfoo', re.DOTALL | re.MULTILINE).group()

sample_pattern = r'^.*$'
test_string = 'foo bar baz'
result_match_object = re.match(sample_pattern, test_string)
print result_match_object.group()

test_string2 = 'foo \n bar \n baz'
result_None = re.findall(sample_pattern, test_string2, re.M | re.DOTALL )
print result_None # ['foo \n bar \n baz']

finditer_results = re.finditer(sample_pattern, test_string2, re.M)
for i in finditer_results: 
    print(i.group()) # prints each line as shown in prior list.

txt1 = '''You can reach us at 555.867.5309, or email us at a.b.c234@mta.info.com'''
txt2 = '''Contact us at (555) 123-0987'''
phone_matcher = re.compile(
    r'''
    (\d{3}) # match any three numbers (the parentheses indicate it's a capture group)
    .*?     # followed by an minimal amount of characters to match the rest 
    (\d{3}) # followed by 3 numbers (a capture group)
    [-.]  # followed by a dash, period, or whitespace
    (\d{4}) # followed by 4 numbers (another capture group)
    ''',
    flags=re.VERBOSE | re.DOTALL)

results = []
for txt in (txt1, txt2):
    result = phone_matcher.search(txt)
    if result is not None:
        results.append(result.groups())
print results
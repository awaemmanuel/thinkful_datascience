'''
    Sample Unit Test examples
'''
import unittest

class ExampleTests(unittest.TestCase):
    def test_fizzbuzz_good(self):
        output = []
        for n in xrange(100):
            output.append(str(fizzbuzz(n) + '\n'))
        
        with open("fizzbuzz-output.txt", "r") as expected:
            i = 0
            for line in expected:
                if line == output[i]:
                    print("Success!")
                    i += 1
                else:
                    print("Nope. Try Again.")

def fizzbuzz(n):
    ret = ''
    if not (n%3):
        ret += 'fizz'
    if not (n%5):
        ret += 'buzz'
    return ret or str(n)

def create_expectedfile(n, output_file="fizzbuzz-output.txt"):
    with open(output_file, "w") as expected:
        for n in xrange(n):
            expected.write(fizzbuzz(n) + "\n")
    
if __name__ == '__main__':
    #create_expectedfile(100)
    unittest.main()
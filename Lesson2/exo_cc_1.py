import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.
def string_times(string, n):
    if(n >= 0):
        return string * n
    return

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
#longueur=min(len(nums) & 4)
def array_front9(nums):
    return 9 in nums[:4]


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    count = 0
    last2char = string[-2:]
    for i in range(0, len(string)-2):
        if last2char == string[i:i+2]:
            count += 1
    return count


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    #Charles's solution: map(array, lambda x: x.length)
    return [len(w) for w in array]

#write fizbuzz programm
def fizbuzz():
    for i in range(1,101):
        isMultiple3 = i%3 == 0
        isMultiple5 = i%5 == 0
        printnumber = ''
        if( not isMultiple3  and not isMultiple5):
            printnumber = i
        if(isMultiple3):
            printnumber += 'Fizz'
        if(i%5 == 0):
            printnumber += 'Buzz'
        print(printnumber)

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    string = str(number)
    return [int(string[i]) for i in range(0,len(string))]

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    # Charles's solution : ' '.join[x[1:]+x[0]+'ay' for x in text.split(' ')].capitalize()
    pigLatinWords = [w[1:]+w[0].lower()+'ay' for w in text.split(' ')]
    return (' '.join(pigLatinWords)).capitalize()
    
    

#Write a proramm that returna dictionary of occurences of the alphabet for a given string.
# Test it with the Lorem upsuj
#"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
def occurences(text):
    result = {}
    for c in text.lower():
        if c.isalpha():
            if c in result.keys():
                result[c] += 1
            else:
                result[c] = 1
    return result

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    fizbuzz()
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)
        self.assertEqual(array_front9([1, 2, 3]) , False)
        self.assertEqual(array_front9([]) , False)


    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )
        self.assertEqual(string_times('Error', -5), None )
        self.assertEqual(string_times('', 0),'' )
#
    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)
        self.assertEqual(last2('axxxaaxx') , 2)
        self.assertEqual(last2('a') , 0)
        self.assertEqual(last2('') , 0)


    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])
#
    def testNumber2Digits(self):
        self.assertEqual(number2digits(4) , [4])
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")
        self.assertEqual(pigLatin("Oneword") , "Newordoay")

    def testOccurences(self):
        self.assertEqual(occurences("The text") , {'t': 3, 'h':1, 'e':2, 'x':1})
        self.assertEqual(occurences("Hello, my name is Nazha BOUCHIA") , {'h': 3, 'e':2, 'l':2, 'o':2, 'm':2, 'y':1, 'n':2, 'a':4, 'i':2, 's':1, 'z':1, 'b':1, 'u':1, 'c':1})


def main():
    unittest.main()

if __name__ == '__main__':
    main()


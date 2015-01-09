#!/usr/bin/python

from nltk.stem.snowball import SnowballStemmer
import string

def parseOutText(f):
    """ given an opened email file f, parse out all text below the
        metadata block at the top
        (in Part 2, you will also add stemming capabilities)
        and return a string that contains all the words
        in the email (space-separated) 
        
        example use case:
        f = open("email_file_name.txt", "r")
        text = parseOutText(f)
        
        """


    f.seek(0)  ### go back to beginning of file (annoying)
    all_text = f.read()

    ### split off metadata
    content = all_text.split("X-FileName:")
    words = ""
    if len(content) > 1:
        ### remove punctuation
        text_string = content[1].translate(string.maketrans("", ""), string.punctuation)

        ### project part 2: comment out the line below
        words = text_string
        
        # Eric: remove the escape characters
        escape_char_list = ["\a", "\b", "\t", "\n", "\v", "\f", "\r"]
        for escape_char in escape_char_list:
            words = words.replace(escape_char, " ")
        ### split the text string into individual words, stem each word,
        ### and append the stemmed word to words (make sure there's a single
        ### space between each stemmed word)
        stemmer = SnowballStemmer("english")
        word_list = words.split(" ")
        
        stemmed_word_list = []
        for word in word_list:
            if word != "":
                word = stemmer.stem(word)
                stemmed_word_list.append(word)
            
        # Join the word into string with sep = " "    
        stemmed_string = string.join(stemmed_word_list, sep = " ")

    return stemmed_string

    

def main():
    #ff = open("../text_learning/test_email.txt", "r")
    ff = open("../enron_mail_20110402/maildir/bailey-s/deleted_items/101.", "r")
    text = parseOutText(ff)
    print text



if __name__ == '__main__':
    main()


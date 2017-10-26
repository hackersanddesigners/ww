import string
import random

#Shaney stuff - JBG
def choice(words):
  #assumes words is non-empty
  random.seed
  index = random.randint(0,len(words)-1)
  return words[index]

def do_shaney(text):
  output = ''
  words = string.split(text)
  end_sentence = []
  dict = {}
  prev1 = ''
  prev2 = ''
  for word in words:
    if prev1 != '' and prev2 != '': 
      key = (prev2, prev1)
      if dict.has_key(key):
        dict[key].append(word)
      else:
        dict[key] = [word]
        if (prev1[-1:] == '.' or prev1[-1:] == '?' or prev1[-1:] == '!'):
          end_sentence.append(key)
    prev2 = prev1
    prev1 = word

  if end_sentence == []: 
    print 'Sorry, there are no sentences in the text.'
    return

  key = ()
  count = 10

  while 1:
    if dict.has_key(key):
      word = choice(dict[key])
      #print word,
      output += word + ' ' 
      key = (key[1], word)
      if key in end_sentence:
        #print
        count = count - 1 
        key = choice(end_sentence)
        if count <= 0:
          break
    else:
      key = choice(end_sentence)
  return output



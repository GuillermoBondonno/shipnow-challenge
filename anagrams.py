from collections import Counter

def anagrams(word, possible_anagrams):
  result = []
  for w in possible_anagrams:
    if len(word) == len(w):
      if Counter(word) == Counter(w):
        result.append(w)
  
  return result
def frog_jump(x, y, d):
  result = 0
  current = x
  while current < y:
    current += d
    result += 1

  return result

print(frog_jump(10,9,30))
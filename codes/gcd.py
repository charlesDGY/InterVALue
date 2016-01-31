def gcd(a, b):
  if a < b:
    a, b = b, a

  while b != 0:
    temp = a % b
    a = b
    b = temp

  return a

r = gcd(2,4)
print r

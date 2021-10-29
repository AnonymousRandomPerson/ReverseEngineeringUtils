def divide(dividend, divisor):
  if divisor == 0:
    raise Exception

  sign_check = dividend ^ divisor

  divisor = abs(divisor)
  dividend = abs(dividend)

  if dividend < divisor:
    quotient = 0
  else:
    shift_amount = 1
    shift_threshold = 1 << 31
    while divisor < shift_threshold and divisor < dividend:
      divisor = divisor << 1
      shift_amount = shift_amount << 1

    quotient = 0
    while divisor != 0:
      if dividend >= divisor:
        dividend -= divisor
        quotient |= shift_amount
      divisor = divisor >> 1
      shift_amount = shift_amount >> 1

  if sign_check < 0:
    quotient = -quotient

  return quotient

dividend = 475
divisor = 10
quotient = divide(dividend, divisor)
print(quotient)
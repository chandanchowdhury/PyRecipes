#
#
# 

def SumOfNumbersUpto(n):
'''
Name: SumOfNumbersUpto
Purpose: Return the sum of all numbers upto the number it called with.
'''
	return ((n+1)*n)/2

def SumOfSquareNumbersUpto(n):
'''
Name: SumOfSquareNumbersUpto
Purpose: Return the sum of all square numbers upto the number it called with.
'''
	return (n*(n + 1)*(2*n + 1))/6 

def ListOfPrimeFactors(n):
'''
Name: ListOfPrimeFactors
Purpose: Return the list of prime factors for a number.

ref: http://stackoverflow.com/questions/23287/largest-prime-factor-of-a-number
'''
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n /= d
        if d == 2:
            d = 3
        else:
            d = d + 2
            
        if d*d > n:
            if n > 1: 
                factors.append(n)
            break
            
    return factors

def LCM(x,y):    
'''
Name: LCM
Purpose: Calculate and return the LCM of two numbers.
'''
    # if both are equal, return any    
	if x==y:
		return x
	# if any of them is 1, return the other
	elif x==1:
		return y
	elif y==1:
		return x    
											    
	# swap to make x greater
	if y>x:
		z = x
		x = y
		y = z
																				    
	# if x is multiple of y, the LCM is x
	if x%y == 0:
		return x        
																									    																								    
	lcm = 1
	z = 2
	while(z <= y):
		#print "----"
		#print cs("Z: ",z)
		#print cs("X: ",x)
		#print cs("Y: ",y)
																																						        
		# if divisible by a common number (z), LCM= LCM*z        
		while(x%z==0 and y%z==0 and x>1 and y>1):
			#print cs("Z: ",z)
			#print cs("X%z: ",x%z)
			#print cs("Y%z: ",y%z)
			lcm *= z            
			x = int(floor(x / z))
			y = int(floor(y / z))
			#print cs("X: ",x)
			#print cs("Y: ",y)
																																																																				        
 		z += 1

	return lcm*x*y


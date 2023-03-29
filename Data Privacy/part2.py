import numpy as np
import struct

# Input: Float
# Output: String representing a float
#    - 1 sign bit
#    - 11 bits for the exponent
#    - 52 bits for the mantissa
def float_to_binary(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!d', num))



# Input: String representing a float
#    - 1 sign bit
#    - 11 bits for the exponent
#    - 52 bits for the mantissa
# Output: Float
def binary_to_float(b):
    bf = int(b, 2).to_bytes(8,'big')  
    return struct.unpack('>d', bf)[0]



def my_laplace(scale=1): 
    
    # float between 0 and 1
    # not every possible representable float in that range
    u = np.random.uniform()
    
    # either 0 or 1
    b = np.random.randint(2)
    
    # switches the sign of log(u)
    # implementation of the log function also does not output every possible float
    l = (2*b-1)*np.log(u)
    return l*scale


def generate_cases(pow_val):
    lst = []
    for i in range(pow(2,pow_val)):
        num = bin(i).replace('0b', '')
        if len(num) < pow_val:
            num = '0'*(pow_val-len(num)) + num
            
        lst.append(num)
    return lst

# Should return `True` when y is believed to be an output of my_laplace(scale).
# Otherwise should return `False`
def is_scaled_laplace_img(y, scale):

    # make sure y is negative
    y = -1*y if y>0 else y
    
    # find an approximate x value from the given y and scale
    x_approx = np.exp(y/scale)
    #     print(x_approx)
    
    # get the binary reprentation of x_approx
    x_approx_bin = float_to_binary(x_approx)
    #     print(x_approx_bin)

    # Loop over making changes to this binary representation
    #  by flipping one bit at a time
    #  One of such cases should find itself in set U
    
    # Generating all cases of bit flips for least significant bits
    pow_val = 5
    lst = generate_cases(pow_val)
    start = x_approx_bin[:-pow_val]
    
    for x in lst:
        num_bin = start + x
        num_float = binary_to_float(num_bin)
        if (num_float%(2**(-53)) == 0) and (scale*np.log(num_float) == y):
            return True
        
    return False


# This method will run your implementation of is_scaled_laplace_img 1000 times
# on unshifted samples, and then 1000 times on shifted samples.
# 
# When completed, this method should output numbers that are as different as
# possible.
def test(): 
    scale = 1.2 # you can try with different scales
    # first, run on unshifted samples
    total_0 = 0
    for i in range(1000):
        l = np.random.laplace(scale=scale) 
        # switch to the line below to test on my_laplace instead
        #l = my_laplace(1.2) 
        if l > 0:
            l = l*-1
        if is_scaled_laplace_img(l,scale):
            total_0 += 1
    print('True outputs on total on unshifted samples: ', total_0) # should be high, ideally 1000

    # second, run on shifted samples
    total_1 = 0
    for i in range(1000):
        l = 1.0 + np.random.laplace(scale=scale) 
        # switch to the line below to test on my_laplace instead
        #l = my_laplace(1.2) 
        if l > 0:
            l = l*-1
        if is_scaled_laplace_img(l,scale):
            total_1 += 1
    print('True outputs on total on shifted samples:   ', total_1) # should be low


################################################################################
# driver/test code below here.
################################################################################
if __name__ == "__main__":
    test()
    exit()


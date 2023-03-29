from Crypto.Hash import SHA256

# public exponent
e = 3

# public modulus
N = 0x00bc9e8d81ce1de63e0ab302030e5c0595bf5d2c30fd2660ac9299431a29c4e231a675d684e35415ad87ca738509469aaa0455d62543ab9265d71767f55c7f5fdbb9e2618112212178417c21b4e8a98ab0980fd67864ed7e7e3dcefc3143d5e5d3be2bf0c36c75c977052fedbfdc1c2e448710338fad4fe0e3fa8fc2c662e3466d358df6618dc0a63f45395e5c5aa88d15a49ce2be791acbcd81e28533228918f6abb57e023145a97afea85ad238686f51409017a4d6af8687f7a9438f09a2d9d9e619abdde8e67fc95af23dc97b4a595baa26bfeaf16d31b93e3e1bae1f5813fcd9ef2c8f93df2dd4a779626d07852f120e6b84d936abb811fd4525d9a0cf6621

# modulus length, in bytes. 256 bytes is 2048 bits
k = 256

# You won't need to call this. It is used by verification.
def modexp(base, exp, modulus):
    ret = 1
    while exp > 0:
        if exp % 2 == 1:
            ret = (ret*base) % modulus
        base = (base*base) % modulus
        exp = exp >> 1
    return ret

# The buggy verification algorithm. This is explained in the assignment.
# Arguments k, N, e, and sig should be integers.
# Argument msg should be a bytes or bytearray.
def buggy_verify(k, N, e, msg, sig):
    digest = SHA256.new(msg).digest()
    #print('Buggy verify: Input msg =',msg)
    #print('Buggy verify: Input digest =\n',digest)

    sig_blk_int = modexp(sig, e, N)
    #print('Buggy verify: Sig exponentiates to integer:\n ', sig_blk_int)
    sig_blk = sig_blk_int.to_bytes(k,byteorder='big')
    #print('Buggy verify: Sig exponentiates to bytes:\n',sig_blk)
    #print('recovered len:',len(sig_blk))

    if sig_blk[0] != 0 or sig_blk[1] != 1:
        # print('invalid leading bytes (',sig_blk[0],sig_blk[1],')') 
        return False
    digest_start_byte = 0
    # this is the buggy part
    for i in range(2,len(sig_blk)):
        if sig_blk[i] == 255:
            continue
        elif sig_blk[i] == 0:
            digest_start_byte = i + 1
            break
        else:
            #print('invalid padding byte %d (%d) '%(i,ord(sig_blk[i])))
            return False
    recovered_digest = sig_blk[digest_start_byte:digest_start_byte+32]
    #print('Buggy verify, recovered_digest:\n',repr(recovered_digest))
    return digest == recovered_digest


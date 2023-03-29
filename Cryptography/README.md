# Assignment 4: Cryptography

This assignment covers how three different cryptography vulnerabilities are exploited: One each with encryption, hash-based MACs, and RSA digital signatures. All of these attacks can be accomplished with relatively small amounts of code in Python3, but require some reading on your part to understand the setting and devise an attack.

## Tech Set-Up and Included Files

You will need to implement this assignment in Python3. You may do this on your own machine or on department machine like `linus.cs` or a CSIL machine. It is fine to run the "attacks" here on shared machines, since they do not consume many resources, target anything shared, or doing anything suspicious that would trip alarms.

The only special package you will need is [pycrypto](https://pypi.org/project/pycrypto/). You can install this package with the command

```
python3 -m pip install pycrypto
```
on most systems when online (if you already use Python3 and like another package manager, then `pycrypto` should be available there). If you see a Python error complaining about the `Crypto` module not being found, then you have not successfully installed this package.

The following files are provided in `assignment4.tar`:

- `assignment4.py`: This contains skeleton code. You will implement your code for Problem 1 (which is not of a prescribed format), and also functions
`problem2()` and `problem3()` here.
- Files `problem1.py`, `problem2.py`, `problem3.py`. You may modify these if you want, but your solutions should work with unmodified versions of these files.
- `pymd5.py`: A purely Python implementation of the MD5 hash function, used in Problem 2.
- `problem2_example.py`: An example of a length extension attack against MD5 to help with Problem 2.

## Problem 1: One-Time Pad Reuse (34 points)

In lecture and the readings it was stated that reusing a one-time pad leads to attacks. In this problem you'll get to see hands-on how an attack can exploit reused pads.

The file `problem1.py` contains four ciphertexts that were encrypted with the same one-time pad; your job is to recover the plaintexts in them.

Before starting, please ensure that you understand how these ciphertexts are encoded. If you open the file, you will see four long strings consisting of hexadecimal digits that form an array called `ctxts_hex`. These strings are actually representing unprintable bytes, which are a pain to include directly as text. The array `ctxts_bin` is computed at the bottom of the file and contains the actual bytes you should attack. This array is computed by decoding the first array, where each pair of hex digits is interpreted as a byte value.

The plaintexts are all English text with punctuation that includes spaces, periods, semicolons, etc. They have upper and lowercase letters. All of these are encoded as [ascii](https://en.wikipedia.org/wiki/ASCII); see the [printable characters table](https://en.wikipedia.org/wiki/ASCII#Printable_characters) in particular. This means that a byte with hex value `41` represents `A`, for example. The ciphertext bytes largely won't be printable.

I recommend you read about and implement *crib-dragging*; it tends to work well and not involve much guesswork. You read about it in section 5.5 of [Crypto 101](https://www.crypto101.io/), a free online textbook. Other ad-hoc approaches are fine too, but be sure you can explain what you did afterwards.
 
#### Python3 Quirks: `string`, `bytes`, `bytearray`


Working with bytes in Python3 is nice, but one be careful to use the correct data types. Python3 has three data types that cause some confusion: `string`, `bytes`, and `bytearray`.  How you declare your variable determines which type you are getting:

- `s = 'abc'` makes `s` a `string`
- `s = b'abc'` makes `s` a `bytes`
- `s = bytearray(b'abc')` makes `s` a `bytearray`
- `s = bytearray(16)` makes `s` a `bytearray` with
        16 zero (NULL) bytes.

Note that `s = bytearray('abc')` will throw an error; You have to pass in
bytes for that type of declaration, as we did in the third example.

Strings are nasty to deal with in this assignment because Python treats them
rather abstractly in effort to be inclusive of languages that use characters not encodeable in individual bytes (i.e. most languages). In Python3's abstraction, a `string` on its own has no bit representation. To get a bit representation of a string, you need to "encode" it (and you get a string back from bytes by "decoding"). I was able to solve all of these problems without needed to
encode/decode, so if you find yourself doing that, perhaps there is a simpler
way.

Since you are manipulating binary representations of bytes, you will want to stick with `bytes` and `bytearray` everywhere in your code.  Also `bytearray`'s allow for appending, concatenation, and other handy operations that make Python3 nice, so you will usually want to use those over `bytes`. If see Python3 errors that involve encoding and decoding, it probably because your code is mixing `string` and `bytes` or `bytearray` variables, often because you forgot the `b` in front (i.e. `'abc'` instead of `b'abc'`).
 
#### What to submit for Problem 1


You approach to solving this problem will likely involve some automated steps mixed with some manual work. Thus your code won't consist of a simple function, but probably several smaller helper functions that you use at various points. In the file `assignment4.py`, 

- Include your code in the space marked for Problem 1. **Please document this code to explain what you used it for.** It should be consistent with your text explanation that you submit on Gradescope. We will primarily grade this by checking that you thought through this problem for yourself; It needs to be comprehensible but not beautiful code. We understand that this class may be your first encounter with Python3.
- Populate the array `ptxts` in the function `problem1()` with the four plaintexts you recover **in order**. If you are unsure about some characters of the plaintexts, you should just guess at them instead of deleting them. We will perform a character-by-character scan to see how many are correct. **You do not need to recover these automatically; They can be hardcoded. But please still have the function return `ptxts` to make grading easier.**
- Respond to the appropriate prompt for Problem 1 on Gradescope.


## Problem 2: Length Extension Attacks (33 points)

### Introduction

In lecture we briefly saw that constructing a MAC from a hash function
is a delicate task. A common insecure construction is
```
    MAC(K,M) := H(K+M),
```
where "+" is string concatenation. This fails even if the key is large
and the hash function ``H`` is reasonably secure. In this problem,
we'll take the hash to be MD5, which is insecure and should be never be used.
(We use MD5 here for two reasons: First, a good Python library is available.
Second, secure hashes like SHA256 are vulnerable to the same attack, so
the lesson is the same.)

This construction is vulnerable to a so-called *length extension attack*, which we explain in detail shortly. It is based on the following principle: Due to the way the MD5 algorithm works, it is possible for someone to take the hash `h` of an unknown message `X` and compute the hash of `X+S` where `S` is a string mostly under their control. That is, given the value
```
h = MD5(X)
```
one can compute the value
```
h' = MD5(X+S)
```
*without knowing `X`*! This leads to a MAC forgery against the construction above: Given the output `t=MAC(K,M)=MD5(K+M)`, one can compute `t'=MAC(K,M+S)=H(K+M+S)` for some partially-chosen string `S`, and this will be accepted as valid. (Here, we took `X=K+M`.)

An untold number of systems have fallen to this attack. A famous example
is a 2009 attack against Flickr (see [here](http://netifera.com/research/flickr_api_signature_forgery.pdf)). 


### Background: How MD5 works 

To begin understanding length extension attacks, we need to look at
how MD5 is structured.
Internally, MD5 works as follows on an input
`X`.  It first performs some pre-processing:
1. Let `L` be the bit-length of `X`.
2. Break `X` into 512-bit blocks, leaving the last block possibly less than 512 bits.
3. Pad the last block up to 512 bits by appending a 1 bit, then
        the appropriate number of zero bits, then a 64-bit encoding of
        `L`. If the last block had fewer than 65 bits of space left,
        add a new 512-bit block.

Now let `X'[1]`, `X'[2]`, ..., `X'[n]` be the 512-bit blocks of the
preprocessed message. To compute the output hash, MD5 initializes a
128-bit state `s` to a default value, and then computes
```
for i = 1,...,n:
    s = f(s,X'[i]) 
```
where `f` some function that outputs 128 bits (`f` is called the *compression function*). The final output is `s`. Intuitively, `s` is an internal "state", and MD5 is chomping up the blocks of (padded) input and updated the state. You can check out how the compression function works on [Wikipedia](https://en.wikipedia.org/wiki/MD5), but it will not be needed for this assignment.

### Background: Length-extension attacks 

Suppose you have the final output `s` of MD5, computed for some input `X`. There's nothing stopping you for computing `f(s,y)` for your chosen block `y`, and indeed from continuing with more blocks (the function `f` is publicly known and it does not take a secret key as input). If you do this, and are careful about padding, you'll have the MD5 hash of the original message plus a suffix.

Take a minute to examine exactly what message the resulting digest corresponds to after performing this attack for one step. The state output `s` corresponds to evaluating MD5 on some message, and that means the message was padded. If we start using `s`, it means the "message" will now contain the padding that was previously added, and we have to pad again. You can see this show up in the example attack below.

### Background: Running a length-extension attack 

A Python implementation of MD5 is given in the included file `pymd5.py`. If you open up this file, `md5_compress` plays the role of `f`. The function `padding` takes an integer as input, and returns the correct padding for message with that bit-length (i.e. a 1 followed by the correct number of zeros). The file has further documentation at the top.

An example attack is given in the included file `problem1_example.py`. Note that the MD5 implementation gives an object that you can "update" many times before asking for the current digest. Internally, this changes the state and counter (of the number of bits processed so far). In the example attack, we use feature that allows us to set the state and counter ourselves (this is the `md5(state=...)` line). Note the tricky step, where we reuse a previous state but set the counter to larger value. This effectively turns the previous padding bits into message bits.


### Your task: Attack FlickUr. 

In this part, you will carry out a version of the Flickr attack
against a new and improved, but still insecure, service called Flick*Ur*. You will use some provided Python3 files to simulate obtaining a URL which contains a MAC tag computed using the vulnerable MD5 construction.

The attack will be simulated using two functions that are implemented in the file `problem2.py`: `get_user_url(cnet)` and `query_url(url)`. These simulate obtaining a token for a non-privileged user and then subsequently submitting a modified token in an attempt to log in as a privileged user.

#### Getting the initial URL: `get_user_url(cnet)`

Calling `get_user_url(cnet)` will return a URL of the form

```
http://www.flickur.com/?api_tag=<token>&uname=<cnet>&role=user
```
The token is computed by the server as

```
MD5(<secret-key> + <rest of url after first ampersand>)
```
 where "+" is string concatenation and
`<secret-key>` is a secret string of unknown length.
More concretely, for this URL, the digest is

```
MD5(<secret-key> + uname=<your-cnet>&role=user).
```
Constructions like this are sometimes used to keep a user "logged in" to a web app (since the user will present the token with each request). We will learn more about this when we study web security. For now, you should think of this string as what a regular user would see in the browser after authenticating to the service.

#### Loading a modified URL: `query_url(url)`

The function `query_url(url)` simulates requesting the `url` from the vulnerable server. The function will parse the submitted url and check the token. Its return value represents if the token was a valid for privileged user, a non-privileged user, or was invalid.


In more detail, when you call the `query_url(url)`, it will check that the domain is correct, and parse out the `api_tag` and the rest of the URL. It will attempt to verify the token value after `api_tag` is correct
for the URL you submitted. If you have the correct token, and your string
contains the `&role=admin`, then it will return a success message for an admin login. If your token is correct but the you don't have the role `admin`, it will return another message indicating an unprivileged login. If your `api_tag` token is incorrect then you will receive an error message. You can have the role assigned multiple times in your URL, and the server will also (unrealistically) tolerate NULL bytes in the URL.

Note that we don't own `flickur.com`, and this is all simulated.


#### What to submit for Problem 2

In your code file, should implement a function `problem2()` that retrieves the initial URL and returns a modified URL that causes the function to return success for an admin login. (Your function does not need to call the `query_url()` with the modified URL, but it may. It should return the URL in any case.) Both the original URL and your modified URL should have *your* CNetID (reminder: David's CNetID is `davidcash` and not his email or numeric ID). For testing, your code should be robust to changes in the secret length (from up to 8 to 64 bytes).

You should note that the secret is available in `problem2.py`, so if you want you can use that to produce valid tokens directly. It should go without saying that your code should work without access to the key (and also for different key values; test your code!).

Your code file `assignment4.py` should contain your implementation of `problem2`. 

In appropriate gradescope prompt, briefly describe any ideas or techniques that you used in your solution (beyond those described above) to make the attack work. Please remember to cite sources.


## Problem 3: RSA Signature Bug Vulnerability (33 points)

In this problem you'll implement a forgery attack against RSA signatures when the verification algorithm does not properly check the format of the padding. This problem first explains how signing and verification is supposed to work. Then it describes a common bug

### PKCS#1 v1.5 Signatures: Signing and Verification

The following is a somewhat simplified version of PKCS#1 v1.5 RSA signatures. Signing works as follows: It takes as input a private key `(N,d)` and a message `M`, and then

1. Computes `X` as

```
    X = 00 01 FF FF FF ... FF 00 <H(M)>
```
Concretely in this problem, `X` will be a 256 bytes long,
and the hash digest `H(M)` will be the output of SHA256, which is 32 bytes
long, so there should be 221 `FF` bytes added. Finally signing
outputs `X^d mod N`.

2. Next it computes the signature `s` as

```
   s = X^d mod N
```
It outputs the signature `s`.

Given a public key `(N,e)`, a message `M`, and a signature `s`, verification works as follows:

1. Compute 

```
   X = s^e mod N
```
here, `X` is a positive integer between 0 and `N-1`.

2. Compute `H(M)`.
3. Check that

```
    X = 00 01 FF FF FF ... FF 00 <H(M)>
```
where this notation means checking that when the number `X` is encoded as a 256-bytes, it starts with `00` byte, then a `01` byte, then 221 `FF` bytes, followed
by another `00` byte and then the last `32` bytes are the hash of `M`.

If this check passes, the verification algorithm should accept the signature.
Otherwise, it should reject.

### Buggy PKCS#1 v1.5 Verification

Now for the buggy version. It seems counter-intuitive that people who make this error, but it arises due to using libraries for encoding and decoding integers, and they can be quite subtle sometimes.

The buggy version of verification computes steps 1. and 2. correctly as above.
In step 3, however, it does the following:

3'. Encode `X` as 256 bytes. Perform the same check as the correct algorithm, except allow for any positive number of `FF` bytes, not just 221 of them. After the `FF` bytes, check that a `00` byte follows, and then check if the 32 bytes following match `H(M)`. Ignore any other trailing bytes.

For example, the buggy version would accept if `X` has the form

```
    X = 00 01 FF 00 <H(M)> ?? ?? ... ??
```
where the `??` bytes are ignored. Note this format has a single `FF` byte rather than 221.


### Forging Signatures against Buggy Verification

In this problem you'll forge a signature on message `M` that is accepted by a buggy verification implementation. This attack assumes the public key `(N,e)` has public exponent `e=3`, which was once common (but isn't anymore).

Recall the setting of a forging attack: You have a public key `(N,e)` and a message `M`, and you'd like to find a signature `s` that is accepted by the buggy verification algorithm for this key and message. This means you must find an `s` such that `s^e mod N` has the form

```
   s^3 mod N = X = 00 01 FF 00 <H(M)> ?? ?? ... ??
```
where the `??` bytes are not checked. (You can have more `FF` bytes if you want, but this isn't important.)

Now for the fun part: The attack first finds a useful value `X` of this form, and then finds `s`. The trick is to find some `X` of this form that is a *perfect cube* as an integer! (This means that there is an integer `s` such that `X = s^3`.) Then, as mentioned in class, it's very easy to find the cube root of this number and use it as the signature (or more likely, you'll pick `X` so that
you already know `s`; there are multiple ways to approach this). *Hint: One approach involves binary search, but it is not the only approach.*


### Your task: Implement a forging attack

The file `problem3.py` contains the following:

- A public key `(N,e)` with `e=3`. These are actually integers; Python handles large integers very easily, so no need to worry about encodings.
- A function `buggy_verify(k, N, e, msg, sig)` that implements the buggy verification algorithm. The arguments `N,e,msg,sig` have the same meanings as above. The argument `k` is the number of bytes in the modulus and should always be 256 in this problem. There are a lot of debugging print statements that are commented out; feel free to use them.

Your task is to fill in the `problem3(msg)` that takes as input a message `msg` (of type `bytes` or `bytearray`) and produces a signature `sig` so that `buggy_verify(k, N, e, msg, sig)` returns `True`.

On Gradescope, respond to the appropriate prompt for problem 3 by explaining briefly how you implemented the attack, and especially how you found the needed perfect cube.


## Submission checklist

This section collects the deliverables for your convenience.

1. Your file `assignment4.py` that contains, in the marked sections
  - Your Problem 1 helper code **with comments** for the graders.
  - The four plaintexts you recovered for problem1 in the `ptxts` array in the `problem1()` function.
  - Implementations of `problem2()` and `problem3()`
2. Responses to questions for Problems 1, 2, and 3 on Gradescope.

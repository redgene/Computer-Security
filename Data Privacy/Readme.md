# Assignment 8: Data Privacy


This assignment covers a few aspects of data privacy from the lectures and readings during Week 8. It is divided into three parts, which are all described in this file.

In the first part, you will implement and experiment with some of the
concepts we covered and observe their effect on a synthetic US Census
dataset. For this part you will work with `pandas`, a very popular Python
data analysis toolset that many of you will probably use in other contexts.
The assignment does not assume prior knowledge of `pandas`.

In the second part, you will implement the attack from Lecture 20 that broke
many implementations of the Laplace mechanism in 2012 (it also breaks our
implementation from the first part). The root issue exploited by this attack
concerns how libraries generate random floating point numbers. Implementing
this attack is more technically involved than the first part of the
assignment, and requires a deep-dive into the representation of floating
point numbers and the implementation of `numpy.random`.

In the third part you will be asked to apply the theoretical analysis techniques for
differential privacy. This part will not invovle any code.

### What is Included

The following files are included in this assignment:

- `assignment8.html`/`assignment8.md`: This file.
- `part1.py`/`part2.py`: Starter code files.
- `adult_with_pii.csv`: Data file for Part 1.
- `mironov-2012.pdf`: Copy of the research paper used in Part 2.
- `assignment8-questions.txt`: Copy of the Gradescope questions. **This file is for your convenience only. This file is not used for submitting answers. Use Gradescope!**


### What and How to Submit

This assignment uses *both* Gradescope and Canvas.

**Upload to Canvas** the following files:

1. Files `part1.py` and `part2.py`, with the appropriate functions filled in.


**On Gradescope** answer the questions in Assignment 8. Note that you will upload your plot files here.

A submission checklist is also included in each problem below.

The point totals on Gradescope include the points for the code associated with each problem. So, for example, the 10 points in Part 1 - Problem 1 will be based on your Gradescope answer *and* your code in `part1.py`.

## Part 1: Introduction to Differential Privacy (35 points total)

### Setup

You'll need a working implementation of Python3.
For the rest of this part you will work with Python modules `pandas`,
`numpy`, and `matplotlib`. All of these can be installed via your favorite
method, like `pip`, and should be installed on department machines. You can
probably learn the latter two libraries `numpy` and `matplotlib` as you go,
since we will make very simple use of them. But it is worth taking a little while
to familiarize yourself with a tutorial on `pandas` if this is your first
time using it. Reasonable tutorials are
[here](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
and
[here](https://www.learndatasci.com/tutorials/python-pandas-tutorial-complete-introduction-for-beginners/).
Try to get some idea about what a dataframe is and the various ways to query
one. Also pay attention to merging dataframes.

The problems below will use the `adult` dataset, which is included with this
assignment as `adult_with_pii.csv`. That dataset is courtesy of [Joe
Near](http://www.uvm.edu/~jnear/) at the University of Vermont.

Make sure you can parse in the `csv` file using `read_csv`, and take a peek
at the data using the `Dataframe` methods `head()` and `info()`.

### Problem 1: De-identifying and Linking (7 points)

- In the `part1.py` file, fill in the function `deidentify`. Your function
  should take as input the dataframe from the `adult` dataset (or one with the
  same columns) produced by `read_csv` called on the `csv` file. It should
  return the same dataframe, but with the `'Name'` and `'SSN'` columns deleted.
  This models a typical faulty data release.

- Now fill in `pii` to also take in a dataframe from `adult`, but have it
  produce a dataframe with only columns `'Name'`, `'DOB'` `'SSN'` and `'Zip'`.
  This models the data that an attacker may have obtained.

- Now fill in the `link_attack` function. It should take as input the
  de-identified dataframe and the PII dataframe, and should return a dataframe
  consisting of all rows from the de-identified dataframe that could be uniquely
  linked, reattached to their PII. Proceed as in the classic Sweeney attack from
  lecture (but without sex). Your function should output a dataframe consisting
  only of the individuals that were uniquely recoverable. (Hint: This can be a
  few lines using the `pandas` method `merge`, followed by the removal of
  duplicates in the merged table. You may want to use `duplicated`.)

- Answer the questions under `Part 1 Problem 1` on Gradescope.

*Submission Checklist for Problem 1:*

- In `part1.py`, complete `deidentify`, `pii`, and `link_attack`.
- Answer the Gradescope questions under `Part 1 Problem 1`.


### Problem 2: k-Anonymity (12 points)

Fill in the function `is_k_anon`. It takes as input a dataframe `df`, a list
of column names `cols`, and an integer `k` assumed to be at least `1`. It
should output `True` or `False` depending on if the dataframe is
`k`-anonymous with respect to `cols`.

Your implementation should also run reasonably fast (a few seconds) on a
dataset the size of `adult`. Note that some naive implementations with nested
loops can be very slow in `pandas`; I recommend implementing this in a couple lines with `value_counts` from `pandas`, but you might find a slicker way
to do it.

You should test your implementation on (small) dataframes that are
`k`-anonymous but not `(k+1)`-anonymous for `k=1,2,3`.

Finally answer the questions under `Part 1 Problem 2` on Gradescope.

*Submission Checklist for Problem 2:*

- In `part1.py`, complete `is_k_anon`.
- Answer the Gradescope questions under `Part 1 Problem 2`.

### Problem 3: The Laplace Mechanism (8 points)

- Fill in the function `num_bachelors` that takes a dataframe as input and
returns the number of individuals with exactly a Bachelor's level of
education.

- Fill in the function `laplace_mech` that takes as input a float `query`
(representing the output of a query), a float `sensitivity`, and a float
`epsilon`. It should return the output of the Laplace mechanism with these
values. (Note: If you attended lecture, this is very easy. It's not a trick
question.)

- Fill in the function `make_plot_3` to compute *empirical probability
density functions* for the Laplace mechanism with different epsilons, and
then plot the results to visualize how changing epsilon effects the output
distribution. You function should fix `query=200.0`, `sensitivity=1`, and
then complete three runs with `epsilon` set to `0.5`, `1`, and `10`. In each
run, sample using `laplace_mech` 10,000 times. Finally use `matplotlib` to
plot the results (binned into groups) by calling `plt.hist(..., bins=50)`
three times (one for each run) and then `plt.show()`. You should get a plot
with three overlayed histograms which you can save as `problem3.png`.

- Answer the Gradescope questions under `Part 1 Problem 3`.

*Submission Checklist for Problem 3:*

- In `part1.py`, complete `num_bachelors`, `laplace_mech`, and `make_plot_3`.
- Answer the Gradescope questions under `Part 1 Problem 3`, including uploading your plot file `problem3.png`.

### Problem 4: The Laplace Mechanism on Nearby Queries (4 points)

Implement `make_plot_4`, which will generate a plot to see how different
queries changes the output distribution of the Laplace mechanism. Using
`laplace_mech` from the previous section, compute a differentially private
answer with `query=200.0`, `sensitivity=1`, and `epsilon=.05` by running it
10,000 times and plotting the results, again with 50 buckets. Repeat this
with `query` set to `201.0`, and plot similarly (on the same plot). Your
implementation should generate a single plot (i.e. one call to `plt.show()`),
which you should save as `problem4.png`. 

Afterwards, answer the questions under `Part 1 Problem 4` on Gradescope.

*Submission Checklist for Problem 4:*

- In `part1.py`, complete `make_plot_4`.
- Answer the Gradescope questions under `Part 1 Problem 4`, including uploading your plot file `problem4.png`.

### Problem 5: Error and the Laplace Mechanism (4 points)

Implement `make_plot_5` to produces another plot:
Using `laplace_mech` from the previous section, compute 10,000
differentially private answers with `query` hardcoded to the correct output of `num_bachelors` from Problem 3 and with `sensitivity` set correctly. For each
answer, compute the absolute error (which is always positive)
between the differentially private answer and the true answer, and plot
with `bins=20`.
Repeat this with `epsilon` set to 0.5, 1, and 10.  Overlay the 3
histograms (all with `bins=20`) from the three runs in on plot as before. 
Your implementation should show the plot, and you should also save it
as `problem5.png`

Afterwards, answer the questions under `Part 1 Problem 5` on Gradescope.


*Submission Checklist for Problem 5:*

- In `part1.py`, complete `make_plot_5`.
- Answer the Gradescope questions under `Part 1 Problem 5`, including uploading your plot file `problem5.png`.


## Part 2: Floating-Point Attack (50 points total)

### Background on the Attack

The included file `mironov12.pdf` describes an attack against implementations
of the Laplace mechanism that use tools like `np.random.laplace`. This is an
example of a nicely written research paper, and it doesn't require much more
than our lectures to be fully understood. (You should refer to the paper in
the course of working this part, but you can skip the analysis in Section 4.6
and the proof of Theorem 1 in Section 5.)

Here is a brief summary of the attack, which was described in lecture. The
attack shows that one can often distinguish
*with certainty* if a given float was output by either
`np.random.laplace(1)` or `1.0+numpy.random.laplace(1)`. That is, just by
looking at the bits of the float, you can often tell if the sample was
shifted by 1 or not! Section 4.5 of the paper (and also the lecture slides)
has a visualization of what this looks like for an attacker. The ability to
determine this information conclusively, even part of the time, is a bad
violation of the requirement for differential privacy (in this case, failing
to protect a query with result 0 or 1).

This may sound a bit contrived, but it is the seed of a damaging attack. For a possible scenario where the attack would apply, suppose we are reporting the number of people with a particular rare health issue. Given that it is rare, the number of people is very likely to be zero or one. If an adversary is targeting one individual who it suspects has the health issue (if anyone does), then this attack will result in complete breach of privacy, contrary to the goals of differential privacy, which should protect individuals even in extreme cases.

The important point here is that, while even a properly-implement DP system allows
adversaries to gain some knowledge of the likelihood that the targeted individual has the health issue, it should *never* allow them ever be sure. In other words, there should always be some measure of plausible deniability, and this attack shows that sometimes that won't hold.

While we're working only with zero versus one in this assignment, the attack works in distinguishing any `n` versus `n+1`. This attack lead to everyone being much more careful with implementations. A meta-lesson is: *Be very careful when using floating point numbers in security tools!*

### How the Attack Works

How does this attack work? First we need to examine how samplers for the
Laplace distribution are coded up. Refer to the implementation of
`my_laplace` in `part2.py`. This uses a standard technique also used in the
`numpy` version (which is written in C). The sampler first draws a sample
from `np.random.uniform`, which returns a float between 0 and 1. It then
takes the natural log of this number using `np.random.log`, and
multiplies the result by a random sign. Finally it scales the result.

There are two important features that cause the failure of this sampler:

1. First, the uniform sampler only returns certain floats between 0 and 1,
and not every possible representable float in that range. Let us call this
set of floats `U`. (See Table 1 on page 6 of the Mironov paper or my lecture slide.)

2. Second, the implementation of the log function also does not output every
possible float. Let us denote by `L` the set all floats that log would ever
output. (See the figures on page 6 of the Mironov paper.)

This suggests a general strategy for an attack. Given a scale `s` and a float
`y` which is either drawn from `my_laplace(s)` or from that
distribution plus `1.0`, the goal is to determine if it could have came
from `my_laplace(s)`. At a high level, it proceeds:

1. If `y > 0` set `y = -1*y`. (i.e. ensure `y` is negative)

2. Find *all* floats `x` such that `s*np.log(x) == y` where `s` is the scale.
Note that you're going to test for *equality of floats* here; you almost
never want to test this in any other circumstance, but here you do.

3. If any `x` is in `U`, output `True` (since `y` *could* be output by the sampler). Else output `False`.

It is possible that we settle for approximations of these tests for membership
in sets. The goal is after all an attack that will distinguish the types of
samples with some probability, so it will not work 100% of the time anyway.


### Your Task, Hints, and What to Submit

*Submission Checklist for Part 2:*

1. Implement the function `is_scaled_laplace_img` in `part2.py`. You may
implement helper functions above in the file. Further hints and a rubric are
provided below.

2. On Gradescope answer the questions under `Part 2`.


**Correctness Rubric.** Part of your grade will depend on the effectiveness of
your distinguishing function (the rest will come from your write-up).
To measure effectiveness, we'll use the `test()` function in `part2.py`.
In particular, we'll do the following:

1. We'll run your `is_scaled_laplace_img` on 1000 *unshifted* samples
from `my_laplace`, and let `x` be the number of times it returns `True`.

2. Next we'll run your `is_scaled_laplace_img` on 1000 *shifted* samples
from `my_laplace`, and let `y` be the number of times it returns `True`.

3. We'll compute `d=x-y`. If `d>450` you'll receive full credit for
correctness. Partial credit will be awarded, down to `d=100`, which
will receive half credit for correctness. In all cases we'll run your
code several times and take the highest difference, to remove the
element of luck if you're near the threshold.

The highest difference I could get was about 600 on average. 


### Hints: Floating Point Encodings

 The paper nicely describes how floats are encoded on a modern computer. Python uses 64 bit floats that follow this standard. At a few points in your code it might be helpful to have the bits of a float, either to print out or to
manipulate. To help, the file `part2.py` includes some utility functions for
converting a float to an ASCII string of 64 ones and zeros, and also to
convert such a string back to a float.

The comments above these functions describe the expected inputs and output. Here is an example: If we call

```
float_to_binary(0.25)
```
we get the result

```
'0011111111010000000000000000000000000000000000000000000000000000'
```
This is a *string* meant to be human readable and easily manipulated. That these bits follow the encoding from Section 5.2 (see also the
[Wikipedia](https://en.wikipedia.org/wiki/Double-precision_floating-point_format#IEEE_754_double-precision_binary_floating-point_format:_binary64)
for a [visualization](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/IEEE_754_Double_Floating_Point_Format.svg/2560px-IEEE_754_Double_Floating_Point_Format.svg.png) of this bit encoding). Parsing out
this string as in the diagram, we get

```
sign = 0
exponent = 01111111101
fraction = 0000000000000000000000000000000000000000000000000000
```
The "fraction" is often called the "mantissa". If one interprets `sign` and `exponent` as numbers in the standard binary encoding, the formula for the intended number is

```
(-1)^sign * 2^(exponent - 1023) * 1.fraction
```

The function `binary_to_float` takes a string of zeros and ones and converts it back to a floating point number. For example, running

```
binary_to_float('0011111111010000000000000000000000000000000000000000000000000000')
```
give the output `0.25` (a number, not a string).

The main purpose of `float_to_binary` and `binary_to_float` is that they together allow for precise manipulation of floating point numbers. For example, you can flip a bit of the mantissa by calling `float_to_binary`, changing the string, and then calling `binary_to_float`. That's very tricky to do if you're working with floating operations directly.

Feel free to change these utility functions if you want.

### Hints: Implementing the Attack

To find `x` such that `s*np.log(x) == y`, you can try using `np.exp`.
Mathematically, exponentiation should be the inverse of the natural log, but
this isn't so when dealing with floats. Instead, you can use `np.exp` to get
pretty close to such and `x`, and then try nearby numbers, say be brute force
trying all possible values for the several least significant bits of the
mantissa. Don't worry about doing this part with absolute correctness.
Something that works based on empirical observations can be good enough.

To test if a value `x` is in `U`, think about the binary representation of a
number fitting the condition given in Table 1. It might be possible to test this algebraically using the `%` operator. I preferred to use the utility function to extract the bits and test them directly by hand.
It might be helpful to take some samples from `np.random.uniform()` yourself,
convert them to binary, and print them for eyeballing what's going on.

## Part 3: Theory Problems (15 Points)

This part consists of three problems related to the theoretical analysis of differentially private systems.

### Problem 1 (2 Points)

Recall that randomized response instructs subjects to flip coins `C_a` and `C_b` and then:

1. If `C_a` is Heads, give their true answer.
2. If `C_a` is Tails, give a random answer as determined by `C_b`.

Suppose we change this process to only use one coin `C_a`

1. If `C_a` is Heads, give their true answer.
2. If `C_a` is Tails, reverse their answer (from "yes to "no", or vice versa).

Explain in a sentence or two why this modification is flawed.

### Problem 2 (5 Points)

Consider the following variant of randomized response from lecture: The subject is now given a fair ten-sided die `D_10` and coin `C_b` and instructed roll `D_10` and then:

1. If `D_10` shows a `1`, give their true answer.
2. Else give a random answer as determined by `C_b`.

For which `epsilon` is this variant `epsilon`-differentially-private? Justify your answer with a proof that follows the technique from Lecture 20. Your proof should be written in complete sentences, and explain each step. (The proof on the slides is abbreviated; Your proof should explain the elided steps.)

You do not need to appeal to formal probability theory in your proof. You can use a simple [tree diagram](https://www.mathsisfun.com/data/probability-tree-diagrams.html) to calculate the needed probabilities, and then just state them them in your proof. If you are uncertain, please ask for help in checking your thinking.

### Problem 3 (8 points)

This part considers queries that may be run on an imaginary dataset `D` that consists of data about the UChicago college. Assume that there between 6000 and 7500 students in any possible dataset. We define two datasets to be *neighboring* they differ by one student's data (in other words, one dataset is equal to the other with exactly one student removed). 

For each of the following functions, state the sensitivity of the function and a short justification for your answer. For some of these your answer will depend possibly on some features of the data; in those cases, explain how and why this is the case.

1. `f_1(D)` outputs the number of students enrolled in CS232 in Winter 23.
2. `f_2(D)` outputs the number of students enrolled in three or more classes in Winter 23.
3. `f_3(D)` outputs the sum of all class sizes in Winter 23 (so, if the university only had three classes, of sizes 12, 20, and 65 respective, then `f_3` would output `97`).
4. `f_4(D)` outputs the average GPA of all students in Winter 23. (Assume GPAs are between `0` and `4`).

*Submission Checklist for Part 3:* Please type your answers into Gradescope.

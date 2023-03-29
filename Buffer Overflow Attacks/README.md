# Assignment 2: Memory Bug Exploitation

In this assignment you will implement buffer-overflow attacks to hijack
victim programs, starting with a simple program similar to the one David
attacked in class.

These victim programs have been stripped down to minimal examples to
highlight the step where an unsafe memory operation can be exploited
to take control of a program. In practice, getting to this stage can
take many tedious days (or longer) by a team of analysts. And even when the
unsafe operations are found, they are frequently much more difficult to
exploit due to un-fun complicating factors.


## Get the Assignment Files onto your VM

For this assignment you will use the same virtual machine from Assignment 1 Part 2; doing so allows for a controlled environment (e.g. 32-bit addressing rather than 64-bit, countermeasures turned off, a clean environment, etc) and makes carrying out the attacks much easier.


Log into your VM as before. To download the assignment files, run the following command from your home directory:

```
wget https://people.cs.uchicago.edu/~davidcash/assignment2.tar
```
This program will download a file named `assignment2.tar` to the your home directory. Next, run

```
tar -xvf assignment2.tar
```
After this command, you should have a directory named `assignment2` in your home directory. The assignment files are in that directory.



## Your Tasks


The directory `assignment2/targets` contains the C source code of victim programs you'll attack. These have been compiled using the included `Makefile`, and the binaries have been copied to `/tmp`. You do not need to build them. The binaries in `/tmp` are owned by a user `victim`, and they have SUID permissions set, so a successful attack will give a shell running as `victim`. 


In `assignment2/sploits/` you will find skeleton files `sploit0.c`, ..., `sploit4.c`, along with `shellcode.h`. These files can be compiled with the makefile included in that directory. When run, the skeleton code will execute their respective target from `/tmp/`. The `args` array are the command line arguments passed to the target. You shouldn't modify `env`, except perhaps for `sploit4` (and even then there are other ways to finish that problem).

You will modify files `sploit0.c`, ..., `sploit4.c` so that, when compiled and run, each executes the appropriate target and obtains a shell. When you get a shell, a bare-bones prompt that is simply a `$` will appear. You can run the `whoami` command at the shell, celebrate your success, and then close it. **When you get a shell as `victim`, please just run `whoami` and log out of the shell! There is no secret information or anything fun to do as `victim`.**

For your convenience, `shellcode.h` contains the classic NULL-free shellcode that I used in class.

You may find it useful, especially at the very start, to try attacking the targets directly at the command line instead of via the `sploit` files. But ultimately you must implement your attacks in the `sploit` files because grading will assume this format. (I find this easier, since working in C makes it easier to feed binary garbage to the program as an argument.)

Note that while debugging your attacks, you will need to run `gdb sploitx`, and then set `gdb` to follow the child `target` process by typing `set follow-fork-mode child` into `gdb`. Note that when you set a breakpoint in `main`, `gdb` will break at both the `main` in the sploit *and* the `main` in the target. Once you're in the target, you can set further breakpoints. (Another quality-of-life recommendation: Put the 

```
set follow-fork-mode child
```
command in a file `.gdbinit` in your home directory, and it will run every time you start `gdb`. You can put other startup commands there, and also alias your favorite commands too.

### Problem 0

I have solved Problem 0 for you in a video to be uploaded soon. This video begins with installing the assignment, and involves some debugging as I work through the problem from scratch. Even if you understand buffer overflows, it may help orient you with the assignment infrastructure and gdb.

### Problem 4

The last problem is built to have a non-executable stack. You will need to implement a return-to-libc attack for this sploit.

## Resources on Buffer Overflows

The following assigned readings are especially relevant to this assignment:

1. [Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html#article)

2. [Basic Integer Overflows](http://phrack.org/issues/60/10.html#article)

The textbook also has good coverage of integer overflow bugs. If you can get your hands on it (possibly electronically), [Hacking: The Art of Exploitation](https://nostarch.com/hacking2.htm) is an excellent introduction with lots of examples.

## What and How to Submit

You will submit everything to Gradescope [here](https://www.gradescope.com/courses/481333/assignments/2572833). Specifically,

1. For each sploit, in the appropriate blank, respond to the following: (1) Describe the vulnerability you found. (2) Describe how your exploit works.

2. In the appropriate question, upload a file `sploits.tar` created as follows. In the `sploits` directory run

```
tar -cvf sploits.tar sploit0.c sploit1.c sploit2.c sploit3.c sploit4.c
```
When this command completes, you should find a file `sploits.tar` in the directory. Transfer this file off of your VM to submit. One way to do this to run `scp` **on your local machine** via

```
scp CNETID@cs232-XX.c.cs.uchicago.edu:~/sploits.tar .
```
Now this assumes that `sploits.tar` is in your home directory on your VM; You can either put it there or change the path in the command. Also note that this command will overwrite a local file named `sploits.tar` if there is one.

We recommend checking that your `sploits.tar` has the exactly the files you intend to submit before uploading it. After you transfer it from your VM, you can open it (by doubleclicking in most OSes) and look at the files that result when it expands. You can also run

```
tar -xvf sploits.tar
```
to expand the file.

## Some Frequently-Asked Questions

> I'm trying to place an address in memory, but the bytes are in the reverse order from my payload. How do I fix this?

The simple answer is to reverse the order of the bytes. This is necessary because x86 is "[little endian](https://en.wikipedia.org/wiki/Endianness)".


> Can I create my payloads in Python or some other language?

You should feel free to do so, but your solution should ultimately be contained in the sploit C files.


> This is fun. Can you recommend some more problems?

[Mirocorruption.com](microcorruptoin.com) is a fun CTF with these sorts of vulnerabilities, simulated on a weird 16-bit architecture.

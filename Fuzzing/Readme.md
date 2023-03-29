# Assignment 5, Part 1: Fuzzing

Assignment 5 is divided into two parts. This is the first part, on fuzzing, and it is worth 50 points. The second part is about certificate measurements and is also worth 50 points. Together they are worth as much as one assignment.

In the tasks below you'll get to use [AFL](https://lcamtuf.coredump.cx/afl/), an industrial-strength fuzzing tool that was demo'ed in class, to find bugs in real-world applications. This will not require writing much code. Instead, you'll experience scanning a new codebase, modifying its build scripts, and writing small driver code to set it up for fuzzing.

## Tech Set-Up

For this project you will need to run AFL yourself. There are two options for how to do this:

### Option #1: Install AFL on Your Computer

If you have a Windows, Linux, or non-M1 Mac, please read installation instructions for your machine and attempt to install AFL there:

- [Windows/WSL](https://github.com/status-im/nim-testutils/blob/master/testutils/fuzzing/fuzzing_on_windows.md) (In these instructions, a few of the commands left the `$>` prompt in, while others didn't; Make sure you aren't copying the prompt when running those commands.)
- [Non-M1 MacOS with `brew`](https://formulae.brew.sh/formula/afl-fuzz) (`brew` is a package management system for MacOS that is very easy to use and handy, especially for programming tools). You will need to install [brew](https://brew.sh/) first.
- [Non-M1 MacOS without `brew`](https://github.com/google/AFL) You can also just clone the repo and follow [the installation instructions](https://github.com/google/AFL/blob/master/docs/INSTALL). You will need to install [Xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12), which is Apple's official set of developer tools. It's rather large, but you might want it anyway if you plan to play with app development.
- [Linux](https://github.com/status-im/nim-testutils/blob/master/testutils/fuzzing/readme.md#Install-afl): AFL should be available through your package management system.

Finally, AFL runs faster if we turn off OS features for handling crashed programs.

**On Linux or WSL**, we need to turn off coredumps. To do this, run the following three commands:

```
sudo su
```
(enter your password)

```
echo core > /proc/sys/kernel/core_pattern
```
```
exit
```

**On MacOS**, we need to disable the OS from phoning home to Apple every time a program crashes. The first time you run AFL, it will complain and give you three commands to run.


**If you have an M1 Mac, or otherwise encounter extensive difficulties that you cannot resolve, then go to Option 2. Please attempt to resolve them by reading error messages, considering them, and then asking for help at office hours or on Campuswire if you are stuck.**

### Option #2: Use a Department-Hosted VM


The second option is to use the same VM you used on Assignments 1-3. Your public key should still be installed there.

A few instructions will be different for users of the these VMs. Please be careful to follow them - They are designed to vastly reduce the load on our servers.

***Please attempt Option #1, unless you have an M1 Mac. This will conserve our server load as well as the sanity of the CS department's techstaff.***

**Etiquette and Tips for the Department VM:** The department VM is running on shared infrastructure. **Please do not leave your fuzzer running for a long time.** We may kill your process if it has been running for a hours and we get complaints from other students.

Please also follow the instructions for using the ramdisk when setting up your test inputs. This will save a lot of resources (see the discussion later in the write-up).

If at all possible, **do this assignment early**. This will reduce the peak load.

When you're on the VM, you can run the command

```
w
```
to see who else is logged in, and what programs they are running. You can also run

```
top
```
to see which processes are consuming the most resources. If you notice other people are already fuzzing, you can try fuzzing but consider checking back in later. If you notice someone has been hogging the VM for a long time, you can let us know on Campuswire and we will address it.

Finally, if something doesn't look right or is excruciatingly slow, please ask on Campuswire.

## Fuzzing Exercise 1: A JSON Parser (20 points)

This first exercise is worth half the assignment. Please read it all the way through before proceeding, paying special attention to the deliverables so that you remember to save them as you go.

### Exercise 1: Download and Compile a JSON Parser Library

In this part, we'll install a JSON library, compile it with ASAN instrumentation, and fuzz it to find some bugs. This particular library is a perfect application for fuzzing: It parses [JSON](https://en.wikipedia.org/wiki/JSON) files, which are complicated, and we can easily generate them. It also has a simple interface that we can drive and check for crashes.


Run the following from your home directory:

```
git clone https://github.com/VernonGrant/jsn.c.git
```
This will download the repo's code. (Note that this is some unsuspecting person's repo; Please don't bother them. I chose this repo arbitrarily from amongst thousands of reasonable targets.)

Now run

```
cd jsn.c
```

We need to compile this code. If we just build it by running the usual command `make`, then it won't be instrumented with ASAN, and AFL won't be able to detect crashes. To properly instrument it, we
need to instruct `make` to use the special AFL compiler `afl-clang`. In order to do this, we need to edit the file `makefile` in this directory. (This file is like a recipe for the program `make` that tells it what to run, and with what options.)

More specifically, open up `makefile` in your favorite editor. The first line should be

```
GCC=gcc -ggdb -Wall
```
Change this line to

```
GCC=afl-clang -ggdb -Wall
```
Don't edit any other lines. If you accidentally change something else, `make` will complain; it is **very** picky about formats. (For example, `make` completely breaks if you use spaces instead of actual tab characters on some lines!)

Now run

```
make
```

You should see some output telling you that the AFL compiler instrumented the code. At this point, we only have a library file named `jsn.o`

### Exercise 1: Create a Driver Binary to Fuzz

We need to create an executable program that uses the `jsn.o` library in a simple way amendable to fuzzing. Create a file called `test.c` in this directory, and put the following program in it:

```
#include "jsn.h"

int main(int argc, char *argv[]) {

    jsn_handle jh = jsn_from_file(argv[1]);
    jsn_free(jh);

    return 0;
}
```
Take a moment to understand what we're doing here; it's a very short program.

Now compile this test program into an object file `test.o`:

```
afl-clang -o test.o -c test.c
```

And finally produce an executable program `test` by linking `test.o` with `jsn.o` by running this command:

```
afl-clang -o test jsn.o test.o
```
Now you should able to run `./test FILENAME` to check if it successfully parses a file named `FILENAME`. For example, you can run

```
./test test.c
```
and it should complain that `test.c` is not a valid JSON file.

### Exercise 1: Create input and output directories

This part assumes you are still in the directory `jsn.c`.

We need to set up directories for input and output files for AFL. 
**If you are running AFL on your own machine,** these can be in
the current directory. Just run

```
mkdir inputs
```
and

```
mkdir outputs
```

**If you are on a department VM,** we have created a special shared directory for you to use. Instead of putting `inputs` and `outputs` in the `jsn.c` directory, put them `/mnt/ramdisk`. Since the machine is shared, you will need to change the name of your file. I suggest including your CNetID. For example, David could create these directories as

```
mkdir /mnt/ramdisk/davidcash
mkdir /mnt/ramdisk/davidcash/inputs
mkdir /mnt/ramdisk/davidcash/outputs
```
Once you've created these, **you will need to use these directories below in place of `inputs` and `outputs` everywhere**. It's easiest if you always use the full path to these directories.

Here is why we needed to do this: The `ramdisk` directory is actually not stored on disk: it's a simulated disk that sits in memory. Since AFL creates millions of files, it will save a lot of wear and tear on our infrastructure to just have that happen in memory. The downside is that if you (or your VM buddies) manages to explode the VM and force us to reboot it, then the data here will be lost. You should move crucial files (like the crashes generated later) out of this directory and into your home directory for safekeeping.

Creating a ramdisk on your machine is also a good idea if you're curious and want fuzzing to run faster. A simple Google search will reveal instructions for your OS, and after you create it, you can simply put your inputs and outputs there.

### Exercise 1: Collect some test cases


Now let's put a bunch of test input files into the directory `inputs` by doing the following:

1. Go grab [this file](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/JSON.Fuzzing.txt) from GitHub. It contains a bunch of JSON examples - one per line. Save this to your current directory. (If you are on the department VM, you will need to scp this file there.)
2. Write a quick Python script that reads in the lines of the file (use `readlines()`) and writes each line to a different file in the `inputs` directory. You can just number these files `1.json`, `2.json`, etc. The names don't matter.
3. Now run your script to produce the input files. You should get about 100 files.

Note: Check that script is outputting files into the `inputs` directory. You might run it on a one or two-line file first as a test.

At this point, you should have an `inputs` directory with many test files, along with an empty `outputs` directory.


### Exercise 1: Fuzz the JSON Parser

Time to fuzz! This part will ask you to take a screenshot of AFL running, so please look up how to do that before you get started.

In the `jsn.c` directory, run

```
afl-fuzz -i inputs -o outputs -- ./test @@
```
to kick off the fuzzing. (If you're on the department VM, remember to use the correct paths to the actual input and output directories.) Please take a second to understand the syntax of this command. The `-i` and `-o` options specify input and output directories. The `--` part delineates regular options from the remaining options, which will tell AFL which program to run (`./test` in our case) and how to feed it file arguments (the `@@` part says to just put the names in here).

At this point, AFL may complain about various issues. A common one is the coredump or crash reporting setting. It kindly gives you commands to run (possibly using `sudo`). Please take a moment to read the error messages and try to resolve them before asking for help. You don't have root on the department VMs anymore, so let us know if we overlooked anything that needs `sudo`-ing.

On my computer (and the department VMs), I found one crash nearly instantly, and then several more crashes a few seconds later. Try running it until you get at least two crashes. **At this point, take a screenshot of AFL before stopping it.**

### Exercise 1: Check out the Crash Files

Once you have a couple of crashes, you can kill AFL by hitting `ctrl-C`. You should find the crash files in `outputs/crashes`. They have long names like `id:000000,sig:11,src:000000,op:havoc,rep:8`. You can test that the program actually fails on the files by running (from the `jsn.c` directory)

```
./test outputs/crashes/id:000000,sig:11,src:000000,op:havoc,rep:8
```
(replace the long filename with whatever `id` file is in that directory). You should get a segfault - maybe the first time you've ever been happy to see one! You can take a look at the files by using `cat` or an editor - it turns out that this parser has some very basic bugs.

### Submitting Exercise 1

One Gradescope, respond to the appropriate prompts for Exercise 1. You will need the following files:

1. Your Python script for creating the test input files.
2. Your screenshot of AFL's dashboard showing at least two crashes.
3. Your two crash files.

## Fuzzing Exercise 2: Find and Fuzz another Project (30 points)

In this exercise you will repeat the above process of finding software that is likely to have bugs and using AFL to fuzz it. You will essentially be walking through the first exercise, but responsible for figuring out how to build and drive the software yourself, and then for finding test inputs.

As with the previous exercise, please read this part through before starting so that you know what deliverables to hold onto.

### Exercise 2: Find a project to Fuzz

Use the GitHub search feature to find a repo that looks like a reasonable target for fuzzing. Please find something other than a JSON parser. I recommend searching for something related to parsing files, then filtering the language to C. Then go *deep* into the search results, and look at libraries with few or no stars. You probably want a repo that was done as a hobby project. Check that the project is not a complete joke, however (like something half-finished). Avoid repos that indicate the project has already been fuzzed.

Once you identify a candidate, check that it has a `Makefile` or some other simple build instructions that use the `gcc` or `clang` compilers (which indicates that switching to the AFL wrapper will work).

Next, check that the software has a simple interface appropriate for testing. In Exercise 1, this was the `jsn_from_file()` function that we could call from the compiled binary. You can find this from usage instructions in the repo, or perhaps from some included drive code for (non-fuzz) testing. If there are several possible choices, you could choose one that appears to be doing the heavy lifting (i.e. the main parsing job).

You may need to look through a few repos before you find one that has the right combination of properties. For what it's worth, David produced Exercise 1 above on the first try and only had to look at a few repos to find it.

This should without saying, but you should not own this repo, and you definitely shouldn't create the repo yourself for the purpose of this assignment.

At this point, you should have a good candidate; record your reasoning about how you arrived at this candidate for later submission to Gradescope.

Please don't use the same repo as your friends; You should do this independently.

### Exercise 2: Build your chosen project and write driver code

Now `clone` the repo and check that you can compile it without modification. If it appears not to compile for hard-to-fix reasons, you can pick another repo.

Now modify the build process to use `afl-clang` instead of `gcc` or `clang`. This will involve either editing a `Makefile` or modifying some provided instructions. You might need to run `make clean` to delete the previously-built binaries from before you modified the `Makefile`.

At this point, the project may give you binary that is appropriate for fuzzing directly (for example, it produces a program that takes a file name as an argument and attempts to parse it). In that case, you can go ahead and build that binary with the AFL instrumentation.

On the other hand, it is possible that the project only produces a library. Check that you can compile the project's library with AFL instrumentation. After that, it is time to write a tiny driver program like we did in Exercise 1. David did this in Exercise 1 by looking at some included test code and stripping it down to a few minimal lines. Once you have that code written, make sure you can compile it with `afl-clang`.

At this point you are ready to start fuzzing. Remember to record the major steps you took in this part for later submission, namely:

- What you modified to get the project to build with AFL instrumentation, and the commands you ran to build it.
- What you did to get a fuzz-able binary; Either taking included driver code or writing your own.
- The commands required to compile your driver code.

### Exercise 2: Find test cases and fuzz

The rest of this exercise follows Exercise 1. You need to collect test files, put them in the appropriate directories, and run AFL. **It is okay to Google for test inputs appropriate for fuzzing the type of program you're testing.** For example, in Exercise 1 I googled to find that list of fuzzer inputs. Input files should be small typically (AFL will complain if you give it big inputs, and also we don't have much disk space on the department VMs.)

After you collected some reasonable test inputs, set everything up like before and fuzz away. (You probably want to use different input/output directories; AFL complains if you try to reuse them.)

**If you get no crashes:** At this point you should, ideally, get some crashes. It is possible that you won't. Either you chose a rock-solid program, the setting just isn't good for fuzzing, or something is wrong with your setup. If you cannot get crashes after 10 minutes, but you appear to exploring new paths and making progress, please private post to Campuswire with the details of your work so far. We will take a look and either approve a submission without a crash or, in the case we spot a misstep in the instructions, ask you to start over (or recommend fixes to your work).

**In order to get approval for a submission without a crash, you must post this request by Tuesday, Feb 7 at 11:59pm.** Posts after that point will not be reviewed; You should just pick a different repo that you can crash.

**If you get at least one crash:** Take a look and double-check that you're not just crashing your driver code (outside of the test library) due to a silly error. If it looks good, then you're done. Congrats on crashing someone's program!

Now record the following for submission on Gradescope:

- How you find test inputs, and any code you wrote to process them.
- Your actual test inputs.
- The command you used to run AFL.
- A screenshot of AFL showing that it found at least one crash.
- Your crash files.


### Submitting Exercise 2

Now respond to the prompts for Exercise 2 on Gradescope. You will need the information and/or files identified in the steps in this exercise.


<!-- 

# STOP HERE - NOT EDITED BELOW

## Fuzzing Exercise 2: `guff`

Next we'll throw AFL at another tool: [`guff`](https://github.com/silentbicycle/guff).
This program reads in points and plots them using ASCII characters.

To get the code,
go back to your home directory and run
```
git clone https://github.com/silentbicycle/guff
```
```
cd guff
```
```
make guff
```
to download and build the plotting tool `guff`.

**Edited to add:** If you got some errors, it may be due to a bug in the Makefile for `guff`. To address them, try copying the included Makefile over the one in the `guff/`. (See also [post \#399](https://campuswire.com/c/GA5F4793A/feed/399) on Campuswire.)

Now, recompile `guff` to be compatible with AFL, by setting the `CC`
and `CXX` variables as before. Then, create a few seeds for AFL to use while
fuzzing guff (maybe look up some of the syntax for guff files for inspiration).
Place these seeds into `/mnt/ramdisk/CNETID_inputs/` as before and begin running
AFL just like with `test_json` in the previous problem. (Note: it is probably
a good idea to delete the inputs and outputs from the previous problem,
so AFL doesn't use json-parser tests as seeds and you don't get the crashes
mixed up.)

Make sure to save one of the seeds you came up with and one of your
crash files for submission.

After fuzzing guff with seeds, try running guff with just a file containing
"hello" (which is intuitively a bad seed). Note how the path exploration
compares between the two seeds.

## Etiquette and Tips for the Department VM

The department VM has been deployed for the first time this quarter. It definitely cannot support 20+ people fuzzing at the same time. **Please do not leave your fuzzer running for a long time.**

If at all possible, **do this assignment early**. If everyone waits until the last day, there may be conflicts. We can ask techstaff for more VMs, but I'd prefer not to bother them if possible.

When you're on the VM, you can run the command
```
w
```
to see who else is logged in, and what programs they are running. You can also run
```
top
```
to see which processes are consuming the most resources. If you notice other people are already fuzzing, you should check back in later. If you notice someone has been hogging the VM for a long time, you can let us know on Campuswire and we will address it.

Finally, we expect issues to arise with this VM (we just don't know what the issues are). If something doesn't look right or is excruciatingly slow, please ask on Campuswire.


## Questions (to submit on Gradescope)

1. Give two reasons that would lead AFL to not trigger any crashes in a program after 10 minutes, even if the code had bugs. If you faced this problem, what would you do to address one of them?

2. For `json-parser`, approximately how long did you run AFL for? How many unique crashes and total paths did it explore?

3. Same question as the previous one, but for `guff` when fuzzed with one your seeds.

4. Answer the previous question, but for `guff` when fuzzed with seed "hello". How does this compare to the guff with a (presumably higher quality) seed?

5. Why did we need to recompile `json-parser` and `guff` with `AFL_USE_ASAN=1`? And what does `CC=afl-gcc` do? (Feel free to use Google or the AFL documentation here, and cite your sources.)

6. [Optional bonus question] Now select one of the crashes you found, and run the appropriate program (`json-parser` or `guff`) in gdb and attempt to determine what the bug is in the source code. More detailed answers will receive more bonus points!


## What and How to Submit

1. On Gradescope, please answer Questions 1-5, and optionally 6.

2. On Canvas, submit a files `json-crash`, `guff-crash`, and `guff-seed` respectively. The first two should be crash files, and the third should be your seed for `guff`.

You're done! Time for Part 2.



## Configure a Ramdisk (Local VMs Only)

AFL runs faster if does not have to touch the disk. To help it, we'll keep its input and output files in a "ramdisk", which is a "virtual" disk stored in memory.

If you are on the department VM, I have already created a ramdisk.

The first command should output a group ID, which is used
for the second command. You can also enter any password for the ubuntu user you'd like. (Note: If you shutdown your VM, you may have to rerun these commands to recreate the ramdisk)
```
sudo addgroup ubuntu
```
This command should output the group ID (GID) of the group you just created. Take note of this number and use it in the next command: 

```
sudo adduser --gid GID_FROM_PREVIOUS_COMMAND ubuntu
```
Now run the following:

```
sudo mkdir /mnt/ramdisk
```

```
sudo chown ubuntu:ubuntu /mnt/ramdisk
```

```
sudo mount -t tmpfs -o size=256M tmpfs /mnt/ramdisk
```
Now the directory `/mnt/ramdisk` will behave like a super-fast disk.

-->



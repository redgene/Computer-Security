Assignment 3: Password Cracking (100 points)

The Broad Setting of this Assignment

This assignment explores a few different aspects of the password and authentication ecosystems. In particular, you will learn a little bit about how passwords look when they are stored in a UNIX system and gain experience cracking passwords using existing password-cracking software (albeit in configurations you will have to choose).

In this assignment, the "flags" you will be aiming to capture are passwords for different users.

Before getting to the problems, we discuss the rules for this assignment and how you can access the assignment infrastructure for your attacks.

Rules

As with all assignments, follow the course policy and cite any sources you use. You may Google liberally to learn how to navigate Linux, program in Python, and learn how to use Hashcat. Again, per the course policy, you **must** note in your writeup the sources you referenced. Please note any you found particularly helpful since we might include them in future versions of this writeup.

Assignment Tech Set-Up and Overview

This assignment begins (Problem 1) on your VM and continues (Problems 2-3) on either your own machine or the CSIL machines.

You don't have to write much code for this assignment, but rather most of the effort will be in configuring Hashcat to run smart attacks. As in past assignments, you may implement your code in whatever programming language you choose. That said, we recommend Python, for which we can provide the most support. You will be submitting your code (when applicable) alongside descriptions of what you did, as detailed in each task below.

Problem 1: Online Attack to Steal the Shadow File (30 points)

On your class VM, you have an account with your CNetID as the username. This is a user with intentionally limited access to the system (i.e., not a superuser). However, you are suddenly no longer alone on this machine (even beyond any other students with whom you are sharing the VM). There are hundreds of other users on the system, 400 of which are assigned to you. You will worry about them in Problem 3. For now, your goal in Problem 1 is just to steal the file containing the password hashes of all other users on the system.

There is a file /etc/passwd that anyone (even without superuser privileges) can read, but this is not the file you want. You actually want /etc/shadow. Why? See [this Wikipedia articleLinks to an external site.](https://en.wikipedia.org/wiki/Passwd). The problem is that if you try to access this file, access will be denied. However, if you carefully peruse /etc/passwd, you might notice another user on the system -- kingcash -- who it turns out has sudo access to the system. This knowledge about kingcash is useful because, if you could log in as kingcash, you could access (and make a copy of) the shadow file.

Do this. Switch to the user kingcash and exfiltrate the shadow file (see below for a very important note about what it means to exfiltrate that file). As David mentioned during the first week of class, you can switch to a different user from the command line with the su command (run man su to read about it). There's a slight problem, though. Running su kingcash asks your for that user's password, and you don't know what password they used. However, because kingcash has let their power go to their head and developed false delusions of security, they have chosen a fairly weak password.

Thus, you will launch an online guessing attack against that user's password. We've provided some support to facilitate this. First of all, we've provided the leaked passwords from [RockYou](https://canvas.uchicago.edu/courses/47779/files/8785084/download), which is the same file we examined in class. You will want to write code (in any language) to take this file and generate an ordered list of password guesses, from most probable to least probable, based on how often a password appeared in RockYou.

Note that kingcash has chosen a password that is easy to guess, but not completely trivial. Thus, you'll want to automate this attack. To help, we've done two things. First, we've created a user called bargainbinblase on your VM who has the password badpassword so that you can see an example of using su to switch users; type exit to return to your command prompt. Second, we've provided a [starter Python file](https://canvas.uchicago.edu/courses/47779/files/8785081/download) that shows an example of using the Python pexpect library ([full official documentationLinks to an external site.](https://pexpect.readthedocs.io/en/stable/api/pexpect.html) and [more helpful short examplesLinks to an external site.](https://www.geeksforgeeks.org/how-to-use-python-pexpect-to-automate-linux-commands/)). The pexpect library lets you script automated interaction with interactive command prompts. The example Python file we provided shows what happens when you provide the right password for bargainbinblase; try changing the password that is sent to see the failure mode.

While you're welcome to code in any language you want that has its own expect-style functionality, we've already installed the necessary language support for Python on your VM and given that example code, so we strongly recommend you use Python to automate your attack.

Once you learn kingcash's password, you are able to exfiltrate the aforementioned shadow file. **DO NOT MOVE THE SHADOW FILE.** You can, and should, make a copy of this file. For instance, while you are logged in as kingcash and have sudo permissions, you could make a copy of the shadow file in your home directory, set the permissions such that only you can read it (chmod 700), and change the owner (with chown) of the copy in your home directory to yourself. However, **do not move /etc/shadow, and do not change the permissions or owner of /etc/shadow** because **that will make it impossible for anyone (you, us, you classmates) to log into the VM**. As might be implied by these bold warnings, this happened in a past year and caused lots of frustration for all involved. Once you own the copy of the shadow file in your home directory, you can use scp to copy it to your personal machine. Note that you can't immediately use scp or ssh as the user kingcash even though you know their password. That's because we've disabled password authentication over ssh for all VMs to prevent actual attacks by people not in this class. This is why we suggest making a copy, changing the owner to yourself, and then running scp from your own machine.

What to submit for this part

Submit a code file <YOUR CNETID>-problem1-rockyou.py (or substitute an appropriate extension for the language you used) that includes any code you wrote to pre-process the RockYou leak. **Do not submit either the RockYou leak or the output of your post-processing!**

Submit a code file <YOUR CNETID>-problem1-automation.py (or substitute an appropriate extension for the language you used) that includes any code you wrote to automate the password guessing attack on kingcash.

Submit the shadow file you exfiltrated.

In your shared write-up file, <YOUR CNETID>-writeup.pdf, briefly describe your approach to solving this problem and include kingcash's password in bold text.

Problem 2: Hashcat Setup (0 points, but needed for Problem 3)

For Problem 3, you'll be using the [Hashcat password cracking softwareLinks to an external site.](https://hashcat.net/hashcat/), which is an open-source tool. You have a few options for where you will run Hashcat:

**Option 1 is that you can install Hashcat on your own machine.** Installing Hashcat on your computer can require installing additional drivers and is fraught with opportunities for technical difficulties. Since Hashcat can be run in CSIL, we will not be providing much support in office hours or over Campuswire for debugging driver issues when installing hashcat on personal computers. You can download the [HashcatLinks to an external site.](https://hashcat.net/hashcat/) binaries, which support Linux, OS X, and Windows. Hashcat works much faster on a GPU, but getting the right GPU drivers installed can sometimes be very frustrating. It also works on CPUs, though much slower (but fast enough for this assignment).

**Option 2 is to go in person to CSIL in Crerar and use the pre-installed Hashcat on the Linux machines**. Cosmos from CSIL and Cody from the CS Department Techstaff (thanks to both!!) helped us out by getting Hashcat installed on the Linux machines in CSIL. Hashcat has been pre-installed in /usr/local/bin/hashcat on those machines, whic hwas added to the path. That means you can be in any directory and call:

**hashcat**

There are some sample hashes and word lists in /usr/local/hashcat that can be helpful.

**Option 3 is to go in person to CSIL in Crerar and get Hashcat up and running on the Macs**. While Hashcat has been pre-installed onto the Mac images in CSIL (thanks again to Cosmos and team), there have been some errors with temp directories that haven't been fully worked out as of assignment release. That said, you can clone the Hashcat repo and run it on any of the Macs running Big Sur.

On the CSIL Mac computers, we will be installing Hashcat from Github:

1. run **git clone https://github.com/hashcat/hashcat.git**
1. **cd** into the directory and run **make**

You will not be able to run *make install*, and that is totally fine! The important thing to remember if you are running Hashcat on the CSIL computers is that you need to run hashcat from inside the folder that you cloned, and you will have to run it as:

**./hashcat (followed by all of the flags and other info specified by the Hashcat executable)**

If you run it without "./" you will get an error, probably saying that the drivers are missing.

Problem 3: Password Cracking in an Offline Attack (70 points: 50 points for the cracks, 20 points for the explanation)

Ok, you now have the */etc/shadow* file. You will notice inside the file that there are around 400 users with usernames that start with *your* CNetID followed by an underscore. We will refer to these 400 usernames as the users assigned to you. Your first step for this problem is to extract only the lines corresponding to the users assigned to you from the shadow file; there are a handful of accounts made by the system for various purposes.

Unfortunately, this shadow contains hashes, yet you want (plaintext) passwords. Thus, you'll need to crack the passwords!

When you get a set of hashes, the first step is to figure out what hash function was used. Typically, you would use an online version of the [Hashtag scriptLinks to an external site.](http://www.onlinehashcrack.com/hash-identification.php) to identify possibilities. For instance, try *5f4dcc3b5aa765d61d8327deb882cf99*, which is "password" hashed with MD5. Once you know which (or which set of) hashes are possible, you will need to know the numerical hash function parameter (the -m parameter) for Hashcat from [their listLinks to an external site.](https://hashcat.net/wiki/doku.php?id=example_hashes). In this case, though, you could also learn how the hashes are stored by simply examining the shadow file; see [this tutorialLinks to an external site.](https://www.cyberciti.biz/faq/understanding-etcshadow-file/). Before you try to crack any hashes, you will want to extract just the information that you want to pass into hashcat (be *very carful* about determining the delimiter and think about what blase has told you about the best practices for storing passwords) and feed that info to your cracking software. The examples below assume you saved this file as *hashes.txt*.

You can run Hashcat by going to a command prompt, navigating to the directory where the Hashcat files are (assuming that directory hasn't been already added to the system path), and calling the appropriate binary. For example, on Ubuntu, I call *./hashcat64.bin*, but see above for how to call Hashcat on CSIL machines.

This won't do anything, though. You need to point Hashcat towards the file of hashes you want to crack (giving it the full path if it's not in the same directory as your Hashcat executable). You must also specify an attack mode. Your successful cracks will appear in the *hashcat.pot* file in the same directory as Hashcat, though you can (and we recommend that you) change the output file using the -o option to specify where your successful guesses go.

Here are some sample attack modes, but be sure to replace ./hashcat64.bin with whatever binary is appropriate for your environment (see above), and also be sure to set the right flag for the hash function used, as well as the file containing hashes :

1. **./hashcat64.bin hashes.txt -m 100 -a 3 ?l?l?l?l?l?l?l** will try to crack hashes in hashes.txt that are hashed with SHA1 (-m 100) using the selective brute-force (mask) mode (-a 3) of Hashcat, trying all 7-character strings of only lowercase letters.
1. **./hashcat64.bin hashes.txt -m 100 -a 0 pw.txt** will try to crack hashes in hashes.txt that are hashed with SHA1 (-m 100) using the wordlist mode (-a 0) of Hashcat, drawing its guesses from the file pw.txt (which you would have to provide).
1. **./hashcat64.bin hashes.txt -m 100 -a 0 -r ./rules/best64.rule pw.txt** will try to crack hashes in hashes.txt that are hashed with SHA1 (-m 100) using the wordlist mode (-a 0) of Hashcat, drawing its initial words from pw.txt, and also mangling those entries with the Best64 mangling rules.

Recall that you'll need to edit the sample commands above to reflect the proper binary for your operating system, specify the mode (-m) that actually applies for the hashes you have, provide valid paths to the rulelist (if applicable) and wordlist (if applicable) you want to run, and so on.

Feel free to look around on the internet for other sources of passwords or rules. Remember that you must document any you find.

You do not have to guess all passwords to receive full credit! **If you successfully guess the passwords for 150 of the 400 users assigned to you, and your write-up is sufficiently descriptive, you can receive full credit for this section.** If you crack fewer than 150, you will receive a proportional number of points. Note that some of the attacks you configure might run for a while (but, depending on how you configure them, you might end up configuring an attack **that would run for years**, so think carefully about what you're doing). You'll probably want to leave some of the attacks running for a bit, so **start early**.

If you find as much joy in cracking passwords as we do, try to crack as many as you can. We'll figure out some reward (snacks, etc.) for the people who crack the most.

To answer some other questions that you might have:

**How can I tell that it is working?** We suggest using the "--status" flag to have your screen automatically update the status screen

**How do I make hashcat run faster?** The -O will "Enable optimized kernels." You can also change the -w flag. Finally in some cases the -D can be used to speed things up. (Note: these optimizations are not substitutes for thinking through your attacks)

What to submit for this part

You do not need to submit any code for this problem.

You must submit the passwords you crack in one of two formats. If you used Hashcat, you can submit the .pot file that Hashcat outputs to store successful cracks as *CNET*-problem3.pot. If you don't use Hashcat (or if you really want to reformat the output for whatever strange reason), you may instead submit a file *CNET*-problem3.txt that includes the usernames and corresponding passwords you successfully guessed. Each line of this file should contain a username, followed by a **tab character** (\t), followed by the plaintext password that was a successful guess. If you choose the .txt option, do not include the usernames of users whose passwords you did not successfully guess.

In your shared write-up file, *CNET*-writeup.pdf, describe your approach to solving this problem. In particular, be sure to note what machine you used, all configurations of Hashcat you tried in order (word lists, rule lists, etc.), and comment briefly on the success or failure of the main cracking strategies you employed. Also identify which hash function was used and report (based on Hashcat's benchmarking/profiling features) how quickly you were able to make guesses against passwords stored with that hash function. What does this tell you about password hashing?

What and How to Submit

1. Please upload to [**Canvas**](https://canvas.uchicago.edu/courses/47779/assignments/528942) the following files. (1) <YOUR CNETID>-problem1-rockyou.py or similar (2) <YOUR CNETID>-problem1-automation.py or similar (3) The file shadow (4) Either *CNET*-problem3.pot or *CNET*-problem3.txt. **Do not** upload source files (e.g., password leaks) that you used since those are often huge files and we don't need to see them.
1. Please upload to [**Gradescope**Links to an external site.](https://www.gradescope.com/courses/481333/assignments/2604820/) a PDF file that includes your prose answers to the questions asked above for Problem 1 and Problem 3.





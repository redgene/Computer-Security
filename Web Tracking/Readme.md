Web Tracking (50 points)
The Broad Setting of this Half of the Assignment
In previous assignments, you attacked the security of a system. Here, you will attack users' privacy, further learning about how easy it is to track people online to enable targeted advertising or even more nefarious uses. This assignment lets you more deeply explore the different techniques we discussed in class for tracking users on the web. In particular, you will set up a web server on a Linux virtual machine (VM) and create your own tracking infrastructure. When you are ready to test your infrastructure, you will indicate this on a machine we control, causing web traffic to visit your site. Because the visits incur non-trivial overhead on our end because of the way we are isolating browser visits between students, we have created a series of test cases that each cause a small amount of traffic focused on a single tracking-related attribute. In the final step of the project, you will indicate that you are ready for a full test, which will fire up our full fleet of browsing traffic.

Like many of our previous assignments, you will need to gain a bit of experience with a number of commonly used technologies to complete this assignment. This approach helps you explore computer security and privacy on an intellectual level while at the same time gaining practical computing skills. On the skill side, to complete this assignment will probably require you to learn at least a little bit of Linux (Ubuntu) server administration on the command line, Apache (or some other web server) configuration, MySQL (or some other database), JavaScript, and either PHP or Python to connect to the database. You will also have to think deeply about online tracking and how to leverage both overt and subtle information leaks to infer when website page visits are from the same person.

Before getting to the problems, we discuss the rules for this assignment and how you can access the assignment infrastructure for your tracking system.

Note that, in this assignment, your write-up file will not a PDF. Instead, you will be copy-pasting your text answers into appropriate textboxes on Gradescope.

Rules
As with all assignments, follow the course policy and cite any sources you use. You may Google liberally to learn about how to configure Apache, use JavaScript, use MySQL (or another database of your choosing), write to the database (e.g., using PHP), or navigate the command line. You may also Google liberally to learn the concepts underlying fingerprinting. You may not, however, use or consult existing libraries for browser fingerprinting, nor may you use other people's code (e.g., on StackOverflow) for browser fingerprinting. Your solutions, as well as the precise way you turn the concepts into code, should be your own. Again, per the course policy, you must note at the end of your write-up for each task the sources you referenced. Please note any you found particularly helpful since we might include them in future versions of this write-up. Furthermore, note that you are not permitted to view or copy what your classmates are doing. All servers have visit logs that the course staff can read.

Assignment Tech Set-Up and Overview
This assignment involves setting up your own server and configuring it (both through installing and configuring existing software packages and through writing your own code) to track website visitors. Our CS department Tech Staff has generously created a virtual machine for each student in the class. These virtual machines run Linux, specifically Ubuntu. You have root (sudo) on your VM, and you didn't even need to guess anyone's password for that privilege in this assignment.

Instead of using a password to authenticate, you will log in using your ssh key pair. We have created subdomains for all of you as follows, configuring DNS so that your subdomain points to your VM:


You can ssh into your VM (using your public key) on the host CNET@DOMAIN. For instance, the example student at the end of this list would run ssh student@student.example.com (optionally with the -i flag to point to your private key if you need to do this for previous assignments).

As in past assignments, you may implement your code in whatever programming language and environment you choose. Below, we give detailed pointers towards tutorials for doing it in the way we think is easiest. If you prefer nginx to Apache or MongoDB to MySQL, etc., feel free to do what you want. Note, though, that we can provide the most detailed assistance for our recommended approach.

Step 1: Setting up a web server/certificate (2 points total)
Log in
Your first job in this assignment is to set up your VM as a web server. To log into your server (assuming you've provided us your public key and given us time to set it up), follow the instructions above. You are welcome to install any other packages (e.g., emacs) you'd like on your VM.

Install Apache as your web server (0 points total, but required)
Great, now you're logged into your VM and seeing an Ubuntu command prompt. Now, you need to install a webserver (we'll use Apache) and a way to create databases (we'll use MySQL). On the command line of your VM, follow these steps, which are based on https://phoenixnap.com/kb/how-to-install-lamp-stack-on-ubuntuLinks to an external site., yet adjusted for what we'll need.

sudo apt-get update
sudo apt-get install apache2
sudo rm /etc/apache2/sites-available/default-ssl.conf (to remove a file we don't need)
sudo vi /etc/apache2/sites-available/000-default.conf
This brings you into a config file, where you'll notice the following line commented out: #ServerName www.example.com. Uncomment this line and change it to match your subdomain (e.g., ServerName student.example.com)
sudo service apache2 restart (to restart Apache)
Verify that this worked by opening up a browser on your own computer and going to your server (e.g., http://student.example.com, noting the http (not https). You should see the Apache2 Ubuntu Default Page.
Get a certificate (0 points total, but required)
Ok. Now let's get an HTTPS certificate for your server using Let's Encrypt. Run the following:

sudo apt install python3-certbot-apache
sudo letsencrypt
When you are asked about redirecting to HTTPS, choose "Redirect," which is choice 2.
sudo service apache2 restart (to restart Apache)
Verify that this worked by opening up a browser on your own computer and going to your server (e.g., https://student.example.com, noting the s in https). You should still see the Apache2 Ubuntu Default Page, but now you're connected over TLS.
Install PHP (0 points total, but required)
Instead of installing PHP, feel free to substitute whatever you want to use (e.g., Python) in its place. If you do indeed want to go with PHP:

sudo apt-get install php libapache2-mod-php php-mysql
Install MySQL as your database and create your database schema (2 points)
Next we need a database. We suggest using MySQL. Follow the steps on https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04Links to an external site. to install MySQL on your VM. Some quick notes. After you install the package in the first step, you will probably have to run the command sudo service mysql start to start MySQL. When you do sudo mysql_secure_installation you should say yes to everything they ask and, as part of those steps, create a root password. Save it somewhere. By the end of Step 3, you'll have created a user for your MySQL instance. Note also that the tutorial's suggested command of systemctl status mysql.service to check the status won't work because of the way Tech Staff installed Ubuntu within a container for you all. Don't worry that trying to run that command fails! If you run top you can see that mysqld is indeed running properly.

Now you need to create a database and probably create a table in the database. You're going to use this database in subsequent parts of the assignment to store the data, so you should read the rest of the assignment first to guide your design of a table schema. Specifically, think about the information you will need to track from each visit You can initialize the database from the mysql console. As you did above, run mysql -u THEUSERYOUCREATED -p and then follow the directions on https://www.tutorialsweb.com/sql/working-with-mysql.htmLinks to an external site. starting at Step D. For a more comprehensive tutorial, check out https://www.tutorialspoint.com/mysql/index.htmLinks to an external site.. You could instead do all of the database administration directly in PHP without opening the console: https://www.w3schools.in/mysql/php-mysql-create/Links to an external site.

What to submit for this part
We can just visit your VM to verify that you did most of the things we asked. That is, if we can't reach the website hosted on your VM, we'll assume you did not do this part. In other words, keep your VM up so that we can verify you finished this step.

In your write-up (Step 1), present the schema (column headers) you chose for your database and justify this design.

Step 2: Be able to write to your database (3 points)
In the remainder of the assignment, you will be writing HTML/JavaScript that tracks visitors to your website. That code will track visitors on the client side (their own computer), so you will need to send the information back to your server. You will need to write code that takes information sent by your JavaScript code and writes it to the database you just created. Because this will be code running on your server, you should be thinking about server-side technologies like PHP or Python.

One of the first things you'll probably want do is to take ownership of the directory for your webpage, which is currently owned by root:

sudo chown -R CNET:CNET /var/www/html (don't forget to replace CNET with your own, as in all other parts of these instructions)
Similarly, when you upload files, you may want to make sure the permissions are correct (e.g., PHP files need to have execute permissions --- +x --- for all users since your Apache server runs as www-data, not your user. If the permissions are wrong, fix them using chmod. Note that we didn't have any problems with the default permissions, so you may be able to skip this step.

We recommend thinking about your design in the following way: Someone visits your webpage. They make GET requests to your server for HTML and JavaScript code you will have written. This HTML and JavaScript code will do the profiling described below in Step 3. Now, you have fingerprinted the user on their own computer, but you need to get the data back to your server. Therefore, as part of this JavaScript code, make an AJAX request to your server sending back the values you have profiled. (For developing and testing this current step, simply use placeholder values instead of profiles.) You'll need some code running on your server (e.g., PHP, Python) to retrieve these values and (different from sink.php) write them to the database you created in the last step.

Because we haven't covered this in class, feel free to Google liberally about how to do this and feel free to reuse code from others for this step, with attribution of course.

Once you have established that people visiting your webpage have their (placeholder) profile sent back to your server and written to your database, you are ready to proceed.

What to submit for this part
Submit all code you wrote for this part.

In your shared write-up (Step 2), briefly discuss your design and give us pointers to the file names of the code that accomplished each part of your design.

Step 3: Tracking particular attributes (35 points total)
This step is the main point of this assignment. Here, you will explore using a number of different methods, from cookies to browser fingerprinting, to track visitors to your site. For each of these sub-steps, we have written test cases. When you have updated your HTML / JavaScript to profile people in the way specified by each sub-step and deployed it on your server, you can test it with your own browser by visiting that page. Once that seems to be working (comparing your browser configuration to what you see being written to your database), you can start to request traffic from our test fleet. Go to https://fleet1.uchicago.techLinks to an external site. or https://fleet2.uchicago.techLinks to an external site. or https://fleet3.uchicago.techLinks to an external site. and enter your CNet ID and the desired test case into our queueing system. Our system sends traffic on the order of a handful of visits to your server.

DO NOT USE ALERT() IN YOUR TESTING. DO NOT PASSWORD PROTECT YOUR PAGE. IF, FOR ANY REASON, OUR CRAWLER SEEMS TO GET STUCK ON YOUR PAGE IN ONE FLEET, DO NOT TRY IT ON ANY OTHERS; POST ON CAMPUSWIRE SO WE CAN FIGURE OUT WHAT THE ISSUE IS.

As described below, you will be turning in your profiling code as well as a clustering of pages visits based on your profiles. Each visit will be labeled between 1 and 500 based on the file name visited. In other words, there are 500 possible files we could be visiting, and your server should be able to fulfill GET requests for any of those 500. To make this easier for you, we have distributed a short script called duplicate.sh that, if you name your HTML file track.html, will make 500 identical copies of it numbered 1.html through 500.html. Don't forget to re-run duplicate.sh each time you update your track.html file!

Step 3.1 Basic cookie tracking (5 points)
To detect which page visits are associated with each other (from the same user), set and get cookies.

Test using the "track using cookies" test case. (Our test case for this step causes 3 visits to your page, 2 of which are from the same person.)

Step 3.2 Track by IP address (5 points)
To detect which page visits are associated with each other (from the same user), track the IP address of the visitor. Note that you may have to make some sort of external call to figure out their IP address; the client's IP address isn't natively available in JavaScript.

Use the "detect different IP addresses" test case.

Step 3.3 Track visitors based on window size (5 points)
To detect which page visits are associated with each other (from the same user), examine the size of the window in which the visitor is viewing the page.

Test using the "detect different devices (user agents) and window sizes" test case.

Step 3.4 Track visitors by the user agent string (5 points)
To detect which page visits are associated with each other (from the same user), rely on the client's user agent string.

Test using the "detect different devices (user agents) and window sizes" test case.

Step 3.5 Track visitors by whether cookies are enabled (5 points)
To detect which page visits are associated with each other (from the same user), check whether the client is letting you set cookies at all.

Test using the "detect whether cookies are enabled" test case.

Step 3.6 Track visitors by fingerprinting based on the fonts installed (5 points)
Different fonts render text as different sizes on screen and that the browser can view the computed size of different elements on a webpage. Exploit this fact to detect which fonts the user has installed. Hint: try making a span on your page and measuring the width with a varied amount of text (lots of different characters) inside. Specifically, different fonts will take up different amounts of space for specific characters. Also look up how browsers handle when fonts are unavailable; you can define "fallback" fonts, which you will probably need to do to run this attack.

To make this task more tractable, assume that these are the only five fonts that are possible (so consider only whether or not the user has these five fonts installed):

Abyssinica SIL
DejaVu Sans
GFS Baskerville
Liberation Sans
Roboto
Test using the "detect different fonts installed" test case. For this sub-step only, all 5 test case visits are different. In your write-up, you should provide us a mapping of the visit number (e.g., 100) and which of the above fonts are NOT installed (e.g., DejaVu Sans). In the CNET-step3.txt file, simply put each of the 5 test case visits in their own cluster for this sub-part.

Step 3.7 Track visitors by fingerprinting whether JavaScript is enabled (5 points)
In this step, you will distinguish visits based on whether or not the client has JavaScript enabled. Note that this will almost certainly require you to rethink the way you are sending data to your server since you were probably using JavaScript to do so. Think back to tricks we played when discussing web security attacks to get around this. You may also need to write a different sink function on your server to work with the new way you are sending data to the server. As a hint, look up the HTML noscript tag.

Test using the "Detect whether JavaScript is enabled" test case.

Note that we do not have any visitors in Step 4 with JavaScript disabled, so you don't have to worry about this there.

What to submit for this part
First, submit all code you wrote for this part. This might be as simple as uploading substantially updated versions of the files from Step 2, though with different file names.

Second, report the page-visit clusters you find in each sub-step in a file called CNET-step3.txt (it must be a txt file, not a doc or pdf or anything else), structured as follows. For each sub-step of Step 3, report each of your page-visit clusters based only on the specific metric investigated in this sub-step. Each sub-step should be on its own line, and the lines (sub-steps) should be in the same order as in this document. As a result, there should be exactly 107 lines in this file. If you do not finish a sub-step, leave its line blank. Page numbers within a cluster should be delimited by a comma (no spaces), and clusters on a line should be delimited by a single space. Within each cluster, page numbers should be sorted in ascending order. Clusters on a line should be sorted in ascending order based on the first page listed in the cluster (the page in that cluster with the smallest page number). Leave out .html from all page visits.

For example, if you received visits to pages 53.html, 20.html, 400.html, and 32.html for Sub-step 3.1 (these are not the real page visits) and you determine by this metric alone, 53 and 32 are associated and 20 and 400 are associated, then the first line of your file would be 20,400 32,53. Note that there is exactly one space in this line. Subsequent sub-steps should have similar lines. Note that different clusters may have different numbers of pages in them, and different sub-steps may have different number of clusters and pages. Note that this file includes sub-steps 3.6 (fonts), for which we noted above that each page is in its own cluster.

Third, in your write-up, respond to the following points for each of the sub-steps 3.1 through 3.7:

Briefly (in one sentence) describe your approach to putting this sub-steps's method of tracking into action.
For each sub-step we want you to reflect on why this type of tracking remains possible in browsers. In two or three sentences, describe how this type of tracking could be stopped (e.g., what features/calls would need to be eliminated from browsers), if at all, as well as what desirable benefits to websites (if applicable to that method) would be lost as a result of eliminating that functionality. If it were up to you, would you eliminate those features to prevent this type of tracking? Why/why not?
(For sub-step 3.6 only) Write which font(s) are not installed on each different visit you receive in this sub-step. For example, if the visit to 500.html does not have Roboto and the visit to 300.html does not have DejaVu Sans, write "300: DejaVu Sans, 500: Roboto."
Step 4: Tracking using multiple attributes (10 points total)
Finally, unleash the full fleet of visits by adding yourself to the queue on https://fleet1.uchicago.techLinks to an external site. or https://fleet2.uchicago.techLinks to an external site. or https://fleet3.uchicago.techLinks to an external site.. Using the full set of features from the previous step, cluster the page visits that appear to have come from the same person.

What to submit for this part
You will likely be able to simply reuse the code from the last step. If you did update your code, submit the updated code with a different file name.

As for Step 3, submit a file called CNET-step4.txt that contains the clusters you found. This file should have exactly one line. Clusters should be delimited by a single space, and pages within a cluster should be sorted and delimited by a comma. Follow the sorting conventions from Step 3.

Finally, in your shared write-up file (labeled Step 4), write at most a paragraph discussing how stable the different features you were tracking are over time. That is, which features might change for a given user a month from now? How might these changes manifest, and could you perhaps still associate the pre-change and post-change visits?

What and How to Submit
Please upload to Canvas three different kinds of files. (1) A file CNET-step3.txt (it must be a text file) with your clusters for the sub-steps in Step 3. There should be exactly 7 lines in this file. We detail the required format above. (2) A file CNET-step4.txt (it must be a text file) with your clusters for Step 4. There should be exactly 1 line in this file. We detail the required format above. (3) All code you used in this assignment. These are discussed for each individual step above. Your shared writeup file should make clear (e.g., by referencing file names) which files were used to solve which steps. For this reason, please pick descriptive filenames. Feel free to upload files individually to Canvas or submit a single zip/tar/gzip/7zip archive.

Please copy and paste into the GradescopeLinks to an external site. text boxes your prose answers to all questions above. We don't accept a PDF; only copy-pasted answers in the text boxes.


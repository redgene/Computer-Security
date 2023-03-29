Assignment 7, Part 1 of 2: Web Security (50 points)
This assignment lets you practice a few different web security attacks we've learned about. There exist short solutions to each problem, but you will need to learn new concepts and how to use new languages and techniques. Before getting to the problems, we discuss the rules for this assignment and how you can access the assignment infrastructure for your attacks.

Notes
As with all assignments in this course, remember to cite any sources you use and name any fellow students with whom you discussed the assignment (per the course syllabus). You may Google liberally to learn helpful aspects of HTML/JavaScript, how web browsers work, or to learn more about the web security techniques discussed in class.

Your attacks for this assignment should be those discussed below. Do not attempt to compromise our server, sniff your classmates' network traffic (i.e., no Wireshark this time), or do other nefarious things. You will not receive credit for breaking into the server. In fact, you will lose credit for doing so.

This assignment was built by Blase for this class over the last few years and edited in a number of ways this year. Please let us know if you find bugs or need instructions fleshed out by posting on Campuswire.

Detailed Tech Set-Up and Overview
This assignment involves visiting and interacting with pages on: https://insecurityclass.cs.uchicago.edu/. You will be visiting pages on our server in a web browser.

As in past assignments, you may implement your code in whatever programming language you choose. That said, not all of the problems require writing any substantial amount of code. In fact, many problems simply involve generating some very carefully crafted inputs or interactions with the server. You will be submitting these carefully crafted inputs or interactions alongside descriptions of how you generated them and how they work. However, in the process of crafting these inputs, you will likely have to experiment on your own. You should submit any test pages / minimal working examples you made for yourself in figuring out how to craft these inputs.

Please don't overwhelm the server. It will support thousands of queries per student (which you may need), but not millions. If you are very sure that an input should be working (especially if it did earlier) but it no longer does, please let us know on Campuswire.

There is some small chance that a large amount of traffic will cause our automated infrastructure problems. Notably, don't use alert() in your testing, but rather write to the console with console.log() because alert is blocking and will cause problems in the automated infrastructure for you and your classmates. Seriously, please do not use alert; we are logging the contents of the pages we visit, so we will know that you are to blame!

Problem 1: Authentication By Cookie (10 points)
Following in the footsteps of successful cryptocurrencies like Ethereum, the world's newest, most exciting cryptocurrency — Dcash — is about to start offering non-fungible tokens (NFTs). Unfortunately, since time was short, the mysterious, shadowy figure who created Dcash put together a website to keep track of Dcash in a very quick and slipshod manner. As a result, it has many basic security holes. In this problem, you will bypass a very simple security mechanism.

On https://insecurityclass.cs.uchicago.edu/1/ the creator of Dcash has set up a portal for individuals to obtain a secret access code to begin trading Dcash in advance of the NFT auction. People who send a specified amount of dollars to the creator are assigned premium accounts, which enables them to generate their secret access code. Unfortunately, the way they keep track of, and verify, who is a premium member isn't very smart. Explore this by going to https://insecurityclass.cs.uchicago.edu/1/index.php?username=CNETID, replacing CNETID with your CNetID. Take a look at how persistent state is being kept. Leveraging what you learn, and without spending any dollars, become a premium member and get yourself an access code to the Dcash ICO.

What to submit for this part

You are not required to write any code to solve this problem.

In your shared write-up file (pdf that you will submit to Gradescope), describe your approach to solving this problem and include your secret access code clearly labeled. Also briefly describe why the way the Dcash creator tried to handle authentication is fundamentally incorrect. What should they have done differently?

Problem 2: Easy CSRF (10 points)
The founder of Dcash has decided to give everyone in the class 1000 Dcash in advance of the ICO. On https://insecurityclass.cs.uchicago.edu/2/ they created a tracker to know who has particular amounts of Dcash. Why might some people have a value different than 1000 when you look? That's a great question. The founder decided to let early holders of Dcash transfer some of their Dcash to other users. Of course, some authentication is necessary. Thus, transfers are only valid when presented alongside the secret access token discovered in Problem 1. That is, the sender's CNetID and that sender's secret access token must be presented in conjunction for the transfer to be accepted. This means that you can give other people your Dcash, but you can't take theirs. Or can you?

The founder of Dcash wanted to be able to transfer Dcash arbitrarily between users, so the secretive founder has configured the site such that when they are logged in and making the transfer request, they do not need to provide an access token.

The founder is also kind of a creeper and likes to look up the webpages of people who hold Dcash. Can you make a homepage that uses some clever CSRF to transfer Dcash from one of the instructors (blase or davidcash) to yourself?

Follow these instructions to set up your own homepage on the CS department servers. (The following steps assume you have a CS account; please let us know if you don't have one). Log into linux.cs.uchicago.edu (e.g., by running ssh CNETID@linux.cs.uchicago.edu to log in) and follow the instructions on https://howto.cs.uchicago.edu/techstaff:personal_homepage to create a homepage if you don't have one already. Carefully follow the steps outlined on Techstaff's webpage to set permissions on the different directories and on each file you create, including those we ask you to create to solve different problems. (If you don't set the permissions properly, the file will not be accessible to the founder, or to anyone. If you are getting "forbidden" messages when you look at your own files, you probably forgot to set the permissions for each file with chmod.)

Create your exploit file as assignment6-2.html so that it is accessible at https://people.cs.uchicago.edu/~CNETID/assignment7-2.html (note the tilde, and replace CNETID with your own). Seriously, don't forget to set the permissions on this file or else it can't be opened. If you can visit this file in your own web browser, so can the founder.

Every few minutes, the founder visits your page (over HTTPS). If your CSRF works, then you will notice your transaction reflected in the amounts of Dcash your sender and recipient have within a few minutes. For your own sanity, we have set up a status page that lets you see when the founder most recently visited each person's page: https://insecurityclass.cs.uchicago.edu/status2.txt

After you get the exploit working, please delete assignment7-2.html from your web directory. It is a violation of the university academic integrity policy to try looking at other students' HTML pages and the university keeps server logs. So do we.

For both student privacy and to facilitate your testing, all Dcash amounts reset to 1000 every hour on the hour. That is, don't be shocked when your ill-gotten gains disappear hourly.

What to submit for this part

Include your assignment7-2.html file in what you submit on Canvas.

Furthermore, in your shared write-up file (pdf that you will submit to Gradescope), describe your approach to solving this problem. Also briefly describe the primary reasons the Dcash creator was vulnerable to a CSRF attack on the page they made.

Problem 3: Harder CSRF: Overcoming Badly Designed CSRF Tokens (10 points)
Feeling a bit embarrassed by falling victim to CSRF, the founder changes their approach to authentication and attempting to stop CSRF attacks. At the same time, the founder is getting into the (terribly ill-advised) NFT trend! The founder of Dcash has decided to hold an auction for NFTs created by the different members of the class. The founder specifically is aiming to make themselves a fortune by investing in some of your NFTs. On https://insecurityclass.cs.uchicago.edu/3/, they created a tracker to show how much Dcash they have committed in this auction to each student's NFT.

Why might some people have a value different than 0 when you look? That's a great question. The founder decided to make things convenient for making bids in this auction and left their bidding form on top of the public tracker linked above. Of course, some authentication is necessary. Thus, transfers are only valid when presented alongside the founder's secret access token, which you don't have (and won't get or otherwise utilize in this problem). Whenever the founder visits your page, assume the founder is logged in with their secret access token automatically sent as a cookie.

However, using what they learned in cleaning up the security mess that was Problem 2, the founder designed the submission form to work quite a bit differently than the previous problem's form. Notably, the founder added a CSRF token to the page and now use POST requests, rather than GET requests. To compute the CSRF tokens, the founder is using a JavaScript crypto library. Unfortunately, the founder made some critical errors in designing the CSRF token, enabling you to still steal Dcash despite their attempt at security!

The founder continues to be a creeper. Every few minutes, the founder visits this new page you created (over HTTPS). If your CSRF works, then you will notice your transaction reflected in the amounts of Dcash your sender and recipient have within a few minutes. Create your exploit file as assignment7-3.html in your directory on people.cs.uchicago.edu and again delete assignment7-3.html from your web directory after you get the exploit working.

Hint: Learn how to make AJAX requests. Note that AJAX requests do not send cookies by default, which would prevent the founder's cookies being sent by default when you make an AJAX request on their behalf. However, if you set AJAXobject.withCredentials = true; while making the request (replacing AJAXobject with the variable in which you stored your XMLHttpRequest object), the cookies will be sent. You are also welcome to use newer libraries (like fetch), but we haven't tested our sample solutions with them and can't guarantee that you'll be able to get them to work.

For both student privacy and to facilitate your testing, all Dcash amounts reset to 0 every hour on the hour. That is, don't be shocked when your ill-gotten gains disappear hourly. For your own sanity, we have again set up a status page that lets you see when the founder most recently visited each person's page: https://insecurityclass.cs.uchicago.edu/status3.txt

What to submit for this part

Include your assignment7-3.html file in what you submit on Canvas.

Furthermore, in your shared write-up file (pdf that you will upload to Gradescope), describe your approach to solving this problem. Also briefly describe (i) what the Dcash creator did wrong in designing their CSRF token and (ii) what the Dcash creator could have configured on the server to further protect themselves from this problem.

Problem 4: XSS-based Deanonymization (10 points)
At this point, you are probably curious who the founder of Dcash really is. In this problem, you will unmask them. You notice that when you visit your message page at https://insecurityclass.cs.uchicago.edu/4/ it takes your username from your browser cookie (from Problem 1) and fills it into the page. Well, since you can send messages to the founder and they presumably will be reading your messages on a page with the same layout, you have an opportunity to figure out their name!

In this problem, you'll send the founder a message and use XSS to exfiltrate their name.

Of course, after your message extracts their name from the page, it is still running locally on the founder's browser, so you'll need to send this data somewhere. Conveniently, the narcissistic founder created a guestbook on the page that is linked from https://insecurityclass.cs.uchicago.edu/4/ and which you can use as a place to send your data. Note that the secret thenighttheskeletonscametolife is needed to write things to the guestbook since I didn't want to leave the ability to write to our website open to the world without any meaningful filtering! In your testing, first write code that you can confirm automatically writes to the guestbook when you visit it, and then try editing it so that you can visit a similar page as the founder is visiting and send your own data to the guestbook. Finally send it to the founder. Note that the guestbook automatically resets every 10 minutes (at :00, :10, :15, etc.) for privacy and sanity.

What to submit for this part

In your shared write-up file, describe your approach to solving this problem and include the exact message you sent the founder, clearly labeled (e.g., in bold text). Also include the full name of the founder clearly labeled, such as in bold text. Note that if you only have a one-word name for the founder, you're not quite done (and, to move forward, read about URL encoding of URL parameters!). Also briefly describe how the founder could have protected against this attack.

You do not need to submit any code for this problem if you didn't use any. However, if you created any sample/test files (e.g., HTML files) or wrote any code to help craft your input, please submit those in their native format.

Problem 5: Bobby Tables Joins The Dcash Ecosystem (10 points)
The mysterious and secretive, but also careless, founder of Dcash is getting ready for the Dcash NFT auction and has put together a finalized version of the site to track the bids for each person's NFT. You might notice they are making Dcash rather centralized for a decentralized cryptocurrency, but we can ignore that. In any case, you've realized that you can go to https://insecurityclass.cs.uchicago.edu/5/ and yet again see how much Dcash the founder has bid for a particular user's NFT. Don't be alarmed that your Dcash bids from previous problems has disappeared. According to this new database, everyone starts off with no Dcash.

Because we don't want to leave a vulnerable database open to the web, please use username: cs232 and password: Imissghostalready to access this directory.

The founder lets you query for a particular username to see how much Dcash they have. The things you type into this field are used for a MySQL query. Given the founder's track record, this is bad news for security. Use your best SQL Injection tricks to (separately) do the following two things:

Determine the full list of users in the database.
Give yourself some free Dcash. Hint: the table is called dcashaficionados and the columns should hopefully be obvious from this page.
If you weren't previously familiar with MySQL, you will probably have to read up on how queries are structured to solve this problem.

Note that, because the odds of one of you accidentally blowing up the database for this problem are high, it automatically resets every 5 minutes (on :00, :05, :10, and so on).

What to submit for this part

In your shared write-up file, describe your approach to solving this problem and include (clearly labeled, such as in bold) each value you entered into the name field to solve each of the two parts of this problem. Also include in this shared write-up file a list of the people identified in sub-part 1. Finally, briefly describe how the founder could have protected against this attack.

You do not need to submit any code for this problem if you didn't use any. However, if you created any sample/test files (e.g., HTML files) or wrote any code to help craft your input, please submit those in their native format.

What and How to Submit
Submit to Canvas all code written for this assignment.

Submit to GradescopeLinks to an external site. your written answers as a PDF.


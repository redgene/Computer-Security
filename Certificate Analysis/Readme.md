Assignment 5, Part 2: The X.509 Certificate Landscape (50 points)
The Broad Setting
In class, you learned about TLS and how X.509 certificates (the certs that websites present when you connect over HTTPS) are structured and verified. In this part of the assignment, you will run your own measurement study to understand how certs are deployed in the wild.

Assignment Tech Set-Up and Overview
Our reference solution is written in Python 3, but you can choose to do the assignment in any language that you want.

Step 0: Deciding what websites to visit (0 points officially, but needed to answer all of the remaining questions)
First things first, you need a list of websites whose certs you will analyze. You are going to use the Tranco list, specifically tranco-top-1m.csv. The entries in that file, which contains the million most popular websites ordered by rank. If you are curious, you can optionally check out the Tranco list websiteLinks to an external site. to learn how the ranks of each website are calculated.

Before using this list, you are welcome (but in no way required) to go through the list manually and remove any sites that you do not feel comfortable having your program contacting, or writing automatic rules that eliminate sites.

We want you to create two lists of sites each in the same format as the full Tranco list. First, create a list of the top 1,000 domains in the Tranco list; we'll call this list Top Sites for the rest of the assignment. Second, create a random sample of 1,000 domains among all million sites; we'll call this list Random Sample for the rest of the assignment.

Include these files as step0-topsites.csv and step0-randomsample.csv in your submission in case we need to reproduce your crawl. Of course, anyone who hasn't chosen to remove any sites they find objectionable would have the same Top Sites list.

Step 1: Measuring HTTPS usage (15 points)
As we talked about in class, websites served over HTTPS (i.e., of the form https://domain) are encrypted using TLS. Sites that are served over HTTP (i.e., of the form http://domain) are not encrypted. For the rest of this paragraph, we'll give you a few examples; please try these in your own web browser before your proceed so that you know what these different situations look like to humans browsing the web! You will find that many websites (e.g., http://uchicago.edu/) will automatically redirect to HTTPS if you try to load them over HTTP. However, there are some that don't; for instance, you can load the University of Washington's webpage either unencrypted by visiting http://www.washington.edu/ or encrypted by visiting https://www.washington.edu/ instead. We can also see some cases where sites are not accessible over HTTPS. The site http://tocumenpanama.aero/ loads fine over HTTP, but throws a "connection closed" error when https://tocumenpanama.aero/ is contacted, which is probably a misconfiguration on their part. If you try to load kingcashisafraud.com either over HTTP or HTTPS, it throws a non-existent (NX) domain error (assuming no one in the class spent $12 to register it between when this assignment was released and when it was due). You can also find errors in certificates. For instance, whereas http://www.squid-cache.org/ loads just fine, https://www.squid-cache.org/ throws an "invalid certificate" error since the certificate presented was issued for a different domain.

For this first step, we want you to write code that allows you to map separately for the domains in both of your samples (Top Sites and Random Sample) the following state of encryption on the web:

Question 1. Report separately for Top Sites and Random Sample: (a) what fraction of websites are accessible only over HTTPS since HTTP redirects to HTTPS; (b) what fraction of websites are available over both HTTP and HTTPS separately; (c) what fraction of websites are available only over HTTP; (d) what fractions of websites are not available at all. Report the aggregate values in your write-up along with your interpretation of what these values suggest to you about the state of encryption on the web. Also submit files step1-topsites.csv and step1-randomsample.csv that add a new (third) column to the CSV containing one of the four following values corresponding respectively to situations a-d: (a) HTTPSonly; (b) both; (c) HTTPonly; (d) neither.

If you're using Python, we recommend that you use the RequestsLinks to an external site. library. There are lots of other libraries for Python that can be used for downloading webpages, but this is (in our opinion) the easiest and most straightforward. Note that you can make requests of the following form:

import requests
r = requests.get('https://uchicago.edu')
Hints: You can get the HTTP status codeLinks to an external site. returned by the site from the request above with r.status_code, and you can also get the URL of the resource ultimately loaded after redirects with r.url.

Another hint: If you use the Requests library to try to download a page that throws an error or doesn't exist, your Python program will terminate with an error. How do you handle this so that you can both keep going without needing to constantly restart your program and also document the errors thrown by the Requests library? Read about Try-ExceptLinks to an external site. in Python.

Step 2: Retrieving Certificates (0 points officially, but needed to answer all of the remaining questions)
Next, write code that attempts to retrieve the certificates for all sites available over HTTPS (cases a and b from the previous step) from the previous step for both the Top Sites and Random Sample.

Some helpful hints: * There are multiple ways to get the certs themselves; the Python libraries sslLinks to an external site. and pyOpenSSLLinks to an external site. can both be used to download the certificate from a particular host. Regardless of how you get the certificate in Python, we strongly recommend the pyOpenSSLLinks to an external site. library for analyzing the certs AFTER you have obtained them. Depending on the method you use, looking into the "OpenSSL.crypto.load_certificate" and "ssl.DER_cert_to_PEM_cert" functions might be helpful. * You will not be able to get the certificates for every single website. This is okay! Some websites don't have certificates, or there might be other fundamental reasons why you cannot access a particular cert. As a result, you'll be getting certs for the subset of the top 1,000 sites that are reachable, as opposed to getting 1,000 certs total.

Step 3: Analyzing Certificates (35 points total; 5 points each)
Now that you have the certificates from (many of) the top 1,000 most popular websites and your random sample of 1,000 of the million most popular websites, it is time to start looking at them! Answer the following prompts in your shared write-up file. For each, please write a couple of sentences about the patterns you found and why they might occur, as well as a comparison between the 1,000 most popular websites and your random sample. Additionally, for each question please include some type of visualizations as justification for your answer (e.g., a graph, table).

Question 2. Please list the CAs that issued one or more certificates in your crawl in alphabetical order. Who are the most common CAs, and does the usage of particular CAs seem to vary with the popularity of the site? Note: please use the "Organization Name," NOT the "Common Name."

Question 3. What is the range of how long certificates are valid for? Do you see any patterns in the lengths of time certificates are valid for? Do you notice any connections between the length of time a cert is valid and the CA that issued the certificate?

Question 4. What is the most common issuer country for the certificates you collected?

Question 5. What types of cryptographic algorithms are used in these certs? Please list the actual names, not their numerical codes. What type is the most common?

Question 6. What key lengths are associated with each type of public key types (crypto algorithms) you found?

Question 7. For public key types that have an associated exponent, do you see any pattern in the exponent used? Does it vary with webpage rank or the CA that issued the certificate? Why might you see this pattern?

Question 8. What is the most common signature algorithm for the certificates that you collected?


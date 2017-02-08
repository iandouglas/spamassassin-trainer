# SpamAssassin Trainer script for cPanel

Current version: 4.04

I jokingly call v4.04 "Support Not Found" as a play on the typical 404 "page not found" error you get on the web. I am no longer actively maintaining this script, nor actively supporting it. I'll work on bug fixes from time to time.

## Thanks for the support over the years

**DEPRECATION NOTICE:** As of March 1st, 2016, I will no longer be supporting my SpamAssassin trainer script. I will maintain bug fixes at GitHub where [I set up a repository](https://github.com/iandouglas/spamassassin-trainer) for the code a long time ago, but I will no longer be supporting users who choose to download and use the script.

I've been helping folks battle spam using this script in one form or another since early 2003, and it's time to focus on other things. I truly appreciate the support of everyone who has downloaded sa-trainer over the years.

To be clear, I'm not the author of the training script that ships with Apache's SpamAssassin project. I simply wrote a cPanel-compatible CGI script in Perl that could utilize SpamAssassin to train it to learn what you consider spam or non-spam.

#### Frequently Asked Questions about halting development

**Q:** Will the script stop working?  
**A:** No, the sa-trainer script will continue to work as long as it's configured properly and has access to SpamAssassin on your cPanel-based system. The callback to iandouglas.com to watch for new versions has been taken out of v4.04.

**Q:** Can we still contact you for help?  
**A:** Yeah, but I'm less inclined to respond as quickly as in the past. I'd prefer if you [open an issue](https://github.com/iandouglas/spamassassin-trainer/issues) over at GitHub where others could potentially help as well.

**Q:** Where can we find updates to the script from now on?  
**A:** I'll maintain big fixes at GitHub for existing things that are reproducable bugs, but I'm not going to introduce any new changes going forward, nor will I release new versions just because cPanel decided to change where SpamAssassin gets installed on your server.

# Background
This script setup is meant for people who are on shared hosting accounts with services who offer cPanel, although with some editing, you can adapt this to run on a virtual private server as well.

Up until about late 2010, cPanel didn't give you the means to train your own SpamAssassin tokens for locally-hosted mailboxes, so I wrote a very simple script that you can call from your cgi-bin folder which will scan for your mailboxes and train SpamAssassin for you, which should give you a *dramatic* reduction of spam in your inbox.

## Support
If you use this script, please help out others who have questions. I'm not actively supporting this, but I may pay attention to pull requests from time to time if anyone wants to submit ideas on improvements.

## Configuration

There are only two things you need to change in the Perl script and only one change in the user_prefs file:
- In the `sa-trainer.cgi` script, you will need to configure your domain name and cPanel username where noted.
- In the `user_prefs` file, there's a place where you need to enter your cpanel username.


## Installation

- sa-trainer.cgi
 - Place this file into your public_html/cgi-bin folder and set its permissions to 755

- user_prefs
 - Place this file into your home directory in a subfolder called ".spamassassin" (with the preceeding period in the filename)


## Documentation

There are also heavy amounts of commenting in the Perl script itself, but more background, etc., can be found below.


**DISCLAIMER:** If you're fairly new to using my SpamAssassin training script, be sure to read the instructions carefully. While I've tried to document this as carefully as I can, every hosting environment can be completely different than the next. I CANNOT BE HELD RESPONSIBLE FOR ANY NEGATIVE EFFECTS FROM USING THIS SCRIPT, AND BY USING IT YOU AGREE TO RELEASE ME FROM ALL LIABILITY. THERE ARE NO GUARANTEES ON THESE INSTRUCTIONS OR THE SCRIPT OR USING THE SCRIPT WHATSOEVER. NO WARRANTY OR CLAIM IS MADE THAT USING ANY OF THIS WILL HELP REDUCE THE AMOUNT OF SPAM YOU GET. (but it _should_ drastically reduce it after training it for a few weeks...)

**Second Disclaimer:** I am not affiliated with [SpamAssassin](http://spamassassin.apache.org/), and while I originally wrote this script and documentation to assist my own hosting account at LunarPages, I am not employed in any capacity by LunarPages. My trainer script is not part of SpamAssassin's official release, nor is it the actual "SpamAssassin Trainer" (it merely augments its functionality for cPanel-based hosting providers. My script is not part of cPanel. None of these groups will give you any direct support for my script.

If You are a LunarPages user, Your Primary Support Source is [THE HOWTO guide at LunarForums.com](http://www.lunarforums.com/web-hosting-tutorials-faqs-and-resources/how-to-train-spamassassin-updated-april-27-2010). LunarPages has asked that I direct all LunarPages users back to their forums where I posted my original thread, which I'm absolutely happy to do. I get a kick out of knowing that my script has made such an impact for their client base, and happy to direct people back to LunarForums for help.

### Other Support Info

Please open an ['issue' at GitHub](https://github.com/iandouglas/spamassassin-trainer/issues) for assistance with your copy of the script if you run into trouble. If you contact me via Email, I can't guarantee a quick response, but I will ask you for the following pieces of information:

- a full copy of your sa-trainer.cgi script sent as an attachment
- a copy of your SpamAssassin user_prefs file sent as an attachment
- your domain name and CPanel username (do NOT send me your cPanel password!!!)
- the URL where you actually run the script so I can see what it's doing (or not)

## BACKGROUND

Between 1997 and 2004, I operated a small web hosting business ("wild web hosting"), and found SpamAssassin to be an invaluable tool to combat the flood of spam that would hit my systems on a daily basis. Some of my clients, prior to implementing SpamAssasin (SA), were getting hundreds of pieces of spam for every one piece of legitimate Email. When I closed my hosting business in April 2004, I needed a new hosting provider for my own personal domains, and after some research chose LunarPages.

I was happy to see that SA was a tool available, however the version of CPanel at the time did not allow us to actually train SpamAssassin, and to be honest, my work to get SA working on my LunarPages account to scan and track my own bayesian database was a bit of a hacker's delight, and I was happy to get it up and running. With the cPanel upgrade to v11 at LunarPages SpamAssassin has not operated as well as I'd like, and have had to make some operating changes to this sa-trainer script in order to maintain compatibility with LunarPages' systems. 

This spam training, from my experience with my now-defunct hosting business, was the difference between getting a trickle of spams every day or getting hundreds of spam messages per day, and getting one or two spam messages per day is still far better than getting tens of thousands delivered to my servers every day without SpamAssassin at all. Still, it would have been nice to have a CPanel interface for training spam... 

Since I already had scripts written to assist me in my hosting business, and found it to work at LunarPages with a little tweaking, I modified the script a little more and wrote a pretty lengthy post at LunarForums.com about training SpamAssassin. It was quickly accepted by LunarPages management as their "defacto" HOWTO article and, in the time the article has been live, has received tens of thousands of views and at least 20 pages of follow-up questions and comments from other users.

Statistical analysis on the callback feature of the v3 script to check for upgrades tells me that there were about 150 people per week using the script in early 2016.

I originally wrote my HOWTO article for supporting users at LunarPages, however I've personally tested the script successfully on four other hosting providers other than LunarPages which use standard cPanel virtual hosting. So, I figured I'd just make the instructions as generic as possible and make the claim that this script _should_ work with most standard cPanel installations. I did not need to tweak the operation portions of the script to run on any of the hosting environments I personally tested, I simply needed to change the _configurations_ slightly for path information which I've tried to eliminate in newer versions of the script.

In 2010, I decided I should move the HOWTO article to [my blog](http://iandouglas.com) and rewrite most of it to explain in greater detail what steps are necessary and why, since the forum software that LP uses only allows 20,000 bytes of information per message posting, and the new script itself is at 25kb and growing, so I'm unable to even post the script in their forums any longer.

With regards to long-term support of the sa-trainer script: I have moved my own personal accounts away from LunarPages in early 2008 for multiple reasons. One of those reasons is that I don't like how cPanel makes SpamAssassin operate now (like lack of subject line rewriting, or shorter Email headers), and I frankly need more control (like adding my own SA rules), so I rented a dedicated private server for my needs and later moved my domains to Google Apps.

## Background
This script setup is meant for people who are on shared hosting accounts with services who offer cPanel, although with some editing, you can adapt this to run on a virtual private server as well.

Up until about late 2010, cPanel didn't give you the means to train your own SpamAssassin tokens for locally-hosted mailboxes, so I wrote a very simple script that you can call from your cgi-bin folder which will scan for your mailboxes and train SpamAssassin for you, which should give you a *dramatic* reduction of spam in your inbox.

## Documentation
There are also heavy amounts of commenting in the Perl script itself, but more background, etc., can be found at http://iandouglas.com

## Support
I am available for support if you need assistance with the setup of the script, via paid one-on-one coaching via Google Helpouts: http://goo.gl/5l8ufr

## Configuration

There are only two things you need to change in the Perl script and only one change in the user_prefs file:

- In the CGI script, you will need to configure your domain name and cPanel username where noted.

- In the user_prefs file, there's a place where you need to enter your cpanel username.

## Installation

- sa-trainer.cgi
  Place this file into your public_html/cgi-bin folder and set its permissions to 755

- user_prefs
  Place this file into your home directory in a subfolder called ".spamassassin" (with the preceeding period in the filename)

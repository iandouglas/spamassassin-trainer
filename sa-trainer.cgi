#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser) ;
use vars qw($version);

print "Content-type: text/html\n\n" ;

####
# sa-trainer.cgi
$version = "4.04" ;
#
# sa-trainer.cgi by Ian Douglas, iandouglas.com, Copyright 2004-2016
# Some Rights Reserved under a Creative Commons "Attribution Non-commercial"
# license, http://creativecommons.org/licenses/by-nc/3.0/
# (you are free to use, copy and modify this code and redistribute it, but
# please do give credit where it's due (to me), and your redistribution must
# NOT be for for-profit purposes -- you got it from me for free, do the same
# for others please)
#
# To reach me for support, please contact me via Email at the following
# address: ian.douglas@iandouglas.com
#
# This script has always been, and will continue to be, free of charge to 
# obtain. If you'd like to show appreciation for the work that's gone into it,
# you're more than welcome to send in a PayPal donation of any amount, however
# you are under NO OBLIGATION whatsoever to donate for my time.

#### CONFIGURATION
#
# The following configuration assumes that every mailbox under domain.com
# will have an IMAP folder called "scan-ham" and "scan-spam" will be
# created and exists to hold ham and spam, respectively. These mail folders
# will need to be emptied and then compacted/purged from time to time.
# This block also assumes that cPanel is using Maildir for storing your
# email (which has long been the default). There are other configuration
# options using the commented variables like global_ham_email or 
# global_spam_email but I *highly* discourage their use since SpamAssassin
# will be FAR less accurate screening your spam/ham.

$my_domain = "domain.com" ;
$cpanel_username = "cpanelusername" ;
#$mail_format = "Mbox" ;
$mail_format = "Maildir" ;
#$global_ham_email = "globalham" ; # @ domain.com
$global_hambox = "scan-ham" ;
$check_user_Inbox_for_ham = "N" ;
#$user_hambox = "scan-ham" ;
#$global_spam_email = "global-spam" ; # @ domain.com
$check_user_spamboxes_for_spam = "N" ;
#$user_spambox = "scan-spam" ;
$global_spambox = "scan-spam" ;

#### CONFIGURATION IS COMPLETE!

############################################
# NOTHING SHOULD NEED TO CHANGE BELOW THIS LINE
# Bear in mind that modifications to this script will result in a longer time 
# assisting you in solving any related problems you might encounter along the 
# way. If I ask you for a copy of your script for support purposes (which will 
# pretty much always be free of charge), please DO send me a complete copy of 
# your script including any changes or modifications

# HTML
print <<__EOT__;
<html>
<head>
<title>sa-trainer by iandouglas.com</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css">
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap-theme.min.css">
<script src="https://code.jquery.com/jquery.js"></script>
<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.2/js/bootstrap.min.js"></script>

<!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
  <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
<![endif]-->
<style>
.linkonly {
  margin-top: 1px;
}
.skipnav {
  padding-top: 50px;
}
.bottomblock {
	position: absolute;
	bottom: 10px;
	width: 740px;
}
</style>
<body>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-142829-30', 'iandouglas.com');
  ga('send', 'pageview');

</script>

<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">sa-trainer $version</a>
    </div>
    <div class="collapse navbar-collapse">
      <ul class="nav navbar-nav">
        <li class="linkonly">
					<a href="http://www.iandouglas.com/spamassassin-trainer">
						<span class="glyphicon glyphicon-list-alt"></span>
						Documentation
					</a>
				</li>
        <li class="linkonly">
					<a href="http://www.iandouglas.com/sa-trainer/index.php">
						<span class="glyphicon glyphicon-wrench"></span>
						Important News about my SpamAssassin Trainer!
					</a>
				</li>
      </ul>
    </div>
  </div>
</div>

<div class="container skipnav">
    <div class="starter-template">
      <h1>SpamAssassin Trainer</h1>
      <div style="width:100%; background: #F7FCC7; border: 1px #D67200 solid; margin-bottom: 10px;">
<strong>DEPRECATION NOTICE:</strong> As of March 1st, 2016, I will no longer be supporting this SpamAssassin trainer script. I will maintain bug fixes at a <a href="https://github.com/iandouglas/spamassassin-trainer">GitHub repo I set up</a> a long time ago for the script, but I will no longer be supporting users who choose to download and use the script. I've been helping folks battle spam using this script in one form or another since early 2003, and it's time to focus on other things. I truly appreciate the support of everyone who has downloaded sa-trainer over the years.
      </div>
    </div>

	<div class="container bottomblock">
		<div class="starter-template">
		<p>sa-trainer.cgi version $version by Ian Douglas, iandouglas.com, Copyright 2004-2016<br />
		Some Rights Reserved under a <a href="http://creativecommons.org/licenses/by-nc/3.0/">Creative Commons "Attribution Non-commercial" license</a><br />
		</div>
	</div>

__EOT__



# sanity checks
$continue = 1 ;
$error_msg = '' ;

if ($cpanel_username eq 'myaccount' || !$cpanel_username) {
	$continue = 0 ;
	$error_msg = 'You need to properly configure $cpanel_username within the script, or the script will not operate' ;
}
if ($my_domain eq 'mydomain.com' || !$my_domain) {
	$continue = 0 ;
	$error_msg = 'You need to properly configure $my_domain within the script, or the script will not operate' ;
}
if (!$path_to_salearn) {
	$salearn = `which sa-learn` ;
	chop($salearn) ;
}
if (!$path_to_salearn) {
    $path_to_salearn = '/usr/local/cpanel/3rdparty/bin/sa-learn';
	$salearn = $path_to_salearn ;
	if ( ! -e "$salearn") {
		$continue = 0 ;
		$error_msg = 'The setting you enabled for $path_to_salearn is invalid ('.$path_to_salearn.' was not found)' ;
	}
}
# detect base mail path
$basepath = "/home/$cpanel_username" ;
$basemailpath = '' ;
if ($continue && ( -e "$basepath/mail" ) ) {
	$basemailpath = "$basepath/mail" ;
} elsif ($continue && ( ! -e "$basepath/mail" ) ) {
	if ($base_mail_folder) {
		$base_mail_folder =~ s/\///g ;
		if ( -e "$basepath/$base_mail_folder" ) {
			$basepath = "$basepath/$base_mail_folder" ;
		} else {
			$basemailpath = '' ;
			$continue = 0 ;
			$error_msg = 'The value you specified in $base_mail_folder does not exist as part of '.$basepath.'/'.$base_mail_folder.'/  Please check your configuration within the script and try again' ;
		}
	} else {
		$continue = 0 ;
		$error_msg = 'Your base mail folder could not be found. Please configure the $base_mail_folder variable within the script.' ;
	}
} 
# autodetect mail format here, and set mail_format appropriately
if (!$mail_format && ( -d "$basemailpath/cur/" || -d "$basemailpath/.spam/cur/" )) {
	print '<p>Autodetected mail storage as Maildir; you could speed up this script slightly if you configure $mail_format in the script to "Maildir"</p>' ;
	$mail_format = "Maildir" ;
}
if (!$mail_format && ( -f "$basemailpath/spam" || -f "$basemailpath/inbox" || -f "$basemailpath/Inbox" || -f "$basemailpath/INBOX")) {
	print '<p>Autodetected mail storage as Mbox; you could speed up this script slightly if you configure $mail_format in the script to "Mbox"</p>' ;
	$mail_format = "Mbox" ;
}
if ($continue && !$mail_format) {
	$error_msg = 'The script was unable to detect your Email storage type (Mbox or Maildir). Please contact your hosting provider to determine which it is, and configure the $mail_format variable within the script manually.' ;
	$continue = 0 ;
} 
if ($continue && !$salearn) {
	$error_msg = 'The script could not autodetect where the SpamAssassin training application is on your server, please configure the $path_to_salearn variable within the script' ;
	$continue = 0 ;
}
# configure domain list for scanning
@domains = () ;
push (@domains, $my_domain) ;
foreach $addon_domain (@addon_domain_list) {
	push (@domains, $addon_domain) ;
}

if ($continue) { # sanity checks on global spamboxes and user spamboxes
	if ($global_spam_email && $global_spambox) {
		$error_msg = 'You cannot enable both $global_spam_email <u>and</u> $global_spambox, you must choose one or the other' ;
		$continue = 0 ;
	} elsif ($global_spam_email && lc($check_user_spamboxes_for_spam) eq 'y') {
		$error_msg = 'You cannot enable $global_spam_email <u>and</u> set $check_user_spamboxes_for_spam to "Y", you must choose one or the other' ;
		$continue = 0 ;
	} elsif ($global_spambox && lc($check_user_spamboxes_for_spam) eq 'y') {
		$error_msg = 'You cannot enable $global_spambox <u>and</u> set $check_user_spamboxes_for_spam to "Y", you must choose one or the other' ;
		$continue = 0 ;
	} elsif (!$global_spam_email && !$global_spambox && !$check_user_spamboxes_for_spam) {
		$error_msg = 'You cannot disable $global_spam_email <u>and</u> $global_spambox <u>and</u> $check_user_spamboxes_for_spam, you must choose one of the three for scanning spam messages' ;
		$continue = 0 ;
	}
} 
if ($continue) { # sanity checks on global hamboxes and user inboxes
	if ($global_ham_email && $global_hambox) {
		$error_msg = 'You cannot enable both $global_ham_email <u>and</u> $global_hambox, you must choose one or the other' ;
		$continue = 0 ;
	} elsif ($global_ham_email && lc($check_user_Inbox_for_ham) eq 'y') {
		$error_msg = 'You cannot enable $global_ham_email <u>and</u> set $check_user_Inbox_for_ham to "Y", you must choose one or the other' ;
		$continue = 0 ;
	} elsif ($global_hambox && lc($check_user_Inbox_for_ham) eq 'y') {
		$error_msg = 'You cannot enable $global_hambox <u>and</u> set $check_user_Inbox_for_ham to "Y", you must choose one or the other' ;
		$continue = 0 ;
	} elsif (!$global_ham_email && !$global_hambox && !$check_user_Inbox_for_ham) {
		$error_msg = 'You cannot disable $global_ham_email <u>and</u> $global_hambox <u>and</u> $check_user_Inbox_for_ham, you must choose one of the three for scanning non-spam messages' ;
		$continue = 0 ;
	}
} 

$sa_config = "$basepath/.spamassassin/user_prefs" ;
if ($continue && ( ! -e "$sa_config" ) ) {
	$continue = 0 ;
	$error_msg = 'The script could not find your SpamAssassin user_prefs file as '.$basepath.'/.spamassassin/user_prefs, please make sure SpamAssassin is enabled within your CPanel interface and try again' ;
}

if (!$continue) {
	print '<p style="color:#F00">ERROR: '.$error_msg.'. Execution cannot continue until this is fixed</p>' ;
}
# sanity checks
else { # sanity check passed
	$| ;
	$global_scanspam = 0 ;
	$global_scanham = 0 ;
	if ($global_spambox) {
		print "<p>Checking Global Spambox for SPAM messages:<br />" ;
		$global_scanspam++ ;
		$this_users_spambox = '' ;
		if ($mail_format eq "Maildir") {
			if ($global_spambox =~ /\// && ( -e "$basemailpath/$global_spambox/cur" )) {
				$this_users_spambox = "$basemailpath/$global_spambox" ;
			} elsif ( -e "$basemailpath/.$global_spambox/cur" ) {
				$this_users_spambox = "$basemailpath/.$global_spambox" ;
			}
		} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$global_spambox" )) {
			$this_users_spambox = "$basemailpath/$global_spambox" ;
		}
		if ($this_users_spambox) {
			&check_spam("$this_users_spambox",$sa_config,$mail_format) ;
		} else {
			print '<p>WARNING: Global spam mailbox ('."$basemailpath/$global_spambox".') could not be found, skipping global SPAM scan</p>' ;
		}
	
	} elsif ($global_spam_email) {
		print "<p>Checking Global Email-based Spambox for SPAM messages:<br />" ;
		$global_scanspam++ ;
		$this_users_spambox = '' ;
		if ($mail_format eq "Maildir" && ( -e "$basemailpath/$my_domain/$global_spam_email/cur" )) {
			$this_users_spambox = "$basemailpath/$my_domain/$global_spam_email" ;
		} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_spam_email/inbox" )) {
			$this_users_spambox = "$basemailpath/$my_domain/$global_spam_email/inbox" ;
		} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_spam_email/Inbox" )) {
			$this_users_spambox = "$basemailpath/$my_domain/$global_spam_email/Inbox" ;
		} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_spam_email/INBOX" )) {
			$this_users_spambox = "$basemailpath/$my_domain/$global_spam_email/INBOX" ;
		}
		if ($this_users_spambox) {
			&check_spam("$this_users_spambox",$sa_config,$mail_format,1) ;
		} else {
			print '<p>WARNING: Global spam Email mailbox ('."$basemailpath/$my_domain/$global_spambox".') could not be found, skipping '.$username.'\'s SPAM scan</p>' ;
		}
	} 
	if ($global_ham_email || $global_hambox) {
		# flag it so the individual ham boxes will be skipped, but we always scan ham last anyway
		$global_scanham = 1 ;
	}
	# we'll only scan individual accounts if we aren't scanning global spam or ham
	if (!$global_scanspam || !$global_scanham) {
		foreach $domain (@domains) {
			print '<p><b>Training SpamAssassin for '.$domain.':</b></p>' ;
			# fetch email accounts for $domain
			my @logins ;
			opendir(DH,"$basemailpath/$domain") ;
			while (my $file = readdir(DH)) {
				if (substr($file,0,1) ne ".") {
					if ( -d "$basemailpath/$domain/$file" ) {
						push (@logins,$file) ;
					}
				}
			}
			closedir(DH) ;
			
			foreach my $username (sort @logins) {
				if (!$global_scanspam) {
					if (lc($check_user_spamboxes_for_spam) eq 'y') {
						$this_users_spambox = '' ;
						if ($mail_format eq "Maildir" && ( -e "$basemailpath/$domain/$username/.$user_spambox/cur" )) {
							$this_users_spambox = "$basemailpath/$domain/$username/.$user_spambox" ;
						} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$domain/$username/$user_spambox" )) {
							$this_users_spambox = "$basemailpath/$domain/$username/$user_spambox" ;
						} elsif ($mail_format eq "Mbox" && ( ! -e "$basemailpath/$domain/$username/$user_spambox" )) {
# if the user's Mbox spambox doesn't exist, let's create it here
# we can only do this for mbox format; maildir format is FAR more complex
# so obviously we'll scan 0 messages for this user, let's tell the person running the script
							print 'WARNING: '."$basemailpath/$domain/$username/$user_spambox".' did not exist; attempting to create it; scanner will say it learned from 0 messages if successful or produce another warning if unsuccessful<br />' ;
							if ( -e "$basemailpath/$domain/$username/$user_spambox" ) {
								`touch "$basemailpath/$domain/$username/$user_spambox"` ;
								$this_users_spambox = "$basemailpath/$domain/$username/$user_spambox" ;
							}
						}
						if ($this_users_spambox) {
							&check_spam("$this_users_spambox",$sa_config,$mail_format) ;
						} else {
							print 'WARNING: Could not find spambox for '.$username.'@'.$domain.', cannot scan SPAM<br />' ;
						}
					} 
				}
				if (!$global_scanham) {
				if (lc($check_user_Inbox_for_ham) eq 'n') {
					$this_users_hambox = '' ;
					if ($mail_format eq "Maildir" && ( -e "$basemailpath/$domain/$username/.$user_hambox/cur" )) {
						$this_users_hambox = "$basemailpath/$domain/$username/.$user_hambox" ;
					} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$domain/$username/$user_hambox" )) {
						$this_users_hambox = "$basemailpath/$domain/$username/$user_hambox" ;
					} elsif ($mail_format eq "Mbox" && ( ! -e "$basemailpath/$domain/$username/$user_hambox" )) {
# if the user's Mbox hambox doesn't exist, let's create it here
# we can only do this for mbox format; maildir format is FAR more complex
# so obviously we'll scan 0 messages for this user, let's tell the person running the script
						print 'WARNING: '."$basemailpath/$domain/$username/$user_hambox".' did not exist; attempting to create it; scanner will say it learned from 0 messages if successful or produce another warning if unsuccessful<br />' ;
						if ( -e "$basemailpath/$domain/$username/$user_hambox" ) {
							`touch "$basemailpath/$domain/$username/$user_hambox"` ;
							$this_users_hambox = "$basemailpath/$domain/$username/$user_hambox" ;
						}
					}
					if ($this_users_hambox) {
						&check_ham("$this_users_hambox",$sa_config,$mail_format) ;
					} else {
						print 'WARNING: Could not find hambox for '.$username.'@'.$domain.', cannot scan HAM<br />' ;
					}

				} elsif (lc($check_user_Inbox_for_ham) eq 'y') {
					$this_users_hambox = '' ;
					if ($mail_format eq "Maildir" && ( -e "$basemailpath/$domain/$username/cur" )) {
						$this_users_hambox = "$basemailpath/$domain/$username" ;
					} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$domain/$username/inbox" )) {
						$this_users_hambox = "$basemailpath/$domain/$username/inbox" ;
					} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$domain/$username/Inbox" )) {
						$this_users_hambox = "$basemailpath/$domain/$username/Inbox" ;
					} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$domain/$username/INBOX" )) {
						$this_users_hambox = "$basemailpath/$domain/$username/INBOX" ;
					}
					if ($this_users_hambox) {
						$result = &check_ham("$this_users_hambox",$sa_config,$mail_format) ;
					} else {
						print 'WARNING: Could not autodetect Inbox for '.$username.'@'.$domain.', cannot scan HAM<br />' ;
					}
				} 
				}
			}
		}
	}
	if ($global_scanham) {
		if ($global_ham_email) {
			print "<p>Checking Global Email-based Hambox for HAM messages:<br />" ;
			$global_scanham++ ;
			$this_users_hambox = '' ;
			if ($mail_format eq "Maildir" && ( -e "$basemailpath/$my_domain/$global_ham_email/cur" )) {
				$this_users_hambox = "$basemailpath/$my_domain/$global_ham_email" ;
			} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_ham_email/inbox" )) {
				$this_users_hambox = "$basemailpath/$my_domain/$global_ham_email/inbox" ;
			} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_ham_email/Inbox" )) {
				$this_users_hambox = "$basemailpath/$my_domain/$global_ham_email/Inbox" ;
			} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$my_domain/$global_ham_email/INBOX" )) {
				$this_users_hambox = "$basemailpath/$my_domain/$global_ham_email/INBOX" ;
			}
			if ($this_users_hambox) {
				&check_ham("$this_users_hambox",$sa_config,$mail_format,1) ;
			} else {
				print '<p>WARNING: Global ham Email mailbox ('."$basemailpath/$my_domain/$global_hambox".') could not be found, skipping '.$username.'\'s HAM scan</p>' ;
			} 
		} elsif ($global_hambox) {
			print "<p>Checking Global Hambox for HAM messages:<br />" ;
			$global_scanham++ ;
			$this_users_hambox = '' ;
			if ($mail_format eq "Maildir") {
				if ($global_hambox =~ /\// && ( -e "$basemailpath/$global_hambox/cur" )) {
					$this_users_hambox = "$basemailpath/$global_hambox" ;
				} elsif ( -e "$basemailpath/.$global_hambox/cur" ) {
					$this_users_hambox = "$basemailpath/.$global_hambox" ;
				}
			} elsif ($mail_format eq "Mbox" && ( -e "$basemailpath/$global_hambox" )) {
				$this_users_hambox = "$basemailpath/$global_hambox" ;
			}
			if ($this_users_hambox) {
				&check_ham("$this_users_hambox",$sa_config,$mail_format) ;
			} else {
				print '<p>WARNING: Global ham mailbox ('."$basemailpath/$global_hambox".') could not be found, skipping '.$username.'\'s HAM scan</p>' ;
			}
		}	
	}
# dump magic bits, display information for the users
#
	$result = `$salearn --dump magic` ;
	#print "<pre>".$result."</pre>" ;
#0.000          0          3          0  non-token data: bayes db version
#0.000          0      87807          0  non-token data: nspam
#0.000          0      49456          0  non-token data: nham
#0.000          0     129447          0  non-token data: ntokens
#0.000          0 1174326929          0  non-token data: oldest atime
#0.000          0 1175412433          0  non-token data: newest atime
#0.000          0 1175412895          0  non-token data: last journal sync atime
#0.000          0 1175378065          0  non-token data: last expiry atime
#0.000          0     691200          0  non-token data: last expire atime delta
#0.000          0      32203          0  non-token data: last expire reduction count
	print "<p>" ;
	@bits = split(/\n/, $result) ;
	$nham = &get_bit("nham",@bits) ;
	$nspam = &get_bit("nspam",@bits) ;
	$atime = &get_bit("oldest atime",@bits) ;
	($junk,$junk,$atime,$junk) = split (/ /,$atime) ;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($atime) ;
	$atime = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$mday,$hour,$min,$sec) ;
	$ntime = &get_bit("newest atime",@bits) ;
	($junk,$junk,$ntime,$junk) = split (/ /,$ntime) ;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($ntime) ;
	$ntime = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$mday,$hour,$min,$sec) ;
	$xtime = &get_bit("last expiry atime",@bits) ;
	($junk,$junk,$xtime,$junk) = split (/ /,$xtime) ;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($xtime) ;
	$xtime = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$mday,$hour,$min,$sec) ;
	print "Number of HAM messages scanned over time: $nham<br />" ;
	print "Number of SPAM messages scanned over time: $nspam<br />" ;
	#print "Oldest 'atime' element in bayesian database: $atime<br />" ;
	#print "Newest 'atime' element in bayesian database: $ntime<br />" ;
	#print "Last token expiry 'atime' in bayesian database: $xtime<br />" ;
# print out this information into something meaningful

	print '<p><a href="/cgi-bin/'.$0.'">re-scan mailboxes</a><br />' ;
} 

sub check_spam
{
	my ($spambox,$saconfig,$mailformat) = @_ ;
	if ($mailformat eq 'Maildir' && ( -e "$spambox/cur" )) {
		print "Checking $spambox/cur/ to learn SPAM:\n" ;
		$cmd = "$salearn -p $saconfig --spam $spambox/cur" ;
	} elsif ($mailformat eq 'Mbox' && ( -e "$spambox" )) {
		print "Checking $spambox to learn SPAM:\n" ;
		$cmd = "$salearn -p $saconfig --spam --mbox $spambox" ;
	}
	print `$cmd`."<br />" ;
} 
sub check_ham
{
	my ($hambox,$saconfig,$mailformat,$useignores) = @_ ;

	if ($mailformat eq 'Maildir' && ( -e "$hambox/cur" )) {
		print "Checking $hambox/cur/ to learn HAM:\n" ;
		$cmd = "$salearn -p $saconfig ".($useignores == 1 ? "--use-ignores" : "")." --ham $hambox/cur" ;
	} elsif ($mailformat eq 'Mbox' && ( -e "$hambox" )) {
		print "Checking $hambox to learn HAM:\n" ;
		$cmd = "$salearn -p $saconfig ".($useignores == 1 ? "--use-ignores" : "")." --mbox --ham $hambox" ;
	}
	print `$cmd`."<br />" ;
} 
sub get_bit
{
	my($pattern,@bits) = @_ ;

	@matches = grep(/$pattern/, @bits) ;
	$piece = $matches[0] ;
	$piece =~ s/\t/ /g ;
	while ($piece =~ /  /) {
		$piece =~ s/  / /g ;
	}
	($junk,$junk,$piece,$junk) = split (/ /,$piece) ;
	return $piece ;
} 
# eof ]]]

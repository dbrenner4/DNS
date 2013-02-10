#!/usr/bin/perl
#this script is fucntionally complete but requires commenting (it is quite simple)
#this is a test comment

use warnings;
use strict;
use Getopt::Long;

my $opt_backup;
my $opt_dir;
my $help;

GetOptions( 
	'backup' => \$opt_backup,
	'dir=s' => \$opt_dir,
	'help' => \$help,
);

if ($help) {
	print "\nUsage: %perl zonfile_repair.pl FILES [-d FOLDER|--dir FOLDER |-b|-backup]\n\n" .
		"\tOptions:\n" .
		"\t-h, --help\tShow this help message and exit\n" .
		"\t-b, --backup\tCreate a backup of files before processing, defaults to /BACKUP\n" .
		"\t-d, --dir\tDefines the folder where backups should be placed (implies -b).\n\n";
	exit;
}

if ($opt_backup) {
	$opt_dir = 'BACKUP' unless ($opt_dir);	#define a default value for $opt_dir if it doesnt exist
}
else {
	$opt_backup = 1 if ($opt_dir);	#Defining backup directory implies backup
}


if ($opt_backup) {
	unless (-d $opt_dir) {
		mkdir $opt_dir;
	}
	$^I = "$opt_dir/*.bak";
}
else {
	$^I = '';
}

while ( <> ) {

	my $line = $_;
	chomp $line;
	$line =~ s/\r$//;        #Remove possible windows style newlines

	if ( $line =~ /\tCNAME\t|\tMX\t|\tSRV\t/ ) {
		$line =~ s/\.*$/\./ unless $line =~ /\@$/;
	}

	if ($line =~ /\tSRV\t/ ) {
		$line =~ s/\.@//;
	}

	print $line;
	print "\n";

}

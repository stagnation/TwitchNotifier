Fork changes
============
added two quick and dirty output options for listing online channels

-l to print the url of an online channel, useful for piping to livestreamer or mpv, I personally use this with my streampy script.

-T to print the title of a broadcast, is run in a rudimentary shell script which takes forever. Fixing this with a proper webparsers would be nice

example call:

``$ <twitchnotifier> -c <user> -nl -T``
``$ ~/bin/gits/TwitchNotifier/twitchnotifier -c 1b59d9bd844d438daed1 -nl -T``

Original readme
===============


# TwitchNotifier
A simple python application that sits in the background and notifies you when some channel you follow comes up online or goes offline.

Optionally it can only check for offline/online channels once and exit using options -n/--online or -f/--offline. Also, if you pass -u/--user USER then TwitchNotifier will only check the status of USER and exit. Atleast -c/--nick or -u/--user has to be passed. If both are then -u/--user takes precendence. 

Uses twitch v2 api. 

# Usage
| Command                          | Explanation                                       |
| -------------------------------- | ------------------------------------------------- |
| twitchnotifier -u nadeshot       | Check if nadeshot is online                       |
| twitchnotifier -c Xangold        | Watch followed channels of Xangold                |
| twitchnotifier -c Xangold -n     | Check for online channels followed by Xangold     |
| twitchnotifier -h                | Show help message                                 |

# Requirements
| Name            | Version   |
| --------------- | --------- |
| python-requests | >=2.5.1   |
| libnotify       | >=0.7.6   |
| python-gobject  | >= 3.14.0 |
| python          | >= 3.4.2  |

# Options
| Option         | Explanation                     |
| -------------- | ------------------------------- |
| -h/--help      | Print help message              |
| -i/--interval  | Interval between checks         |
| -n/--online    | Only check for online channels  |
| -f/--offline   | Only check for offline channels |
| -v/--verbose   | Enable verbose output           |
| -u/--user      | Check status of user            |
| -c/--nick      | Watch NICK followed channels    |

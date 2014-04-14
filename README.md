KeybardSpellCheck
=================

A Sublime Text 2/3 plugin that allows you to spell check the word under the cursor from the keyboard (vi style). 
If the ```use_google``` setting is set to true, Google's best guess for what you meant will also be displayed as the first option.

This package is designed to work in conjunction with Sublime's built in spell check. Thus to utilize this package to its fullest, ```"spell_check": true``` should be in your ```Preferences.sublime-settings``` file.


Usage 
-----
Press ```control+alt+k``` (or ```z=``` in command mode) to display spelling suggestions. 
Use ```control+alt+[``` and ```control+alt+]```  (or ```[s``` and ```]s``` in command mode) to step through spelling errors.

When selecting a replacement word from the spelling suggestions fuzzy search is being utilized, so typing the number or some part of the word will select 
the corresponding replacement. 

Installation
------------

  + Package Control - First install Package Control from https://sublime.wbond.net/installation then search for the KeybardSpellCheck package. 
  + From Source - Clone the repo to your Sublime Text packages folder.

  This package requires the enchant spell checking package. On Mac this can be installed using ```brew install enchant```. 
  For windows there is an executable installer (see http://www.abisource.com/projects/enchant/). Most distributions of Linux come with enchant installed by default. 


Credits
-------
 Credit for the keyboard triggered code goes to Alex Naspo. Much of this work is almost an exact copy of what he has done. 
 https://github.com/alexnaspo/sublime-spell-check/

 Credit for interfacing with Google for spelling suggestions goes to Noah Code. Again, much of his code was used in developing this. 
 https://github.com/noahcoad/google-spell-check
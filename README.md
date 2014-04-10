KeybardSpellCheck
=================

A Sublime Text 3 plugin that allows you to spell check the word under the cursor from the keyboard (vi style). Press ```control+alt+k``` or ```z=``` in command mode to display spelling suggestions. Use ```[s``` and ```]s``` to step through spelling errors in command mode. 

If the ```use_google``` setting is set to true, Google's best guess for what you meant will also be displayed as the [0]G option.


Installation
------------

  + Package Control - Pull request sent and waiting for confirmation. Will update README.
  + From Source - Clone the repo to your Sublime Text packages folder.

  This package requires the enchant spell checking package. On Mac this can be installed using ```brew install enchant```. 
  For windows there is an executable installer. I have no information on Linux installation at this time. 


Credits
-------
 Credit for the keyboard triggered code goes to Alex Naspo. Much of this work is almost an exact copy of what he has done. 
 https://github.com/alexnaspo/sublime-spell-check/

 Credit for interfacing with Google for spelling suggestions goes to Noah Code. Again, much of his code was used in developing this. 
 https://github.com/noahcoad/google-spell-check
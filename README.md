

SuperMemo is a cool Windows software that I haven't managed to get working with Wine.
 Additionally, I want to be able to access the data from iOS/Android, so decided it'd be easier to get working with Anki, which supports a lot of platforms.
 The export feature of SuperMemo is pretty closed so I just wrote `supermemo2anki` to change to Anki-friendly format -- specifically for cloze cards. 


##Usage:##

SuperMemo's backup format is a folder like:

(((Backup of my_collection created on 2018-03-28 19-34-30)))

with a bunch of sub-folders.

so just pass the top level directory to supermemo2anki:

`python2.7 supermemo2anki path/to/bkup`

then import the resulting file (`anki_cards_*.txt`) into Anki. If you leave the exported file in the cwd, the old cards
won't be reimported the next time you run this tool.

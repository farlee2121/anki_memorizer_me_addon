# anki_memorizer_me_addon
Use the [memorizer.me](https://memorizer.me/) approach with anki cards.


The plugin does 2 things:
- Add a note type that generates cards for each of the memorizer.me stages for the given text
- Add template filters that mimic the way memorizer.me partially removes text


## Card type

The `Memorizer` card type has several fields, but only two might be set by the user, `OriginalText` and `Title`.
The wordstarts and linestarts fields are auto-generated when the user clicks aways from the OriginalText or Title fields.

WARNING: Anki's mobile apps [don't support addons](https://forums.ankiweb.net/t/how-to-install-add-ons-in-android-13/29489), so the addon will only
generate the computed fields on desktop. Once generated, all the fields/cards should sync to mobile devices as expected.

Three cards will be created based on OriginalText and title
- Original Text as the prompt, the title as the answer
- The starts of the words as the prompt, and title + original text as the answer
- The starts of each line as the prompt, and title + original text as the answer

So if you have a title of "Example Title Here" and this OriginalText
```
This is line one
Another line follows
Third line goes a bit longer
```

You'd get three cards, like these

```
*Card Front*
This is line one
Another line follows
Third line goes a bit longer
___________________________
*Card Back*
Example Title Here
```

```
*Card Front*
E_____ T____ H___

T___ i_ l___ o__
A______ l___ f______
T____ l___ g___ a b__ l_____
___________________________
*Card Back*
Example Title Here

This is line one
Another line follows
Third line goes a bit longer
```

```
*Card Front*
Example Title

This is
Another line
Third line
___________________________
*Card Back*
Example Title Here

This is line one
Another line follows
Third line goes a bit longer
```



## Template Filters

WARNING: Anki's mobile apps [don't support addons](https://forums.ankiweb.net/t/how-to-install-add-ons-in-android-13/29489) so these filters will not work on mobile.
The cards will still sync correctly to mobile because the plugin generates fields with the transformed text.

Template filters allow behavior in card templates.
The two filters this plugin adds are `memorizer-wordstarts` and `memorizer-linestarts`

Suppose you've got a note with field `fieldname` containing the text

```
This is line one
Another line follows
```

Supposing you've made a card template using `memorizer-wordstarts`, like this one
```
{{memorizer-wordstarts:fieldname}}
```

The output resulting card would show this text

```
T___ i_ l___ o__
A______ l___ f______
```

Similarly, a template using `memorizer-linestarts`

```
{{memorizer-linestarts:fieldname}}
```

Would have the output

```
This is
Another line
```

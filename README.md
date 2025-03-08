# anki_memorizer_me_addon
Use the [memorizer.me](https://memorizer.me/) approach with anki cards.


The plugin does 2 things:
- Add a note type that generates cards for each of the memorizer.me stages for the given text
- Add template filters that mimic the way memorizer.me partially removes text


## Card type

The `Memorizer` card type has only one field: `OriginalText`.


Three cards will be created based on OriginalText
- Just the original text
- The starts of the words as the prompt, and the original text as the answer
- The starts of each line as the prompt, and the original text as the answer

So if you have this OriginalText
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

```

```
*Card Front*
T___ i_ l___ o__
A______ l___ f______
T____ l___ g___ a b__ l_____
___________________________
*Card Back*
This is line one
Another line follows
Third line goes a bit longer
```

```
*Card Front*
T___ i_ l___ o__
A______ l___ f______
T____ l___ g___ a b__ l_____
___________________________
*Card Back*
This is
Another line
Third line
```

## Template Filters

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
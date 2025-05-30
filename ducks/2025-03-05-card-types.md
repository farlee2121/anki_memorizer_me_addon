https://addon-docs.ankiweb.net/hooks-and-filters.html


"The Japanese Support add-on uses this hook to automatically generate one field from another"
I could use focus lost to fill in fields for the modified texts.

This seems like it might be the easiest way. It doesn't look like the card templates allow any programmatic transformation.
It seems to just be token replacement

Example: [Here's the docs on how to read and write notes, cards, and card types](https://addon-docs.ankiweb.net/the-anki-module.html#readingwriting-objects)
- `col.models` is note types 

Example: [Here's a plugin adding a note/card type](https://github.com/glutanimate/cloze-overlapper/blob/master/src/cloze_overlapper/template.py#L377)

OPT: [Reviewer Javascript](https://addon-docs.ankiweb.net/reviewer-javascript.html)
- allows html transforms before showing a card to the user
- i could try to find and modify the text in the html, but that seems hacky and like it'd lead difficulty maintaining the collection


Q: How do I add multiple cards per note?
- [here's how to do it in the UI](https://www.youtube.com/watch?v=vIGF_EoGfHk)



TASK: look in anki repository how Basic (And reversed card) is set up
- I think `model.new`/`model.add` can be assigned multiple `model.newTemplate`/`model.addTemplate` and that's how it works
- The Basic (optional reversed card) appears to have a conditional in the template itself `{{#Add Reverse}}{{Back}}{{/Add Reverse}}`
  - Add Reverse is a field. It appears that if anything is in this field, the reverse card is generated, otherwise it isn't. This appears to be because the template conditional, but i'm not 100%
  - doesn't help me either way
  - [I was right](https://docs.ankiweb.net/templates/generation.html#reverse-cards)
  - [here's how conditions work in general](https://docs.ankiweb.net/templates/generation.html#conditional-replacement) 
- `{{FrontSide}}` appears to be a built-in variable for the whole front of the card
- There do seem to be some modifiers available in the templating, like `cloze:`
- !! found some [card template docs](https://docs.ankiweb.net/templates/fields.html)

template learnings
- fields are case sensitive
- they have built-in text to speach!
- [special fields](https://docs.ankiweb.net/templates/fields.html#special-fields)
- [conditions](https://docs.ankiweb.net/templates/generation.html#conditional-replacement)

Q: what do the call template actions like tts: and sound:?
- [Media manager appears to be responsible for sound:](https://github.com/ankitects/anki/blob/63c2a09ef6760890c03be4bd83f613c03c512d1f/pylib/anki/media.py#L33)
- [tts:, cloze:, and others are in template_filters](https://github.com/ankitects/anki/blob/63c2a09ef6760890c03be4bd83f613c03c512d1f/rslib/src/template_filters.rs#L204)

Q: Can we create custom template filters?
- A: yes, and there's [an official example](https://github.com/ankitects/anki-addons/blob/main/demos/field_filter/__init__.py)

Q: why is my filter not returning anything

Tasks
- [x] Demonstrate a new note type
- [x] demonstrate multiple cards per note
- [x] figure out how to auto-fill the transformed versions of the text (probably via the field focus method or an in-template transform)
- [x] make sure I can update text and the transformed text updates accordingly
- [x] fix wordstart regex to leave punctuation alone
- [x] Break fork relationship? I don't think I'm actually going to use any of the code from the repo I forked
  - [x] delete unused code
- [x] make sure that the plugin updates the models/templates if they already exist


Q: should I add a separate field for the verse number / or "title"?
- I'm realizing that there isn't easy initial context for what verse I'm working with. I have to guess it from the partial I have. My focus is memorizing the text, not the verse numbers. And if I want to memorize the verse numbers then i should probably add a card that has the verse number as the answer to the full text

PROBLEM: I'm realizing that now I'm sorting on title, but also considering the field optional. So I don't know how anki will handle sorting...


## PROBLEM: No Addons on Mobile

Anki's mobile apps [don't support addons](https://forums.ankiweb.net/t/how-to-install-add-ons-in-android-13/29489), which means that cards which are supposed to show filtered are showing the full text.

The workaround for this is probably to follow the [japanese addon](https://addon-docs.ankiweb.net/hooks-and-filters.html#legacy-hook-handling).
Add fields for the transformed versions and generate them when the OriginalText field loses focus


## Cloze Deletion

Keegan pointed out that Memorizer is using a variation of [Cloze Deletion](https://en.wikipedia.org/wiki/Cloze_test)

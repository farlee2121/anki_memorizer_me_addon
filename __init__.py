"""
Memorizer.me inspired plugin. Easily memorize text with cloze-type cards.

The plugin does 2 things:
- add a menu button to the card browser that allows one to start an interactive dialog from the selected card
- add a memorizer.me card type that allows to easily add cards from input text
"""
import re

from aqt import mw, AnkiQt, gui_hooks
from anki.models import ModelManager, NotetypeDict, FieldDict
from aqt.qt import QTextDocument
from anki import hooks
from anki.notes import Note
from anki.template import TemplateRenderContext


class HtmlTransforms:
    @staticmethod
    def convert_to_plaintext(html_content: str) -> str:
        # Create a QTextDocument
        text_document = QTextDocument()

        # Set HTML content in the QTextDocument
        text_document.setHtml(html_content)

        # Extract plain text
        plain_text = text_document.toPlainText()

        return plain_text

    @staticmethod
    def escapeNewlinesForHtml(text: str) -> str:
        return text.replace("\n", "<br>")

class MemorizerTransforms: 
    @staticmethod
    def wordStartsOnly(text: str) -> str:
        """Replace all but the starts of words, punctuation and whitespace with underscores. I.e. This is blanked! -> T___ i_ b______!"""
        def callable(match):
            m = match[0]
            return m[0] + len(m[1:]) * '_'

        pattern_letters = r"""\w+"""
        return re.sub(pattern_letters, callable, text)

    @staticmethod
    def wordStartsOnly_ForHtml(text: str) -> str:
        """Replace all but the starts of words, punctuation and whitespace with underscores. I.e. This is blanked! -> T___ i_ b______!"""
        plaintext = HtmlTransforms.convert_to_plaintext(text)
        wordstarts = MemorizerTransforms.wordStartsOnly(plaintext)
        htmlEscaped = HtmlTransforms.escapeNewlinesForHtml(wordstarts)
        return htmlEscaped

    @staticmethod
    def lineStartsOnly(text: str) -> str:
        """Show only the first few words of every line. I.e. Line one text is this \n Line two text is that -> Line one \n Line two"""
        def callable(match):
            return match[1]

        pattern_words = r"^((\s*[\S]+){0,2}).*"
        return re.sub(pattern_words, callable, text, flags=re.MULTILINE)
    
    @staticmethod
    def lineStartsOnly_ForHtml(text: str) -> str:
        """Show only the first few words of every line. I.e. Line one text is this \n Line two text is that -> Line one \n Line two"""
        plaintext = HtmlTransforms.convert_to_plaintext(text)
        linestarts = MemorizerTransforms.lineStartsOnly(plaintext)
        return HtmlTransforms.escapeNewlinesForHtml(linestarts)


class WordStartsFilter:
    """Adds a memorizer-wordstarts: template filter"""
    FILTER_ID = "memorizer-wordstarts"
    # called each time a custom filter is encountered
    @staticmethod
    def wordstarts_filter(
        field_text: str,
        field_name: str,
        filter_name: str,
        context: TemplateRenderContext,
    ) -> str:
        if not filter_name.lower() == WordStartsFilter.FILTER_ID:
            # not our filter, return string unchanged
            return field_text
        else:
            return MemorizerTransforms.wordStartsOnly_ForHtml(field_text)
        
class LineStartsFilter:
    """Adds a memorizer-wordstarts: template filter"""

    FILTER_ID = "memorizer-linestarts"
    # called each time a custom filter is encountered
    @staticmethod
    def linestarts_filter(
        field_text: str,
        field_name: str,
        filter_name: str,
        context: TemplateRenderContext,
    ) -> str:
        if not filter_name.lower() == LineStartsFilter.FILTER_ID:
            # not our filter, return string unchanged
            return field_text
        else:
            return MemorizerTransforms.lineStartsOnly_ForHtml(field_text)
        
class Notetype: 
    ID = "Memorizer"
    TITLE_FIELD_ID = "Title"
    FULLTEXT_FIELD_ID = "OriginalText"
    WORDSTARTS_FIELD_ID = "Wordstarts"
    LINESTARTS_FIELD_ID = "Linestarts"

    DEFAULT_STYLE = """\
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: left;
        color: black;
        background-color: white;
    }\
    """

class FulltextCard: 
    ID = "Memorizer Fulltext"
    FRONT_TEMPLATE = "{{" + Notetype.FULLTEXT_FIELD_ID + "}}"
    BACK_TEMPLATE = f"""\
        {{{{FrontSide}}}}

        <hr id=answer>

        {{{{{Notetype.TITLE_FIELD_ID}}}}}\
    """

class WordStartCard: 
    ID = "Memorizer Wordstarts"
    FRONT_TEMPLATE = "{{"+ Notetype.WORDSTARTS_FIELD_ID + "}}"
    BACK_TEMPLATE = f"""\
        {{{{FrontSide}}}}

        <hr id=answer>
        
        {{{{{Notetype.TITLE_FIELD_ID}}}}}<br />
        {{{{{Notetype.FULLTEXT_FIELD_ID}}}}}\
    """

class LineStartCard: 
    ID = "Memorizer Linestarts"
    FRONT_TEMPLATE = "{{"+ Notetype.LINESTARTS_FIELD_ID + "}}"
    BACK_TEMPLATE = f"""\
        {{{{FrontSide}}}}

        <hr id=answer>
        {{{{{Notetype.TITLE_FIELD_ID}}}}}<br />
        {{{{{Notetype.FULLTEXT_FIELD_ID}}}}}\
    """

def upsert_field(models: ModelManager, noteType: NotetypeDict, fieldName: str):
    if not (fieldName in models.field_map(noteType)):
        models.add_field(noteType, models.new_field(fieldName))

def add_card_types():
    models: ModelManager = mw.col.models

    if models.by_name(Notetype.ID):
        memorizerNoteType = models.by_name(Notetype.ID)
        memorizerNoteType['css'] = Notetype.DEFAULT_STYLE

        upsert_field(models, memorizerNoteType, Notetype.TITLE_FIELD_ID)
        upsert_field(models, memorizerNoteType, Notetype.WORDSTARTS_FIELD_ID)
        upsert_field(models, memorizerNoteType, Notetype.LINESTARTS_FIELD_ID)

        cardTemplates = memorizerNoteType['tmpls']

        fulltextCardTemplate = cardTemplates[0]
        fulltextCardTemplate['qfmt'] = FulltextCard.FRONT_TEMPLATE
        fulltextCardTemplate['afmt'] = FulltextCard.BACK_TEMPLATE

        wordstartsCardTemplate = cardTemplates[1]
        wordstartsCardTemplate['qfmt'] = WordStartCard.FRONT_TEMPLATE
        wordstartsCardTemplate['afmt'] = WordStartCard.BACK_TEMPLATE

        linestartsCardTemplate = cardTemplates[2]
        linestartsCardTemplate['qfmt'] = LineStartCard.FRONT_TEMPLATE
        linestartsCardTemplate['afmt'] = LineStartCard.BACK_TEMPLATE

        memorizerNoteType['sortf'] = 1

        models.save(memorizerNoteType)
        return memorizerNoteType
    
    else:
        memorizerNoteType : NotetypeDict = models.new(Notetype.ID)
        # Add fields:
        models.addField(memorizerNoteType, models.new_field(Notetype.FULLTEXT_FIELD_ID))
        models.add_field(memorizerNoteType, models.new_field(Notetype.TITLE_FIELD_ID))
        models.add_field(memorizerNoteType, models.new_field(Notetype.WORDSTARTS_FIELD_ID))
        models.add_field(memorizerNoteType, models.new_field(Notetype.LINESTARTS_FIELD_ID))

        # Add templates (this is all the same. It wouldn't be to hard to make them a class and have a method that aligns the registered cards with what's defined)
        fulltextCardTemplate = models.new_template(FulltextCard.ID)
        fulltextCardTemplate['qfmt'] = FulltextCard.FRONT_TEMPLATE
        fulltextCardTemplate['afmt'] = FulltextCard.BACK_TEMPLATE
        models.add_template(memorizerNoteType, fulltextCardTemplate)

        wordstartsCardTemplate = models.new_template(WordStartCard.ID)
        wordstartsCardTemplate['qfmt'] = WordStartCard.FRONT_TEMPLATE
        wordstartsCardTemplate['afmt'] = WordStartCard.BACK_TEMPLATE
        models.add_template(memorizerNoteType, wordstartsCardTemplate)

        linestartsCardTemplate = models.new_template(LineStartCard.ID)
        linestartsCardTemplate['qfmt'] = LineStartCard.FRONT_TEMPLATE
        linestartsCardTemplate['afmt'] = LineStartCard.BACK_TEMPLATE
        models.add_template(memorizerNoteType, linestartsCardTemplate)

        memorizerNoteType['css'] = Notetype.DEFAULT_STYLE
        memorizerNoteType['sortf'] = 1

        models.add(memorizerNoteType)
        
        return memorizerNoteType
    
def on_field_unfocus(changed: bool, note: Note, fieldIndex: int) -> bool:
    models = mw.col.models
    memorizerNoteType = models.by_name(Notetype.ID)
    sourceFieldName = models.field_names(memorizerNoteType)[fieldIndex]
    if(sourceFieldName in [Notetype.FULLTEXT_FIELD_ID, Notetype.TITLE_FIELD_ID]):
        srcText = note[Notetype.TITLE_FIELD_ID] +"<br />" + note[Notetype.FULLTEXT_FIELD_ID]
        note[Notetype.WORDSTARTS_FIELD_ID] = MemorizerTransforms.wordStartsOnly_ForHtml(srcText)
        note[Notetype.LINESTARTS_FIELD_ID] = MemorizerTransforms.lineStartsOnly_ForHtml(srcText)
        return True
    else:
        return False

def setup_main():
    """Registers plugin with Anki."""
    hooks.field_filter.append(WordStartsFilter.wordstarts_filter)
    hooks.field_filter.append(LineStartsFilter.linestarts_filter)
    gui_hooks.main_window_did_init.append(add_card_types)
    gui_hooks.editor_did_unfocus_field.append(on_field_unfocus)

# register plugin with hooks
setup_main()

"""
Memorizer.me inspired plugin. Easily memorize text with cloze-type cards.

The plugin does 2 things:
- add a menu button to the card browser that allows one to start an interactive dialog from the selected card
- add a memorizer.me card type that allows to easily add cards from input text
"""
import os
import re

from aqt import mw
from aqt import AnkiQt
from aqt.browser import Browser
from aqt.qt import QDialog, QVBoxLayout, Qt, QComboBox, QPushButton, QTextBrowser, QHBoxLayout, QTextDocument, QLabel
from aqt import gui_hooks

ADDON_PATH = os.path.dirname(__file__)
WINDOW_MIN_WIDTH = 500
WINDOW_MIN_HEIGHT = 600
STATES = ['full text', 'first letters of each word', 'first words of each line']

def convert_to_plaintext(html_content: str) -> str:
    # Create a QTextDocument
    text_document = QTextDocument()

    # Set HTML content in the QTextDocument
    text_document.setHtml(html_content)

    # Extract plain text
    plain_text = text_document.toPlainText()

    return plain_text


class MemorizerMeDialog(QDialog):
    """Memorizer.me plugin main window."""

    def __init__(self, parent: AnkiQt):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setMinimumWidth(WINDOW_MIN_WIDTH)
        self.setMinimumHeight(WINDOW_MIN_HEIGHT)
        self.visible = True
        self.parent = parent
        self.setupUi()
        self.note = None
        self.display_state = 0

    def setupUi(self):
        """Setup the user interface."""
        # Create widgets
        select_box = QComboBox()
        self.select_box = select_box
        button_left = QPushButton("←")
        button_right = QPushButton("→")

        state_label = QLabel("Current display state:")
        current_label = QLabel("")
        self.current_label = current_label

        text_edit = QTextBrowser()
        self.text_edit = text_edit

        # Set up button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(select_box)
        button_layout.addWidget(button_left)
        button_layout.addWidget(button_right)

        # Set up state layout
        state_layout = QHBoxLayout()
        state_layout.addWidget(state_label)
        state_layout.addWidget(current_label)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(state_layout)
        main_layout.addWidget(text_edit)

        self.setLayout(main_layout)

        # Connect signals to slots
        button_left.clicked.connect(self.move_view_left)
        button_right.clicked.connect(self.move_view_right)
        select_box.currentIndexChanged.connect(self.update_displayed_text)

    def move_view_left(self):
        """Change to previous display state."""
        self.display_state = (self.display_state - 1) % 3
        self.update_displayed_text()

    def move_view_right(self):
        """Change to next display state."""
        self.display_state = (self.display_state + 1) % 3
        self.update_displayed_text()

    def show_window(self, editor):
        """This function gets called when the browser button gets clicked."""
        self.show()

    def update_plugin_input_note(self, note):
        """This function gets called when the browser changes notes."""
        if note:
            self.note = note
            # update the select box
            self.select_box.clear()
            for (name, value) in note.items():
                self.select_box.addItem(name)

    def update_displayed_text(self):
        """This updates the text in the dialog window.
        Can get called for several reasons:
        - browser changed card
        - user clicked arrow
        - user changed field
        """
        if self.note:
            index = self.select_box.currentIndex()
            if index > -1:
                values = list(self.note.values())
                input_text = values[index]
                input_textonly = convert_to_plaintext(input_text)

                if self.display_state == 0:
                    # display full text
                    output_text = input_text
                elif self.display_state == 1:
                    # display first letters
                    def callable(match):
                        m = match[0]
                        return m[0] + len(m[1:]) * '_'

                    pattern_letters = r"""[^ ,\.!\?:;—\–\-„“”«»`’¿¡~\[\]\{\}\(\)\*&\^%‰¤\$¢£€₧¥₣₤'"\/<>#@\|\u0964\\\n]([^ \n]*)"""
                    output_text = re.sub(pattern_letters, callable, input_textonly)
                    output_text = output_text.replace("\n", "<br>")

                elif self.display_state == 2:
                    # display first words

                    def callable(match):
                        return match[1]

                    pattern_words = r"^((\s*[\S]+){0,2}).*"
                    output_text = re.sub(pattern_words, callable, input_textonly, flags=re.MULTILINE)
                    output_text = output_text.replace("\n", "<br>")

                print("%%%%%%%%% output %%%%%%%%", output_text)

                self.current_label.setText(STATES[self.display_state])
                self.text_edit.setHtml(output_text)


def on_setup_editor_buttons(buttons, editor):
    """Add a button to card browser."""
    icon = os.path.join(ADDON_PATH, 'icons', 'editor.png')

    b = editor.addButton(
        icon=icon,
        cmd="memorizer_me_button",
        func=lambda editor=editor: mw.dialog.show_window(editor),
        tip="Show memorizer.me plugin window",
        disables=False,
    )

    buttons.append(b)
    return buttons


def on_change_row(browser: Browser) -> None: 
    """Hook that gets called each time the browser changes rows."""
    note = browser.editor.note
    if note:
        mw.dialog.update_plugin_input_note(note)

def setup_main(main_window: AnkiQt):
    """Registers plugin with Anki."""
    # Add a button to card browser
    gui_hooks.editor_did_init_buttons.append(on_setup_editor_buttons)
    # If card browser changes row, updates the input data for the plugin
    gui_hooks.browser_did_change_row.append(on_change_row)


# create instance of Dialog
mw.dialog = MemorizerMeDialog(mw)

# register plugin with hooks
setup_main(mw)

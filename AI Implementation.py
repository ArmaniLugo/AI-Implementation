import language_tool_python
import tkinter as tk
import tkinter.filedialog as tkfd

# Constants for tkinter tags
spelling_error = 'spellingerror'
grammar_error = 'grammarerror'


def main():
    global unchecked_text, spellchecked_text, lang_tool
    # Establishing a connection to the language tool server
    lang_tool = language_tool_python.LanguageToolPublicAPI('en-US')

    window = tk.Tk()

    # Program description
    description = tk.Label(window,
                           text='This is a grammar and spellchecking program that is designed to fix any grammatical and spelling errors.\nPlease type in your passage or import a .txt file to check.\nSpellchecking errors will be highlighted in red and grammatical errors will be highlighted in blue.',
                           font=('Arial', 16))
    description.grid(row=0, column=0, columnspan=2, pady=20)

    # User input section
    tk.Label(window, text='Enter text to spellcheck:').grid(row=1, column=0)
    unchecked_text = tk.Text(window, width=60, height=20)
    unchecked_text.grid(row=2, column=0)
    unchecked_text.tag_configure(spelling_error, background='#BD5747', foreground='white')
    unchecked_text.tag_configure(grammar_error, background='#5159B3', foreground='white')

    # Spellchecked section (not accessible to user)
    tk.Label(window, text='Spellchecked text:').grid(row=1, column=1)
    spellchecked_text = tk.Text(window, width=60, height=20, state='disabled')
    spellchecked_text.grid(row=2, column=1)

    # Interaction buttons
    tk.Button(window, text='Spellcheck text', command=spellcheck).grid(row=3, column=0, columnspan=2)
    tk.Button(window, text='Import .txt file', command=import_file).grid(row=4, column=0)
    tk.Button(window, text='Save .txt file', command=save_file).grid(row=4, column=1)

    window.mainloop()


def import_file():
    global unchecked_text

    try:
        # Open file explorer and pick .txt file
        path = tkfd.askopenfilename(filetypes=[('Text files', '*.txt')])
        file = open(path, 'r')

        # Insert contents of file into unchecked text region
        unchecked_text.delete(1.0, tk.END)
        unchecked_text.insert(tk.INSERT, file.read())
        file.close()

        # And spellcheck the contents
        spellcheck()

    except FileNotFoundError:
        print("Error: unable to open file at given path")

    except:
        print("Error: something else went wrong")


def save_file():
    global spellchecked_text

    try:
        # Open file explorer and give name for new .txt file
        path = tkfd.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])

        # Write contents of spellchecked text region into file
        file = open(path, 'w')
        file.write(spellchecked_text.get(1.0, tk.END))
        file.close()

    except:
        print("Error: something went wrong writing to the file")


def spellcheck():
    global unchecked_text, spellchecked_text, lang_tool

    # Get contents of user input text region
    user_input = unchecked_text.get(1.0, tk.END)

    # Remove all tags from current user input text region
    unchecked_text.tag_remove(spelling_error, 1.0, tk.END)
    unchecked_text.tag_remove(grammar_error, 1.0, tk.END)

    # For each error in user input, highlight region of text that is incorrect
    for error in lang_tool.check(user_input):
        # Tkinter expects indices in format "1.0 + n chars", where n=offset
        startIdx = f'1.0 + {error.offset} chars'
        endIdx = f'1.0 + {error.offset + error.errorLength} chars'

        # Get proper tag to display based on error type
        tag = ''
        if error.ruleIssueType == 'grammar':
            tag = grammar_error
        else:
            tag = spelling_error

        # Add tag
        unchecked_text.tag_add(tag, startIdx, endIdx)

    # Spellcheck user input, insert into spellchecked text region
    spellchecked_text.configure(state='normal')
    spellchecked_text.delete(1.0, tk.END)
    spellchecked_text.insert(tk.INSERT, lang_tool.correct(user_input))
    spellchecked_text.configure(state='disabled')


if __name__ == '__main__':
    main()
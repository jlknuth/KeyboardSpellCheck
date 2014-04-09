import sublime
import sublime_plugin
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "pyenchant"))
import enchant


class SpellCheckCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        # self.view = view
        # self.selection = view.sel()
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = enchant.Dict("en_US")

    def run(self, edit):
        self.selection = self.view.sel()
        self.pos = self.view.sel()[0]
        print(self.pos.__dict__)
        self.view.run_command("expand_selection", {"to": "word"})
        phrase = self.view.substr(self.selection[0])
        if not phrase:
            return  # nothing selected
        self.suggestions = self.dictionary.suggest(phrase)
        self.index_suggestions = ['{}: '.format(ix)+s for ix, s in enumerate(self.suggestions)]

        if not self.dictionary.check(phrase):
            self.view.window().show_quick_panel(self.index_suggestions,
                                                self.on_done,
                                                sublime.MONOSPACE_FONT)
        else:
            sublime.status_message(phrase + " is spelled correctly")
            self.on_done(-1)

    def on_done(self, index):
        if (index == -1):
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(self.pos.a, self.pos.b))
            return
        self.view.run_command("insert_my_text", {"args": {'text':self.suggestions[index],
                              'posa':self.pos.a, 'posb':self.pos.b}})


class InsertMyText(sublime_plugin.TextCommand):
  def run(self, edit, args):
    self.view.replace(edit, self.view.sel()[0], args['text'])
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(args['posa'], args['posb']))



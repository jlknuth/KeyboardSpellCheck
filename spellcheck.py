import sublime
import sublime_plugin
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "pyenchant"))
import enchant
import re

if sublime.version() < '3000':
    # we are on ST2 and Python 2.X
    _ST3 = False
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import quote
else:
    _ST3 = True
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.parse import quote




class SpellCheckCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = enchant.Dict("en_US")

    def run(self, edit):
        s = sublime.load_settings("KeyboardSpellCheck.sublime-settings")
        self.selection = self.view.sel()
        self.pos = self.view.sel()[0]

        if s.get("mark_google", True):
            gstr = '   -Google-'
        else:
            gstr = ''

        if self.view.sel()[0].a == self.view.sel()[0].b:
            self.view.run_command("expand_selection", {"to": "word"})

        phrase = self.view.substr(self.selection[0])
        if not phrase:
            return  # nothing selected

        self.suggestions = self.dictionary.suggest(phrase)

        if s.get("use_google", True):
            gfix = self.correct(phrase)
        else:
            gfix = None

        if gfix is not None:
            if gfix in self.suggestions:
                self.suggestions.remove(gfix)
            self.index_suggestions = ['{0}: '.format(ix+2)+s for ix, s in enumerate(self.suggestions)]
            self.suggestions = [gfix] + self.suggestions
            self.index_suggestions = ['{0}: '.format(1)+gfix+gstr] + self.index_suggestions
        else:
            self.index_suggestions = ['{0}: '.format(ix+1)+s for ix, s in enumerate(self.suggestions)]

        if (not self.dictionary.check(phrase)) or (gfix is not None):
            self.view.window().show_quick_panel(self.index_suggestions,
                                                self.on_done,
                                                sublime.MONOSPACE_FONT)
        else:
            sublime.status_message(phrase + " is spelled correctly")
            self.on_done(-1)

    def on_done(self, index):
        if (index == -1):
            self.view.sel().clear()
            if not _ST3:
                self.view.sel().add(sublime.Region(long(self.pos.a), long(self.pos.b)))
            else:
                self.view.sel().add(sublime.Region(self.pos.a, self.pos.b))
            return
        self.view.run_command("insert_my_text", {"args": {'text':self.suggestions[index],
                              'posa':self.pos.a, 'posb':self.pos.b}})

    def correct(self, text):
        # grab html
        try:
            html = self.get_page('http://www.google.com/search?q=' + quote(text))
        except:
            print('KeyboardSpellCheck: Could not contact Google')
            return None

        # pull pieces out
        match = re.search(r'(?:Showing results for|Did you mean|Including results for)[^\0]*?<a.*?>(.*?)</a>', html)
        if match is None:
            fix = None
        else:
            fix = match.group(1)
            fix = re.sub(r'<.*?>', '', fix);

        # return result
        return fix

    def get_page(self, url):
        # the type of header affects the type of response google returns
        # for example, using the commented out header below google does not
        # include "Including results for" results and gives back a different set of results
        # than using the updated user_agent yanked from chrome's headers
        # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        headers = {'User-Agent':user_agent,}
        req = Request(url, None, headers)
        page = urlopen(req)
        html = str(page.read())
        page.close()
        return html


class InsertMyText(sublime_plugin.TextCommand):
  def run(self, edit, args):
    self.view.replace(edit, self.view.sel()[0], args['text'])
    self.view.sel().clear()
    if not _ST3:
        self.view.sel().add(sublime.Region(long(args['posa']), long(args['posb'])))
    else:
        self.view.sel().add(sublime.Region(args['posa'], args['posb']))



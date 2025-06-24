import sublime
import sublime_plugin
import re
import json
import mdpopups
import webbrowser

SCOPES = [
    "support.function.ring",
    "keyword.control.ring",
    "keyword.control.conditional.ring",
    "storage.type.ring"
]

def lang_map_settings():
    try:
        # load the settings to transfer:
        res = sublime.load_resource("Packages/Ring/tooltips/lang_map.sublime-settings")
        lang_map = sublime.decode_value(res).get("mdpopups.sublime_user_lang_map", {})

        # load user settings
        user_settings = sublime.load_settings("Preferences.sublime-settings")
        user_lang_map = user_settings.get("mdpopups.sublime_user_lang_map", {})

        if user_lang_map.get("Ring") == lang_map.get("Ring"):
            return

        # transfer the settings to the user settings
        user_lang_map.update(lang_map)
        user_settings.set("mdpopups.sublime_user_lang_map", user_lang_map)

        # save the user settings
        sublime.save_settings("Preferences.sublime-settings")
    except Exception as e:
        print("Ring plugin: Could not load lang_map settings: {}".format(e))

def plugin_loaded():
    print("Ring plugin loaded")
    global Pref
    
    class Pref:
        def load(self):
            Pref.isActive = False
            Pref.show_tooltips = settings.get("show_tooltips", True)
            
    Pref = Pref()
    settings = sublime.load_settings("Ring.sublime-settings")
        
    # Load tooltip data from json
    tooltips = sublime.load_resource("Packages/Ring/tooltips/ring.json")
    Pref.data = json.loads(tooltips)
        
    # Load CSS from external file
    Pref.css = sublime.load_resource("Packages/Ring/tooltips/style.css").replace("\r", "")
    
    Pref.load()
    lang_map_settings()
    settings.add_on_change("reload", lambda:Pref.load())

class RingListener(sublime_plugin.EventListener):
    def __init__(self):
        self.menus = []
            
    def on_selection_modified_async(self, view):
        if not hasattr(Pref, 'show_tooltips') or not Pref.show_tooltips:
            return
            
        if hasattr(Pref, 'isActive') and Pref.isActive:
            return
            
        if not any(x in view.scope_name(view.sel()[0].a) for x in SCOPES):
            return
            
        word = view.substr(view.word(view.sel()[0])).lower()
        command = Pref.data.get(word)
        if not command:
            return
            
        Pref.isActive = True
        
        global copy, menus
        
        menus = ["<body id='ring-tooltip'>"]
        menus.append("<style>{}</style>".format(Pref.css))
        
        # Header
        menus.append("<div class='header'>")
        if command.get("class"):
            menus.append("<div class='class-container'>")
            menus.append("<span>Class:</span>")
            for i, cl in enumerate(command["class"]):
                if i: menus.append(",")
                menus.append("<span class='class'> {}</span>".format(cl))
            menus.append("</div>")
                    
        # Content
        menus.append("<div class='content'>")
        if command.get("syntax"):
            name, *args = re.split("(\\W)", command["syntax"], maxsplit=1)
            menus.append("<div class='syntax-container'>")
            menus.append("<strong class='name'>{}</strong>".format(name))
            if args:
                menus.append("<var>{}</var>".format("".join(args).replace("\n", "<br>")))
            menus.append("</div>")
            
        if command.get("description"):
            menus.append("<div class='description-container'>{}</div>".format(command["description"].replace("\n", "<br>")))
        menus.append("</div>")
        
        # Example
        if command.get("example"):
            lang = mdpopups.get_language_from_view(view) or ""
            example = mdpopups.syntax_highlight(view, command["example"], language=lang)
            menus.append("<div class='example-container'>")
            menus.append("Example:")
            menus.append("<code class='example-code'>{}</code>".format(example))
            menus.append("<a class='example-copy' href='tooltip.copy'>copy</a>")
            menus.append("</div>")
            copy = command["example"]
            
        # Footer
        menus.append("<div class='footer'>")
        menus.append("<a href='https://ring-lang.net/' title='Ring Language Official Website'>Ring Website</a>")
        menus.append("<a href='https://ring-lang.net/doc1.22/' title='Ring Language Documentation'>Documentation</a>")
        menus.append("<a href='https://groups.google.com/g/ring-lang' title='Ring Language Google Group'>Group</a>")
        menus.append("</div>")
        
        menus.append("</body>")
        
        max_width, max_height = view.viewport_extent()
        max_width *= 0.90
        max_height *= 0.90
        a = view.word(view.sel()[0]).begin()
        b = view.word(view.sel()[0]).end()
        
        self.view = view
        
        view.show_popup(
            "".join(menus),
            sublime.HIDE_ON_MOUSE_MOVE_AWAY,
            location=b,
            max_width=max_width,
            max_height=max_height,
            on_navigate=self.on_navigate,
            on_hide=self.on_hide
        )
        
        view.add_regions(
            "ring_tooltip",
            [sublime.Region(a, b)],
            "invalid",
            "",
            sublime.HIDE_ON_MINIMAP | sublime.DRAW_NO_FILL
        )
        
    def on_navigate(self, link):
        if link == "tooltip.copy":
            sublime.set_clipboard(copy)
            self.view.update_popup("".join(menus).replace(">copy</a>", ">copied✔</a>"))
        else:
            webbrowser.open_new_tab(link)
            
    def on_hide(self):
        self.view.erase_regions("ring_tooltip")
        Pref.isActive = False

class RingToggleTooltipsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("ring.sublime-settings")
        current = settings.get("show_tooltips", True)
        settings.set("show_tooltips", not current)
        sublime.save_settings("ring.sublime-settings")
        status = "enabled" if not current else "disabled"
        sublime.status_message("Ring tooltips {}".format(status))

class RingRunCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name() and self.view.file_name().endswith('.ring'):
            self.view.window().run_command("build")
        else:
            sublime.error_message("Current file is not a Ring file (.ring)")
    
    def is_enabled(self):
        file_name = self.view.file_name()
        return bool(file_name and file_name.endswith('.ring'))

class RingOpenWebsiteCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        webbrowser.open_new_tab("https://ring-lang.net/")

class RingOpenDocumentationCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        webbrowser.open_new_tab("https://ring-lang.net/doc1.22/")

class RingOpenGroupCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        webbrowser.open_new_tab("https://groups.google.com/g/ring-lang")

class RingOpenSettingsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command("open_file", {
            "file": "${packages}/ring-sublime/ring.sublime-settings"
        })
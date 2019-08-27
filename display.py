""" Draw a native window. """

import wx
from wx import html2

class MyApp(wx.App):
    def OnInit(self):
        WebFrame(None, "Régate").Show()
        return True

class WebFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self._web = html2.WebView.New(self)
        self._web.LoadURL("http://127.0.0.1:23914/login")
        # self.Bind(html2.EVT_WEBVIEW_TITLE_CHANGED, self.OnTitle)

        def OnTitle(self, event):
            self.Title = event.GetString()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()

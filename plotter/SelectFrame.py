import wx
from wx.lib.plot import *
# Needs Numeric or numarray or NumPy
try:
    import numpy.oldnumeric as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        try:
            import Numeric as _Numeric
        except:
            msg= """
            This module requires the Numeric/numarray or NumPy module,
            which could not be imported.  It probably is not installed
            (it's not part of the standard Python distribution). See the
            Numeric Python site (http://numpy.scipy.org) for information on
            downloading source or binaries."""
            raise ImportError, "Numeric,numarray or NumPy not found. \n" + msg

sys.path.append('..')
from SimulationKit.pubsub import *
from PlotFrame import *
import time
import threading

class SelectFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, (600, 400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

        self.SetMenuBar(self.mainmenu)

        # A status bar to tell people what's happening
        self.CreateStatusBar(1)
        
        # FIXME:  Put this elsewhere
        self.subscriber    = Subscriber( 'localhost', 5055 )

        self.subscriptions = {}
        self.data = {}

        # For each entry in the catalog we must figure out where it belongs in the tree
        root_d={}
        for full_name in self.subscriber.catalog:
	    # FIXME: Eventually wee want to be able to plot vairables against eachother, not just against time.
	    # But since we can't do that right now time must always be selected
	    if full_name == 'time':
		self.subscriptions['time'] = 0
		continue
            tokens = full_name.split('.')
            d = root_d
            for token in tokens:
                if not d.has_key(token):
                    d[token] = {}
                d = d[token]

        # The outermost sizer
        self.vsizer_0 = wx.BoxSizer(wx.VERTICAL)

        # list of available variables
        self.catalog = wx.TreeCtrl(self, wx.NewId(), style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_ROW_LINES)
        root_item = self.catalog.AddRoot('root')
        def walkDictForTree(d,tree_item):
            for k,v in d.items():
                child_item = self.catalog.AppendItem(tree_item, k)
                walkDictForTree( v, child_item )
            self.catalog.SortChildren(tree_item)
        walkDictForTree( root_d, root_item )
        self.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.OnCatalogItemActivated, self.catalog )

        self.play_stop_button = wx.Button( self, -1, "Play" )
        self.Bind( wx.EVT_BUTTON, self.OnPlayStopButton, self.play_stop_button )

        self.vsizer_0.Add( self.catalog          , 1 , wx.EXPAND , 0 );
        self.vsizer_0.Add( self.play_stop_button , 0 , wx.EXPAND , 0 );
        self.SetSizer(self.vsizer_0)

        self.Show(True)
    def OnCatalogItemActivated( self, event ):
        itemid = event.GetId()
        tree = event.GetEventObject()
        treeitem = tree.GetSelection()
        text = tree.GetItemText(treeitem)
        # If this item has children keep propagating
        if tree.ItemHasChildren( treeitem ):
            if tree.IsExpanded( treeitem ):
                tree.Collapse( treeitem )
            else:
                tree.Expand( treeitem )
            return
        else:
            full_name = ''
            item = treeitem
            root = tree.GetRootItem()
            while item != root:
                full_name = tree.GetItemText(item) + '.' + full_name
                item = tree.GetItemParent( item )
            full_name = full_name[:-1]
            if self.subscriptions.has_key(full_name):
                tree.SetItemBackgroundColour( treeitem, (255,255,255) )
                del self.subscriptions[full_name]
                # Recurse up the tree, change colors appropriately
                item = tree.GetItemParent( treeitem )
                while item != root:
                    # Check the active leaf count
                    count = tree.GetItemPyData( item )
                    if count:
                        count -= 1
                    tree.SetItemPyData( item, count )
                    if not count:
                        tree.SetItemBackgroundColour( item, (255,255,255) )
                    item  = tree.GetItemParent( item )
            else:
                tree.SetItemBackgroundColour( treeitem, (100,255,100) )
                self.subscriptions[full_name] = 0
                # Recurse up the tree, change colors appropriately
                item = tree.GetItemParent( treeitem )
                while item != root:
                    # Check the active leaf count
                    count = tree.GetItemPyData( item )
                    if count == None:
                        count = 0
                    count += 1
                    tree.SetItemPyData( item, count )
                    tree.SetItemBackgroundColour( item, (255,255,100) )
                    item  = tree.GetItemParent( item )
    def OnDataFrameReceived( self, frame ):
        for k,v in frame.items():
            self.data[k].pop(0)
            self.data[k].append(v)
    def OnPlayStopButton(self, event, close_window = False):
        if self.play_stop_button.GetLabel() == 'Play':
            self.play_stop_button.SetLabel('Stop')
            self.data = { k:[0 for x in range(1000)] for k in self.subscriptions }
            self.subscriber.subscribeTo( self.subscriptions )
            self.subscriber.setCallback( self.OnDataFrameReceived )
            self.subscriber.start()
            if hasattr(self, 'plot_frame'):
                self.plot_frame.Destroy()
            self.plot_frame = PlotFrame(self, -1, "PlotCanvas")
            self.plot_frame.data = self.data
            self.animation_timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.plot_frame.drawData, self.animation_timer)
            self.animation_timer.Start(100,0)
        else:
            self.animation_timer.Stop()
            self.play_stop_button.SetLabel('Play')
            self.subscriber.close()
            self.subscriber    = Subscriber( 'localhost', 5055 )
            if close_window:
                self.plot_frame.Destroy()
                del self.plot_frame
    def OnClose(self, event):
        self.subscriber.close()
        self.Destroy()
    def OnHelpAbout(self, event):
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, __doc__, "About...")
        about.ShowModal()

def __test():
    class MyApp(wx.App):
        def OnInit(self):
            #wx.InitAllImageHandlers()
            frame = SelectFrame(None, -1, "Selection Panel")
            #frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    __test()

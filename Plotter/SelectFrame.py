from PlotFrameSettings import *
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
from Utilities.pubsub import *
from PlotFrame import *
import time
import threading
import os

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
        
        self.config = PlotFrameSettings()
        # FIXME: we need to support plotting variables against eachother in the
        # future
        self.config.subscriptions.append('time')
        self.next_port = 5056
        
        # Grab the catalog and close the subscriber
        self.subscriber    = Subscriber( 'localhost', 5055 )
        self.subscriber.close()
        # For each entry in the catalog we must figure out where it belongs in the tree
        root_d={}
        for full_name in self.subscriber.catalog:
            if full_name == 'time':
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

        self.play_button = wx.Button( self, -1, "Play" )
        self.Bind( wx.EVT_BUTTON, self.OnPlayButton, self.play_button )

        self.vsizer_0.Add( self.catalog          , 1 , wx.EXPAND , 0 );
        self.vsizer_0.Add( self.play_button , 0 , wx.EXPAND , 0 );
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
            def recurseUpTreeChangingColors( root, item, color, inc=1 ):
                while item != root:
                    # Check the active leaf count
                    count = tree.GetItemPyData( item )
                    if count:
                        count += inc
                    tree.SetItemPyData( item, count )
                    if not count:
                        tree.SetItemBackgroundColour( item, color )
                    item  = tree.GetItemParent( item )
            if full_name in self.config.subscriptions:
                # Item was already selected, remove from subscriptions
                tree.SetItemBackgroundColour( treeitem, (255,255,255) )
                self.config.subscriptions.remove(full_name)
                item = tree.GetItemParent( treeitem )
                # Recurse up the tree, change colors appropriately
                recurseUpTreeChangingColors(root,item,(255,255,255))
            else:
                # Add item to subscriptions
                tree.SetItemBackgroundColour( treeitem, (100,255,100) )
                self.config.subscriptions.append(full_name)
                # Recurse up the tree, change colors appropriately
                item = tree.GetItemParent( treeitem )
                recurseUpTreeChangingColors(root,item,(255,255,100),inc=-1)
    def OnRemoteDisconnect( self ):
        self.Stop(connect_callback=self.Play)
    def OnPlayButton(self, event ):
        self.config.port = self.next_port
        self.next_port += 1
        savePlotFrameSettingsToFile( self.config, 'plot_settings.pickle' )
        self.subscriber    = Subscriber( 'localhost', 5055 )
        self.subscriber.requestAnotherPublisher(self.config.port)
        self.subscriber.close()
        os.system('python PlotFrame.py plot_settings.pickle &')
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

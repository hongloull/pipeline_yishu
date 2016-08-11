import path
import pymel.core as pm
import xml.dom.minidom

def loadMenu():
    #    get user menu from menu.xml
    menuXmlPath=path.path(__file__).parent.joinpath('menu_pipeline.xml')
    
    #    get gMainWindow from mel command
    gMainWindow = pm.mel.eval('$tmpVar=$gMainWindow')
    print gMainWindow
    if gMainWindow:
        if menuXmlPath.exists() :        
            menuLabel = ''
            menuName = 'pipeLineMenu'
            print ('Build Menu : ' + menuName)
    
            #    open xml document
            menuXml = xml.dom.minidom.parse(menuXmlPath)
            
            #    search menu node
            for item in menuXml.getElementsByTagName('menu'):
                
                val = item.attributes["name"].value
                menuLabel = val.encode('latin-1', 'replace')
    
                #    search and delete old menuName
                menuList = pm.window(gMainWindow, query=True, menuArray=True)
                
                for menu in menuList:
                    if pm.menu(menu, query=True, label=True) == menuLabel:
                        pm.menu(menu, edit=True, deleteAllItems=True)
                        pm.deleteUI(menu)
                        break
                
                #    Add userMenu to Maya Menu
                pm.menu(menuName, parent=gMainWindow, tearOff=True, label=menuLabel, allowOptionBoxes=True)
                
                #    build each menu
                for child in item.childNodes:
                        if child.nodeType == 1 :
                            #loadMenu_recursive(child)                     
                            nodename = child.nodeName
                            nodetype = child.attributes["type"].value
                            
                            loadMenu_recursive(child, menuName)

                            
def loadMenu_recursive(menuXml, menuName):
    if menuXml.nodeType == 1 :
        nodename    = menuXml.nodeName
        nodetype    = menuXml.attributes["type"].value
        
        if nodetype == 'subMenu' :
            name = menuXml.attributes["name"].value
            pm.menuItem(parent=menuName, subMenu=True, tearOff=True, label=name)       
        
            for child in menuXml.childNodes:
                loadMenu_recursive(child, menuName)
                
            pm.setParent( '..' )
            
        if nodetype == 'command' :
            name        = menuXml.attributes["name"].value
            comment     = menuXml.attributes["comment"].value
            commandExe  = menuXml.attributes["cmd"].value
            mode        = menuXml.attributes["mode"].value
            
            option      = menuXml.attributes["option"].value
            if option == 'False' :
                option = False
            else :
                option = True
                cmd_option = menuXml.attributes["cmd_option"].value
                
            cmd = commandExe.encode('latin-1', 'replace') 
            if mode == 'mel': 
                commandExe  = ('pm.mel.eval(\'' +  cmd + '\')')
                pm.menuItem(label=name, command=commandExe, annotation=commandExe)
                if option :
                    pm.menuItem(label=name, command=commandExe, annotation=commandExe, optionBox=option)
                
            if mode == 'python':
                pm.menuItem(label=name, command=commandExe, annotation=commandExe)
                if option :
                    pm.menuItem(label=name, command=cmd_option, annotation=commandExe, optionBox=option)
                
                            
        if nodetype == 'separator' :
            pm.menuItem( divider=True)

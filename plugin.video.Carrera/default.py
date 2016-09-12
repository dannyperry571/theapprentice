# -*- coding: utf-8 -*-


'''
    Template Add-on
    Copyright (C) 2016 Demo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os
try:
    import json
except:
    import simplejson as json
import yt
ADDON_NAME = 'Carrera'
addon_id = 'plugin.video.Carrera'
Base_Url = 'http://herovision.x10host.com/carrera/'
Main_Menu_File_Name = 'main.php'
search_filenames = ['sv1','teh','s5']
########################################################################################
### FAVOURITES SECTION IS NOT THIS AUTHORS CODE, I COULD NOT GET IT TO REMOVE FAVOURITES SO ALL CREDIT DUE TO THEM, SORRY IM NOT SURE WHERE IT CAME FROM BUT GOOD WORK :) ###

ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/'+addon_id)
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
PATH = 'Carrera'
VERSION = '0.0.1'
Dialog = xbmcgui.Dialog()
addon_data = xbmc.translatePath('special://home/userdata/addon_data/'+addon_id+'/')
favorites = os.path.join(addon_data, 'favorites.txt')
watched = addon_data + 'watched.txt'
source_file = Base_Url + 'source_file.php'
debug = ADDON.getSetting('debug')
if os.path.exists(addon_data)==False:
    os.makedirs(addon_data)
if not os.path.exists(watched):
    open(watched,'w+')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
watched_read = open(watched).read()

def Main_Menu():
    OPEN = Open_Url(Base_Url+Main_Menu_File_Name)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        if name == '[COLORskyblue]F[COLORblue]avourites[/COLOR]':
         	Menu(name,url,6,icon,fanart,desc)	
        elif 'php' in url:
            Menu(name,url,1,icon,fanart,desc)
        elif name == '[COLORskyblue]S[COLORblue]earch[/COLOR]':
         	Menu('[COLORskyblue]S[COLORblue]earch[/COLOR]',url,3,icon,fanart,desc)
        elif name == '[COLORskyblue]i[COLORblue]dex[/COLOR]':
            Menu('[COLORskyblue]O[COLORblue]nline Lists[/COLOR]',url,10,icon,fanart,desc)
        else:
            Play(name,url,2,icon,fanart,desc)
    setView('tvshows', 'Media Info 3')			
	
def Second_Menu(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        Watched = re.compile('item="(.+?)"\n').findall(str(watched_read))
        for item in Watched:
            if item == url:
                name = '[COLORred]* [/COLOR]'+(name).replace('[COLORred]* [/COLOR][COLORred]* [/COLOR]','[COLORred]* [/COLOR]')
                print_text_file = open(watched,"a")
                print_text_file.write('item="'+name+'"\n')
                print_text_file.close
        if 'php' in url:
            Menu(name,url,1,icon,fanart,desc)
        else:
            Play(name,url,2,icon,fanart,desc)
    setView('tvshows', 'Media Info 3')

def index_Menu():
    #Menu('Favourites','',5,'','','','','')
    Menu('List of Index\'s','',10,'','','')
    #    Menu('Search','',6,ICON,FANART,'','','')
# Menu('[COLORred]Press here to add a source url[/COLOR]	','',2,'','','','','')

def Index_List():
    OPEN = Open_Url(source_file)
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url,name in Regex:
            Menu(name,url,8,'','','')



#####################################MAIN REGEX LOOP ###############################

def Main_Loop(url):
    HTML = Open_Url(url)
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(HTML)
    for url2,name in match:
        url3 = url + url2
        if '..' in url3:
            pass
        elif 'rar' in url3:
            pass
        elif 'jpg' in url3:
            pass
        elif 'vtx' in url3:
            pass
        elif 'srt' in url3:
            pass
        elif 'C=' in url2:
            pass
        elif '/' in url2:
            Menu((name).replace('/',''),url3,8,ICON,FANART,'','','')
        else:
            Clean_name(name,url3)

################################### TIDY UP NAME #############################

def Clean_name(name,url3):
    name1 = (name).replace('S01E','S01 E').replace('(MovIran).mkv','').replace('The.Walking.Dead','').replace('.mkv','').replace('Tehmovies.com.mkv','').replace('Nightsdl','').replace('Ganool','')
    name2=(name1).replace('.',' ').replace(' (ParsFilm).mkv','').replace('_TehMovies.Com.mkv','').replace(' (SaberFun.IR).mkv','').replace('[UpFilm].mkv','').replace('(Bia2Movies)','')
    name3=(name2).replace('.mkv','').replace('.Film2Movie_INFO.mkv','').replace('.HEVC.Film2Movie_INFO.mkv','').replace('.ParsFilm.mkv ','').replace('(SaberFunIR)','')
    name4=(name3).replace('.INTERNAL.','').replace('.Film2Movie_INFO.mkv','').replace('.web-dl.Tehmovies.net.mkv','').replace('S01E06','S01 E06').replace('S01E07','S01 E07')
    name5=(name4).replace('S01E08','S01 E08').replace('S01E09','S01 E09').replace('S01E10','S01 E10').replace('.Tehmovies.net','').replace('.WEBRip.Tehmovies.com.mkv','')
    name6=(name5).replace('.mp4','').replace('.mkv','').replace('.Tehmovies.ir','').replace('x265HEVC','').replace('Film2Movie_INFO','').replace('Tehmovies.com.mkv','')
    name7=(name6).replace(' (ParsFilm)','').replace('Tehmovies.ir.mkv','').replace('.480p',' 480p').replace('.WEBrip','').replace('.web-dl','').replace('.WEB-DL','')
    name8=(name7).replace('.','').replace('.Tehmovies.com','').replace('480p.Tehmovies.net</',' 480p').replace('720p.Tehmovies.net','720p').replace('.480p',' 480p')
    name9=(name8).replace('.480p.WEB-DL',' 480p').replace('.mkv','').replace('.INTERNAL.','').replace('720p',' 720p').replace('.Tehmovi..&gt;','').replace('.Tehmovies.net.mkv','')
    name10=(name9).replace('..720p',' 720p').replace('.REPACK.Tehmovies..&gt;','').replace('.Tehmovies.com.mkv','').replace('.Tehmovies..&gt;','').replace('Tehmovies.ir..&gt;','')
    name11=(name10).replace('Tehmovies.ne..&gt;','').replace('.HDTV.x264-mRs','').replace('...&gt;','').replace('.Tehmovies...&gt;','').replace('.Tehmovies.com.mp4','')
    name12=(name11).replace('.Tehmovies.com.mp4','').replace('_MovieFarsi','').replace('_MovieFar','').replace('_com','').replace('&gt;','').replace('avi','').replace('(1)','')
    name13=(name12).replace('(2)','').replace('cd 2','').replace('cd 1','').replace('-dos-xvid','').replace('divx','').replace('Xvid','').replace('DVD','').replace('DVDrip','')
    name14=(name13).replace('DvDrip-aXXo','').replace('[','').replace(']','').replace('(','').replace(')','').replace('XviD-TLF-','').replace('CD1','').replace('CD2','')
    name15=(name14).replace('CD3','').replace('mp4','').replace('&amp;','&').replace('HDRip','').replace('-','').replace('  ',' ').replace('xvid','').replace('1080p','')
    name16=(name15).replace('1970','').replace('1971','').replace('1972','').replace('1973','').replace('1974','').replace('1975','').replace('1976','').replace('1977','')
    name17=(name16).replace('1978','').replace('1979','').replace('1980','').replace('1981','').replace('1982','').replace('1983','').replace('1984','').replace('1985','')
    name18=(name17).replace('1986','').replace('1987','').replace('1988','').replace('1989','').replace('1990','').replace('1991','').replace('1992','').replace('1993','')
    name19=(name18).replace('1994','').replace('1995','').replace('1996','').replace('1997','').replace('1998','').replace('1999','').replace('2000','').replace('2001','')
    name20=(name19).replace('2002','').replace('2003','').replace('2004','').replace('2005','').replace('2006','').replace('2007','').replace('2008','').replace('2009','')
    name21=(name20).replace('2010','').replace('2011','').replace('2012','').replace('2013','').replace('2014','').replace('2015','').replace('2016','').replace('720p','')
    name22=(name21).replace('360p','').replace('  ',' ').replace('BluRay','').replace('rip','').replace('WEBDL','').replace('s01','').replace('s02','').replace('S02','')
    name23=(name22).replace('s03','').replace('s04','').replace('s05','').replace('s06','').replace('s07','').replace('s08','').replace('s09','').replace('S01','')
    name24=(name23).replace('S03','').replace('S04',' ').replace('S05','').replace('S06','').replace('S07','').replace('S08','').replace('S09','').replace('E01','')
    name25=(name24).replace('E02','').replace('E03','').replace('E04','').replace('E05','').replace('E06','').replace('E07','').replace('E08','').replace('E09','').replace('e01','')
    name25=(name24).replace('e02','').replace('e03','').replace('e04','').replace('e05','').replace('e06','').replace('e07','').replace('e08','').replace('e09','').replace('e01','')
    clean_name = name15
    search_name = name25
        #if ADDON.getSetting('Data')=='true':
        # Imdb_Scrape(url3,clean_name,search_name)
        #if ADDON.getSetting('Data')=='false':
    Play(clean_name,url3,2,ICON,FANART,'','','')

def Search():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_Title = Search_Name.lower()
    if Search_Title == '':
        pass
    else:
		for file_Name in search_filenames:
			search_URL = Base_Url + file_Name + '.php'
			OPEN = Open_Url(search_URL)
			if OPEN != 'Opened':			
				Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
				for url,icon,desc,fanart,name in Regex:
					if Search_Title in name.lower():
						Watched = re.compile('item="(.+?)"\n').findall(str(watched_read))
						for item in Watched:
							if item == url:
								name = '[COLORred]* [/COLOR]'+(name).replace('[COLORred]* [/COLOR][COLORred]* [/COLOR]','[COLORred]* [/COLOR]')
								print_text_file = open(watched,"a")
								print_text_file.write('item="'+name+'"\n')
								print_text_file.close
						if 'php' in url:
							Menu(name,url,1,icon,fanart,desc)
						else:
							Play(name,url,2,icon,fanart,desc)
						
			setView('tvshows', 'Media Info 3')
####################################################################PROCESSES###################################################
def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try: 
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def setView(content, viewType):
	if content:
	    xbmcplugin.setContent(int(sys.argv[1]), content)
		
def Menu(name,url,mode,iconimage,fanart,description,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

		
def Play(name,url,mode,iconimage,fanart,description,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        
		
def GetPlayerCore(): 
    try: 
        PlayerMethod=getSet("core-player") 
        if   (PlayerMethod=='DVDPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_DVDPLAYER 
        elif (PlayerMethod=='MPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_MPLAYER 
        elif (PlayerMethod=='PAPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_PAPLAYER 
        else: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    except: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    return PlayerMeth 
    return True 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
		

def resolve(url):
    print_text_file = open(watched,"a")
    print_text_file.write('item="'+url+'"\n')
    print_text_file.close
    play=xbmc.Player(GetPlayerCore())
    import urlresolver
    try: play.play(url)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addon_log(string):
    if debug == 'true':
        xbmc.log("["+ADDON_NAME+"]: %s" %(addon_version, string))

def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            addon_log('Making Favorites File')
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            addon_log('Appending Favorites')
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
		

def getFavorites():
        if os.path.exists(favorites)==False:
            favList = []
            addon_log('Making Favorites File')
            favList.append(('[COLORskyblue]C[COLORblue]arrera Favourites Section[/COLOR]','','','','','',''))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()        
        else:
			items = json.loads(open(favorites).read())
			total = len(items)
			for i in items:
				name = i[0]
				url = i[1]
				iconimage = i[2]
				try:
					fanArt = i[3]
					if fanArt == None:
						raise
				except:
					if ADDON.getSetting('use_thumb') == "true":
						fanArt = iconimage
					else:
						fanArt = fanart
				try: playlist = i[5]
				except: playlist = None
				try: regexs = i[6]
				except: regexs = None

				if i[4] == 0:
					Menu(name,url,'',iconimage,fanart,'','fav')
				else:
					Menu(name,url,i[4],iconimage,fanart,'','fav')

def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")	
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None
fav_mode=None


try:
    fav_mode=int(params["fav_mode"])
except:
    pass

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#####################################################END PROCESSES##############################################################		
		
if mode == None: Main_Menu()
elif mode == 1 : Second_Menu(url)
elif mode == 2 :     
    if 'youtube' in url:
        url = (url).replace('https://www.youtube.com/watch?v=','').replace('http://www.youtube.com/watch?v=','')
        yt.PlayVideo(url)
    else:
    	resolve(url)
elif mode == 3 : Search()
elif mode==4:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==5:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)
elif mode==6:
    addon_log("getFavorites")
    getFavorites()
elif mode == 7 : index_Menu()
elif mode == 8 : Main_Loop(url)
elif mode == 9 : Source_File()
elif mode ==10 : Index_List()

xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))

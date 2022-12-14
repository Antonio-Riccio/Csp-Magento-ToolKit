#main (ok)

# Python
import argparse
import os            
            
def createCsp(args):
    creatCspWhitelist(args)
    createCspConfig(args)
    createCspModule(args)
    createCspRegistration(args)
    createCspComposer(args)
    return 0


#csp_whitelist.xml
def creatCspWhitelist(args):
    if (not os.path.exists('etc')):
            os.mkdir('etc')

    if (args.fileLog=="default"):
        csp_whitelistVarFile = '''<?xml version="1.0"?>
<csp_whitelist xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Csp/etc/csp_whitelist.xsd">
    <policies>
        <policy id="script-src">
            <values>
                <value id="addthis.com" type="host">*.addthis.com</value>
                <value id="ajaxgoogleapis" type="host">*.googleapis.com</value>
                <value id="cloudflare" type="host">*.cloudflare.com</value>
                <value id="fontawesome" type="host">*.fontawesome.com</value>
                <value id="google" type="host">*.google.com</value>
                <value id="google-analytics" type="host">*.google-analytics.com</value>
                <value id="googletagmanager.com" type="host">googletagmanager.com</value>
                <value id="graph-facebook" type="host">graph.facebook.com</value>
                <value id="gstatic" type="host">*.gstatic.com</value>
                <value id="addthis.moatads.com" type="host">*.moatads.com</value>
                <value id="trustpilot" type="host">*.trustpilot.com</value>
                <value id="vimeo" type="host">*.vimeo.com</value>
                <value id="widgets-pinterest" type="host">widgets.pinterest.com</value>
            </values>
        </policy>
        <policy id="style-src">
            <values>
                <value id="cloudflare" type="host">*.cloudflare.com</value>
                <value id="fontawesome" type="host">*.fontawesome.com</value>
                <value id="googleapis" type="host">*.googleapis.com</value>
                <value id="gstatic" type="host">*.gstatic.com</value>
                <value id="twitter.com" type="host">*.twitter.com</value>
            </values>
        </policy>
        <policy id="img-src">
            <values>
                <value id="cloudflare" type="host">*.cloudflare.com</value>
                <value id="data" type="host">data:</value>
                <value id="google-analytics" type="host">*.google-analytics.com</value>
                <value id="paypal" type="host">*.paypal.com</value>
                <value id="twitter.com" type="host">*.twitter.com</value>
                <value id="vimeocdn" type="host">*.vimeocdn.com</value>
            </values>
        </policy>
        <policy id="connect-src">
            <values>
                <value id="cloudflare" type="host">*.cloudflare.com</value>
                <value id="paypal" type="host">*.paypal.com</value>
                <value id="twitter.com" type="host">*.twitter.com</value>
            </values>
        </policy>
        <policy id="font-src">
            <values>
                <value id="cloudflare" type="host">*.cloudflare.com</value>
                <value id="fontawesome" type="host">*.fontawesome.com</value>
                <value id="fontawesomecdn" type="host">*.bootstrapcdn.com</value>
                <value id="googleapis" type="host">*.googleapis.com</value>
                <value id="gstatic" type="host">*.gstatic.com</value>
                <value id="twitter.com" type="host">*.twitter.com</value>
            </values>
        </policy>

        <policy id="frame-src">
            <values>
                <value id="addthis.com" type="host">*.addthis.com</value>
                <value id="google.com" type="host">*.google.com</value>
                <value id="trustpilot" type="host">*.trustpilot.com</value>
                <value id="twitter.com" type="host">*.twitter.com</value>
                <value id="vimeo" type="host">*.vimeo.com</value>
            </values>
        </policy>

    </policies>
</csp_whitelist>
'''

        f = open("etc/csp_whitelist.xml", "w")
        f.write(csp_whitelistVarFile)
        f.close()
    else:
        generatorCspWhitelist(args.fileLog)
        

#config.xml
def createCspConfig(args):
    moduleVarFile = '''<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Store:etc/config.xsd">
    <default>
        <csp>
            <policies>
                <storefront>
                    <frame-ancestors>
                        <inline>'''+str(args.trt)+'''</inline>
                    </frame-ancestors>
                </storefront>
                <admin>
                    <frame-ancestors>
                        <inline>'''+str(args.tra)   +'''</inline>
                    </frame-ancestors>
                </admin>
            </policies>
        </csp>
    </default>
</config>
'''

    f = open("etc/config.xml", "w")
    f.write(moduleVarFile)
    f.close()

#module.xml
def createCspModule(args):
    moduleVarFile = '''<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="'''+ args.nameMod + '''" setup_version="'''+args.version+'''"/>
</config>
'''

    f = open("etc/module.xml", "w")
    f.write(moduleVarFile)
    f.close()

#registration.php
def createCspRegistration(args):

    registrationVarFile = '''<?php
use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(ComponentRegistrar::MODULE, ' '''+args.nameMod+''' ', __DIR__);
'''

    f = open("registration.php", "w")
    f.write(registrationVarFile)
    f.close()

#composer.php
def createCspComposer(args):    
    composerVarFile = '''{
  "name": "csp/module-csp",
  "version": "'''+args.version+'''",
  "description": "This module handle CSP policies",
  "type": "magento2-module",
  "require": {
    "../../../../vendor/magento/framework": "*",
    "../../../../vendor/magento/module-csp": "100.3.*"
  },
  "license": [
    "Proprietary"
  ],
  "autoload": {
    "files": [
      "registration.php"
    ],
    "psr-4": {
      "Ev\\CSP\\": ""
    }
  }
}
'''

    f = open("composer.json", "w")
    f.write(composerVarFile)
    f.close()

def generatorCspWhitelist(nameFileLog):
    
    frameAncestors = []
    imgSrc = []
    connectSrc = []
    fontSrc = []
    defaultSrc = []
    baseUrl = []
    childSrc = []
    formAction = []	
    manifestSrc = []
    mediaSrc = []
    objectSrc = []
    scriptSrc = []
    styleSrc = []
    typeError = ''
    
    initCsp_Whitelist = '''<?xml version="1.0"?>
<csp_whitelist xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Csp/etc/csp_whitelist.xsd">
    <policies>
'''
    
    policyScriptStart = '''        <policy id="script-src">
            <values>
'''
    policyStyleStart = '''        <policy id="style-src">
            <values>
'''
    policyImgStart = '''        <policy id="img-src">
            <values>
'''
    policyConnectStart = '''        <policy id="connect-src">
            <values>
'''
    policyFontStart = '''        <policy id="font-src">
            <values>
'''
    policyFrameStart = '''        <policy id="frame-src">
            <values>
'''
    policyStop = '''            </values>
        </policy>
'''
    endCsp_Whitelist = '''    </policies>
</csp_whitelist>
'''

    f = open(nameFileLog,"r")
    lines = f.readlines()

    for line in lines:
        if ('<URL>' not in line):
            typeError=None
            
            if("Refused to load the script" in line):
                typeError="script-src"
            elif("Refused to load the stylesheet" in line):
                typeError="style-src"
            elif("Refused to load the font" in line):
                typeError="font-src"
            elif("Refused to frame" in line):
                typeError="frame-src"
            elif("Refused to connect" in line):
                typeError="connect-src"
            elif("Refused to load the image" in line):
                typeError="img-src"
            
            if(typeError!=None):
                http=0
                exit = False
                while exit == False:
                    http=http+1
                    if (line[http]=='h'):
                        if (
                            line[http+1] == 't' and 
                            line[http+2] == 't' and 
                            line[http+3] == 'p' 
                        ):
                            exit = True
                            if (line[http+4] == 's'):
                                end=http + 4
                            else:
                                end=http + 3
                exit = False
                while exit == False:
                    end=end+1

                    if(getTldFour(line, end)):
                        end = end + 4
                        exit = True
                    elif  (getTldThree(line, end)):
                        end = end + 3
                        exit = True
                    elif(getTldDuo(line, end)):
                        end = end + 2
                        exit = True

                if(typeError=="script-src"):
                    if (line[http:end] not in scriptSrc):
                        scriptSrc.append(line[http:end])
                elif(typeError=="style-src"):
                    if (line[http:end] not in styleSrc):
                        styleSrc.append(line[http:end])
                elif(typeError=="font-src"):
                    if (line[http:end] not in fontSrc):
                        fontSrc.append(line[http:end])
                elif(typeError=="frame-src"):
                    if (line[http:end] not in frameAncestors):
                        frameAncestors.append(line[http:end])
                elif(typeError=="connect-src"):
                    if (line[http:end] not in connectSrc):
                        connectSrc.append(line[http:end])
                elif(typeError=="img-src"):
                    if (line[http:end] not in imgSrc):
                        imgSrc.append(line[http:end])

    f = open("etc/csp_whitelist.xml", "w")
    f.write(initCsp_Whitelist)

    # <value id="addthis.com" type="host">*.addthis.com</value>
    idHost = 0
    if (scriptSrc!=[]):
        f.write(policyScriptStart)
        for host in scriptSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)


    if (styleSrc!=[]):
        f.write(policyStyleStart)
        for host in styleSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)


    if (fontSrc!=[]):
        f.write(policyFontStart)
        for host in fontSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)


    if (frameAncestors!=[]):
        f.write(policyFrameStart)
        for host in frameAncestors:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)


    if (connectSrc!=[]):
        f.write(policyConnectStart)
        for host in connectSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)


    if (imgSrc!=[]):
        f.write(policyImgStart)
        for host in imgSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost = idHost +1
        f.write(policyStop)

    f.write(endCsp_Whitelist)

    f.close()
    return 0

def getTldDuo(line, end):
    tld = [
           'ac','ad','ae',
           'af','ag','ai','al',
           'am','an','ao','aq',
           'ar','as','at','au',
           'aw','ax','az','ba',
           'bb','bd','be','bf',
           'bg','bh','bi','bj',
           'bm','bn','bo','br',
           'bs','bt','bv','bw',
           'by','bz','ca','cc',
           'cd','cf','cg','ch',
           'ci','ck','cl','cm',
           'cn','co','cr','cu',
           'cv','cx','cy','cz',
           'de','dj','dk','dm',
           'do','dz','ec','ee',
           'eg','eh','er','es',
           'et','eu','fi','fj',
           'fk','fm','fo','fr',
           'ga','gb','gd','ge',
           'gf','gg','gh','gi',
           'gl','gm','gn','gp',
           'gq','gr','gs','gt',
           'gu','gw','gy','hk',
           'hm','hn','hr','ht',
           'hu','id','ie','il',
           'im','in','io','iq',
           'ir','is','it','je',
           'jm','jo','jp','ke',
           'kg','kh','ki','km',
           'kn','kp','kr','kw',
           'ky','kz','la','lb',
           'lc','li','lk','lr' 
          ]

    for tldOne in tld:
        if (tldOne[0] == line[end] and 
            tldOne[1]== line[end+1]):
            if (line[end+2] == '\'' or 
                line[end+2] == '/'):
                return True
    return False

def getTldThree(line, end):   
    tld = ['biz', 'cat', 'com', 
           'edu','gov', 'int', 'mil'] 

    for tldOne in tld:
        if (tldOne[0] == line[end] and 
            tldOne[1]== line[end+1] and
            tldOne[2]== line[end+2]):
            if (line[end+3] == '\'' or 
                line[end+3] == '/'):
                return True
    return False


def getTldFour(line, end):   
    tld = ['aero', 'asia', 'coop',
           'info', 'jobs','mobi'] 

    for tldOne in tld:
        if (tldOne[0] == line[end] and 
            tldOne[1]== line[end+1] and
            tldOne[2]== line[end+2] and
            tldOne[3]== line[end+3] ):
            if (line[end+4] == '\'' or 
                line[end+4] == '/'):
                return True
    return False

def clearFileLog(nameFileLog):    
    nameFileClear = os.path.splitext(nameFileLog)[0]+'_clear.log'
    fileLogClear = open(nameFileClear,"w")

    fileLog = open(nameFileLog,"r")
    lines = fileLog.readlines()

    for line in lines:
        if ('<URL>' not in line):
            if( 
                "Refused to load the script" in line or 
                "Refused to load the stylesheet" in line or            
                "Refused to load the font" in line or 
                "Refused to frame" in line or 
                "Refused to connect" in line or
                "Refused to load the image" in line ):
                fileLogClear.write(line+"\n")

    fileLog.close()
    fileLogClear.close()
    return nameFileClear

def stepToStep(args):
    notFoundFile = True

    args.nameMod = input("Name Module: ")

    NameFile = input("Path file Log: ")
    while notFoundFile:
        try:
            f = open(NameFile)
            if ('/' in NameFile):
                NameFileSplit = NameFile.split('/')
                
                if( 
                  os.path.splitext(NameFileSplit[len(NameFileSplit)-1])[1] == '.log' or
                  os.path.splitext(NameFileSplit[len(NameFileSplit)-1])[1] == '.txt'
                  ):
                    notFoundFile = False
                    f.close()
            else:
                if( 
                  os.path.splitext(NameFile)[1] == '.log' or
                  os.path.splitext(NameFile)[1] == '.txt'
                  ):
                    notFoundFile = False
                    f.close()
        except IOError:
            print("File not found\nRemember add file extension (.txt or .log)\n ")
            NameFile = input("Path file Log: ")

    args.fileLog = NameFile

    args.version = input("Version Module:")
    args.setId = input("Id value: ")

    print('\nSet 0 or 1')
    args.trt = input("Type report storefront: ")
    args.trt = int (args.trt)

    while args.trt != 0 and args.trt != 1: 
        print('\nSet 0 or 1')
        args.trt = input("Type report storefront: ")
        args.trt = int (args.trt)

    print('\nSet 0 or 1')
    args.tra = input("Type report admin: ")
    args.tra =int (args.tra)

    while args.tra != 0 and args.tra != 1: 
        print('\nSet 0 or 1')
        args.tra = input("Type report admin: ")
        args.tra =int (args.tra)

    createCsp(args)
    
def checkFile(nomeFile, numberError):
    try:
        f = open(nomeFile)
        if ('/' in nomeFile):
            NameFileSplit = nomeFile.split('/')
            if( 
            os.path.splitext(nomeFile)[1] == '.xml'
            ):
                exitVar = True
        else:
            if( 
            os.path.splitext(nomeFile)[1] == '.xml'
            ):
                f.close()
    except IOError:
        if (numberError == 1):
            print("First file not found\nRemember add file extension (.xml)\n ")

        if (numberError == 2):
            print("Second file not found\nRemember add file extension (.xml)\n ")
        exit()  

def mergeFile():
    f = open(args.mf1,"r")
    e0f = len(f.readlines())
    f.close()

    f = open(args.mf1,"r")

    scriptSrc = []
    frameAncestors = []
    imgSrc = []
    connectSrc = []
    fontSrc = []
    defaultSrc = []
    baseUrl = []
    childSrc = []
    formAction = []	
    manifestSrc = []
    mediaSrc = []
    objectSrc = []
    styleSrc = []

    initCsp_Whitelist = '''<?xml version="1.0"?>
<csp_whitelist xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Csp/etc/csp_whitelist.xsd">
    <policies>
'''
    
    policyScriptStart = '''        <policy id="script-src">
            <values>
'''
    policyStyleStart = '''        <policy id="style-src">
            <values>
'''
    policyImgStart = '''        <policy id="img-src">
            <values>
'''
    policyConnectStart = '''        <policy id="connect-src">
            <values>
'''
    policyFontStart = '''        <policy id="font-src">
            <values>
'''
    policyFrameStart = '''        <policy id="frame-src">
            <values>
'''
    policyDefaultStart = '''        <policy id="default-Src">
            <values>
'''
    policyBaseStart = '''        <policy id="base-Url">
            <values>
'''
    policyChildStart = '''        <policy id="child-Src">
            <values>
'''
    policyFormStart = '''        <policy id="form-action">
            <values>
'''
    policyManifestStart = '''        <policy id="manifest-src">
            <values>
'''
    policyMediaStart = '''        <policy id="media-src">
            <values>
'''
    policyObjectStart = '''        <policy id="object-src">
            <values>
'''
    policyStop = '''            </values>
        </policy>
'''
    endCsp_Whitelist = '''    </policies>
</csp_whitelist>
'''

    while e0f > 0:
        line = f.readline()
                
        if ('<policy id="script-src">' in line):
            line = f.readline()
            e0f = e0f - 1 
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in scriptSrc):
                    scriptSrc.append(line)
                scriptSrc.append(line)
                line = f.readline()

        elif('<policy id="style-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in styleSrc):
                    styleSrc.append(line)
                line = f.readline()
        
        elif('<policy id="font-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in fontSrc):
                    fontSrc.append(line)
                line = f.readline()

        elif('<policy id="frame-ancestors">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in frameAncestors):
                    frameAncestors.append(line)
                line = f.readline()

        elif('<policy id="connect-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in connectSrc):
                    connectSrc.append(line)
                line = f.readline()

        elif('<policy id="img-src">' in line):
            e0f = e0f - 1
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in imgSrc):
                    imgSrc.append(line)
                line = f.readline()

        elif('<policy id="default-Src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in defaultSrc):
                    defaultSrc.append(line)
                line = f.readline()

        elif('<policy id="base-Url">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in baseUrl):
                    baseUrl.append(line)
                line = f.readline()

        elif('<policy id="child-Src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in childSrc):
                    childSrc.append(line)
                line = f.readline()

        elif('<policy id="manifest-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in manifestSrc):
                    manifestSrc.append(line)
                line = f.readline()

        elif('<policy id="media-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in mediaSrc):
                    mediaSrc.append(line)
                mediaSrc.append(line)
                line = f.readline()

        elif('<policy id="object-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in objectSrc):
                    objectSrc.append(line)
                line = f.readline()

        elif('<policy id="form-action">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in formAction):
                    formAction.append(line)
                line = f.readline()

        e0f = e0f - 1 
    f.close()

    f = open(args.mf2,"r")
    e0f = len(f.readlines())
    f.close()
    
    f = open(args.mf2,"r")
    line = f.readline()
     
    while e0f > 0:
        line = f.readline()
                
        if ('<policy id="script-src">' in line):
            line = f.readline()
            e0f = e0f - 1 
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in scriptSrc):
                    scriptSrc.append(line)
                scriptSrc.append(line)
                line = f.readline()

        elif('<policy id="style-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in styleSrc):
                    styleSrc.append(line)
                line = f.readline()
        
        elif('<policy id="font-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in fontSrc):
                    fontSrc.append(line)
                line = f.readline()

        elif('<policy id="frame-ancestors">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in frameAncestors):
                    frameAncestors.append(line)
                line = f.readline()

        elif('<policy id="connect-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in connectSrc):
                    connectSrc.append(line)
                line = f.readline()

        elif('<policy id="img-src">' in line):
            e0f = e0f - 1
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in imgSrc):
                    imgSrc.append(line)
                line = f.readline()

        elif('<policy id="default-Src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in defaultSrc):
                    defaultSrc.append(line)
                line = f.readline()

        elif('<policy id="base-Url">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in baseUrl):
                    baseUrl.append(line)
                line = f.readline()

        elif('<policy id="child-Src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in childSrc):
                    childSrc.append(line)
                line = f.readline()

        elif('<policy id="manifest-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in manifestSrc):
                    manifestSrc.append(line)
                line = f.readline()

        elif('<policy id="media-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in mediaSrc):
                    mediaSrc.append(line)
                mediaSrc.append(line)
                line = f.readline()

        elif('<policy id="object-src">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in objectSrc):
                    objectSrc.append(line)
                line = f.readline()

        elif('<policy id="form-action">' in line):
            line = f.readline()
            e0f = e0f - 1
            line = f.readline()
            while '</values>' not in line:
                line = line.split("type='host'>",1)[1]
                line = line.partition("</value>")[0]
                e0f = e0f - 1
                if (line not in formAction):
                    formAction.append(line)
                line = f.readline()

        e0f = e0f - 1 
        
    f.close()

    f = open("etc/csp_whitelist_merge.xml", "w")
    f.write(initCsp_Whitelist)
    idHost=0
    
    if (scriptSrc!=[]):
        f.write(policyScriptStart)
        for host in scriptSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (styleSrc!=[]):
        f.write(policyStyleStart)
        for host in styleSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (fontSrc!=[]):
        f.write(policyFontStart)
        for host in fontSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)


    if (frameAncestors!=[]):
        f.write(policyFrameStart)
        for host in frameAncestors:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)


    if (connectSrc!=[]):
        f.write(policyConnectStart)
        for host in connectSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)


    if (imgSrc!=[]):
        f.write(policyImgStart)
        for host in imgSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (defaultSrc!=[]):
        f.write(policyDefaultStart)
        for host in defaultSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (childSrc!=[]):
        f.write(policyChildStart)
        for host in childSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (formAction!=[]):
        f.write(policyFormStart)
        for host in formAction:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (manifestSrc!=[]):
        f.write(policyManifestStart)
        for host in manifestSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (mediaSrc!=[]):
        f.write(policyMediaStart)
        for host in mediaSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    if (objectSrc!=[]):
        f.write(policyObjectStart)
        for host in objectSrc:
            f.write("                <value id="+str(idHost)+" type='host'>"+host+"</value>\n")
            idHost= idHost + 1
        f.write(policyStop)

    f.write(endCsp_Whitelist)

    f.close()

if __name__ == "__main__":
    exitVar = False

    print( "Start CSP script ...")

    parser = argparse.ArgumentParser(description="CspGeneretor")

    #______________
    #|List Function|
    requiredName = parser.add_argument_group('Tool')

    #ClearFile
    requiredName.add_argument('-cc', 
                               default="out",
                               required=False, 
                               type=str, 
                               help='Run a log file cleanup (-cc 1)')
    #Step
    requiredName.add_argument('-st', 
                              default="out",
                              required=False, 
                              type=str, 
                              help='Run Step to Step CSP script (-st 1)')

    #Merge file 1
    requiredName.add_argument('-mf1', 
                            default="out",
                            required=False, 
                            type=str, 
                            help='Merge 2 whitelists (-mf1 "fileLog1.log")')
    #Merge file 2
    requiredName.add_argument('-mf2', 
                            default="out",
                            required=False, 
                            type=str, 
                            help='Merge 2 whitelists (-mf2 "fileLog2.log")')

    #createCsp
    parser.add_argument('--nameMod',     type=str, help="Name Module CSP")
    parser.add_argument('--fileLog',     default="default", type=str, help="Path file Log")
    parser.add_argument('--version',     default="1.0.0",  type=str, help="Version Module")
    parser.add_argument('--setId',       default=0,        type=int, help="Id value")
    parser.add_argument('--trt',         default=0,        type=int, help="Type report storefront")
    parser.add_argument('--tra',         default=0,        type=int, help="Type report admin")

    args = parser.parse_args()

    if (args.mf1!="out" and args.mf2!="out"):
        
        if (args.mf1 == args.mf2):
            print("The inserted white lists are equal and there is no need to merge")
        else:
            #checkFile1
            checkFile(args.mf1, 1)
            
            #checkFile2
            checkFile(args.mf2, 2)

            mergeFile()
    else:
        if (args.mf1!="out"):
            if (args.mf2=="out"):
                print ("Insert the second file")

        if (args.mf2!="out"):
            if (args.mf1=="out"):
                print ("Insert the first file")

    if(args.cc!='out'):
        args.cc=clearFileLog(args.cc)
         
    if (args.st!='out'):
        stepToStep(args)
    else:
        if (args.nameMod==None):
            print ("Insert the module name")        
            exitVar = True

        if (args.fileLog!="default"):
            try:
                f = open(args.fileLog)
                if ('/' in args.fileLog):
                    NameFileSplit = args.fileLog.split('/')
                    
                    if( 
                    os.path.splitext(NameFileSplit[len(NameFileSplit)-1])[1] == '.log' or
                    os.path.splitext(NameFileSplit[len(NameFileSplit)-1])[1] == '.txt'
                    ):
                        exitVar = True
                else:
                    if( 
                    os.path.splitext(args.fileLog)[1] == '.log' or
                    os.path.splitext(args.fileLog)[1] == '.txt'
                    ):
                        f.close()
                    
            except IOError:
                print("File not found\nRemember add file extension (.txt or .log)\n ")
            finally:
                f.close()
    
        if (exitVar==False):
            createCsp(args)
            print( "End CSP script ...")



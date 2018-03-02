# Written by Benjamin Jack Cullen

import os
import time
import requests
import subprocess
import win32com.client
from bs4 import BeautifulSoup

#Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

while True:

    try:
        # clear cmd and create title
        subprocess.call('cls', shell=True)
        print(46*'-')
        print(12*' '+'Def-Con Warning System')
        print(46*'-')
        
        # initialize gateway flags
        write_status = False
        defcon_change = False

        # configure BeautifulSoup
        url = ('http://www.defconlevel.com/')
        print('-source: defconlevel.com')
        rHead  = requests.get(url)
        data = rHead.text
        soup = BeautifulSoup(data, "html.parser")

        # use BeautifulSoup to crawl 'http://www.defconlevel.com/levels/'
        print('-gathering information')
        defcon_status = ''
        for link in soup.find_all('a'):
            href = (link.get('href'))
            if href != None:
                if 'http://www.defconlevel.com/levels/' in href:
                    defcon_status = href.replace('http://www.defconlevel.com/levels/', '')
                    defcon_status = defcon_status.replace('.php', '')
                    defcon_status = defcon_status.strip()
        print('-current status:', defcon_status)

        # create/edit temporary file to store previous def con status
        if not os.path.exists('./temporary/def_con_status.tmp'):
            print('-creating temporary file')
            open('./temporary/def_con_status.tmp', 'w').close()
            with open('./temporary/def_con_status.tmp', 'w') as fo:
                fo.writelines(defcon_status)
            fo.close()

        # read previous defcon status from temporary file
        with open('./temporary/def_con_status.tmp', 'r') as fo:
            print('-reading previouse defcon status')
            for line in fo:
                previous_defcon_status = line.strip()
            fo.close()

        # compare previous defcon status in temporary file to current status
        print('-comparing previous status with current status')
        if defcon_status != previous_defcon_status:
            print('-defcon status changed')
            defcon_num = defcon_status[-1:]
            previous_defcon_num = previous_defcon_status[-1:]

            # defcon_status is != previous_defcon_status so tell me!
            line = 'def con level changed too: ' + defcon_status
            speaker.Speak(line)

            # write new status to the temporary file
            with open('./temporary/def_con_status.tmp', 'w') as fo:
                print('-updating status file')
                fo.writelines(defcon_status)
            fo.close()
        elif defcon_status == previous_defcon_status:
            print('-status unchanged')
            
    except:
        time.sleep(5)
        pass
    time.sleep(5)

import json
import os
import subprocess
import sys
import zlib
import argparse
import signal
import time

from data.journals import JOURNALS
from data.monoco import MONOCO_SKILLS
from data.music import MUSIC
from data.pictos import DATA_PICTOS, DATA_PICTOS_DLC
from data.cosmetics import DATA_COSMETICS, DATA_COSMETICS_DLC
from data.weapons import DATA_WEAPONS, DATA_WEAPONS_DLC

SAVEFILE=None
DLC=True
OUTPUT_FOLDER=None

MONITOR=False
CHEATER=False

WRITE_OBS = False
WRITE_LS = False

ABORT_REQUESTED = False

KEY_JOURNALS = 'journals'
KEY_MUSIC = 'music'
KEY_FEET = 'feet'
KEY_PICTOS = 'pictos'
KEY_WEAPONS = 'weapons'
KEY_COSMETICS = 'cosmetics'
KEY_ALL = 'all'
KEY_GUSTAVE = 'Gustave'
KEY_LUNE = 'Lune'
KEY_MAELLE = 'Maelle'
KEY_SCIEL = 'Sciel'
KEY_VERSO = 'Verso'
KEY_MONOCO = 'Monoco'

data = {
  KEY_JOURNALS: [0,0],
  KEY_MUSIC: [0,0],
  KEY_FEET: [0,0],
  KEY_PICTOS: [0,0],
  KEY_WEAPONS: {
    KEY_ALL: [0,0],
    KEY_LUNE: [0,0],
    KEY_MAELLE: [0,0],
    KEY_SCIEL: [0,0],
    KEY_VERSO: [0,0],
    KEY_MONOCO: [0,0]
  },
  KEY_COSMETICS: {
    KEY_ALL: [0,0],
    KEY_GUSTAVE: [0,0],
    KEY_LUNE: [0,0],
    KEY_MAELLE: [0,0],
    KEY_SCIEL: [0,0],
    KEY_VERSO: [0,0],
    KEY_MONOCO: [0,0]
  }
}

missing = {}

ITER_WEAPONS = [
  (KEY_VERSO, 'V'),
  (KEY_LUNE, 'L'),
  (KEY_MAELLE, 'A'),
  (KEY_SCIEL, 'S'),
  (KEY_MONOCO, 'M')
]
ITER_WRITE_WEAPONS = [ KEY_VERSO, KEY_LUNE, KEY_MAELLE, KEY_SCIEL, KEY_MONOCO, KEY_ALL ]

ITER_COSMETICS = [
  (KEY_GUSTAVE, 'G'),
  (KEY_LUNE, 'L'),
  (KEY_MAELLE, 'A'),
  (KEY_SCIEL, 'S'),
  (KEY_VERSO, 'V'),
  (KEY_MONOCO, 'M')
]
ITER_WRITE_COSMETICS = [ KEY_GUSTAVE, KEY_LUNE, KEY_MAELLE, KEY_SCIEL, KEY_VERSO, KEY_MONOCO, KEY_ALL ]

PICTOS = None
WEAPONS = None
COSMETICS = None

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('savefile', help='E33 savefile, no auto-find, check "%%LOCALAPPDATA%%/Sandfall"')
  parser.add_argument('-o', '--out', help='Outputfolder, must exist, default is "out" subdirectory of the script')
  parser.add_argument('-d', '--dlc', action='store_true', help='Include DLC items (Thank You Update)')
  parser.add_argument('-m','--monitor', action='store_true', help='Don\'t return after a single pass, monitor the file for changes')
  parser.add_argument('-c','--cheater', action='store_true', help='Write file with the missing items to output folder')
  parser.add_argument('--obs', action='store_true', help='Write Textfiles for OBS to output folder.')
  parser.add_argument('--livesplit', action='store_true', help='Try to transmit data to Livesplit Websocket Server as custom variables.')
  args=parser.parse_args()
  global SAVEFILE
  SAVEFILE = args.savefile

  global DLC
  DLC = args.dlc

  global OUTPUT_FOLDER
  if args.out is None:
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__),'out')
  else:
    OUTPUT_FOLDER = args.out
  if not os.path.isdir(OUTPUT_FOLDER):
    print('Output folder doesn\'t exist')
    sys.exit(1)

  global MONITOR
  MONITOR = args.monitor
  global CHEATER
  CHEATER = args.cheater

  global WRITE_OBS
  WRITE_OBS = args.obs
  global WRITE_LS
  WRITE_LS = args.livesplit

  global PICTOS
  global WEAPONS
  global COSMETICS
  if DLC:
    PICTOS = DATA_PICTOS_DLC
    WEAPONS = DATA_WEAPONS_DLC
    COSMETICS = DATA_COSMETICS_DLC
  else:
    PICTOS = DATA_PICTOS
    WEAPONS = DATA_WEAPONS
    COSMETICS = DATA_COSMETICS

  global data
  data[KEY_JOURNALS][1] = len(JOURNALS)
  data[KEY_MUSIC][1] = len(MUSIC)
  data[KEY_FEET][1] = len(MONOCO_SKILLS)
  data[KEY_PICTOS][1] = len(PICTOS)
  n_total = 0
  for it in ITER_WEAPONS:
    temp = len(WEAPONS[it[1]])
    n_total += temp
    data[KEY_WEAPONS][it[0]][1] = temp
  data[KEY_WEAPONS][KEY_ALL][1] = n_total

  n_total = 0
  for it in ITER_COSMETICS:
    temp = len(COSMETICS[it[1]])
    n_total += temp
    data[KEY_COSMETICS][it[0]][1] = temp
  n_total += len(COSMETICS['shared'])
  data[KEY_COSMETICS][KEY_ALL][1] = n_total

  if MONITOR:
    last_ts_checked = 0
    last_data_written = ''
    last_file_existance = None
    signal.signal(signal.SIGINT, signal_handler)

    while True:
      if ABORT_REQUESTED:
        print('Exiting')
        sys.exit(0)
      doUpdate = False
      fileExists = os.path.exists(SAVEFILE)
      if last_data_written == '': # first iteration
        doUpdate = True
      elif fileExists != last_file_existance:
        last_file_existance = fileExists
        last_ts_checked = 0
        doUpdate = True
      if fileExists:
        modificationTime = os.path.getmtime(SAVEFILE)
        if (modificationTime > last_ts_checked):
          last_ts_checked = modificationTime
          doUpdate = True
      if doUpdate:
        print('New version of file detected')
        if updateData():
          temp_data_serialized = json.dumps(data,sort_keys=True)
          if temp_data_serialized != last_data_written:
            writeData()
            last_data_written = temp_data_serialized
            print('Changes to tracked items detected - data updated')
        else:
          last_ts_checked = 0 # try again next iteration
      time.sleep(0.5)
  else:
    if not os.path.exists(SAVEFILE):
      print('Save file doesn\'t exist, which is unexpected for non-monitor mode')
      sys.exit(1)
    updateData()
    writeData()
    print(data)

def updateData() -> bool:
  try:
    global data
    global missing
    read_successful = False
    if os.path.exists(SAVEFILE):
      res_uesave = subprocess.run(
        [
          os.path.join(os.path.dirname(__file__),'bin','uesave.exe'),
          'to-json',
          '-i',
          SAVEFILE
        ], stdout=subprocess.PIPE )
      read_successful = res_uesave.returncode == 0
      if read_successful:
        save_data = json.loads(res_uesave.stdout.decode('utf-8'))
    
    missing = {}
    if not read_successful:
      data[KEY_JOURNALS][0] = 0
      data[KEY_MUSIC][0] = 0
      data[KEY_FEET][0] = 0
      data[KEY_PICTOS][0] = 0
      data[KEY_WEAPONS][KEY_VERSO][0] = 0
      data[KEY_WEAPONS][KEY_LUNE][0] = 0
      data[KEY_WEAPONS][KEY_MAELLE][0] = 0
      data[KEY_WEAPONS][KEY_SCIEL][0] = 0
      data[KEY_WEAPONS][KEY_MONOCO][0] = 0
      data[KEY_WEAPONS][KEY_ALL][0] = 0
      data[KEY_COSMETICS][KEY_GUSTAVE][0] = 0
      data[KEY_COSMETICS][KEY_LUNE][0] = 0
      data[KEY_COSMETICS][KEY_MAELLE][0] = 0
      data[KEY_COSMETICS][KEY_SCIEL][0] = 0
      data[KEY_COSMETICS][KEY_VERSO][0] = 0
      data[KEY_COSMETICS][KEY_MONOCO][0] = 0
      data[KEY_COSMETICS][KEY_ALL][0] = 0
    else:
      data[KEY_FEET][0] = 0
      for char in save_data["root"]["properties"]["CharactersCollection_0"]:
        if char["key"] != "Monoco":
          continue
        unlocked_skills = set(char["value"]["UnlockedSkills_197_FAA1BD934F68CFC542FB048E3C0F3592_0"])
        data[KEY_FEET][0] = len(unlocked_skills & MONOCO_SKILLS)
        if CHEATER & (data[KEY_FEET][0] < data[KEY_FEET][1]):
          missing[KEY_FEET] = sorted(list(MONOCO_SKILLS - unlocked_skills))
        break
      inventory = set(invItem["key"] for invItem in save_data["root"]["properties"]["InventoryItems_0"])
      data[KEY_JOURNALS][0] = len(inventory & JOURNALS)
      if CHEATER & (data[KEY_JOURNALS][0] < data[KEY_JOURNALS][1]):
        missing[KEY_JOURNALS] = sorted(list(JOURNALS - inventory))
      data[KEY_MUSIC][0] = len(inventory & MUSIC)
      if CHEATER & (data[KEY_MUSIC][0] < data[KEY_MUSIC][1]):
        missing[KEY_MUSIC] = sorted(list(MUSIC - inventory))
      data[KEY_PICTOS][0] = len(inventory & PICTOS)
      if CHEATER & (data[KEY_PICTOS][0] < data[KEY_PICTOS][1]):
        missing[KEY_PICTOS] = sorted(list(PICTOS - inventory))
      n_total = 0
      temp_missing = []
      for it in ITER_WEAPONS:
        temp = len(inventory & WEAPONS[it[1]])
        n_total += temp
        data[KEY_WEAPONS][it[0]][0] = temp
        if CHEATER:
          temp_missing += sorted(list(WEAPONS[it[1]] - inventory))
      data[KEY_WEAPONS][KEY_ALL][0] = n_total
      if CHEATER & (data[KEY_WEAPONS][KEY_ALL][0] < data[KEY_WEAPONS][KEY_ALL][1]):
        missing[KEY_WEAPONS] = temp_missing
      n_total = 0
      temp_missing = []
      for it in ITER_COSMETICS:
        temp = len(inventory & COSMETICS[it[1]])
        n_total += temp
        data[KEY_COSMETICS][it[0]][0] = temp
        if CHEATER:
          temp_missing += sorted(list(COSMETICS[it[1]] - inventory))
      for grp in COSMETICS['shared']:
        if len(inventory & grp) > 0:
          n_total += 1
      data[KEY_COSMETICS][KEY_ALL][0] = n_total
      if CHEATER & (data[KEY_COSMETICS][KEY_ALL][0] < data[KEY_COSMETICS][KEY_ALL][1]):
        missing[KEY_COSMETICS] = temp_missing
    return True
  except:
    return False

def writeData():
  writeDataHelper(data[KEY_JOURNALS], KEY_JOURNALS)
  writeDataHelper(data[KEY_MUSIC], KEY_MUSIC)
  writeDataHelper(data[KEY_FEET], KEY_FEET)
  writeDataHelper(data[KEY_PICTOS], KEY_PICTOS)
  for it in ITER_WRITE_WEAPONS:
    writeDataHelper(data[KEY_WEAPONS][it], KEY_WEAPONS + '_' + it, it==KEY_ALL)
  for it in ITER_WRITE_COSMETICS:
    writeDataHelper(data[KEY_COSMETICS][it], KEY_COSMETICS + '_' + it, it==KEY_ALL)
  with open(os.path.join(OUTPUT_FOLDER, 'data.json'),'w',encoding="utf-8") as f:
    json.dump(data, f, indent=2)
  if CHEATER:
    with open(os.path.join(OUTPUT_FOLDER, 'missing.json'),'w',encoding="utf-8") as f:
      json.dump(missing, f, indent=2)

def writeDataHelper(num_arr, basename, output_LS = True):
  percentage = "%0.2f" % (100*num_arr[0]/num_arr[1]) + '%'
  if WRITE_OBS:
    with open(os.path.join(OUTPUT_FOLDER, 'obs_' + basename + '_slash.txt'),'w',encoding="utf-8") as f:
      f.write(str(num_arr[0]) + '/' + str(num_arr[1]))
    with open(os.path.join(OUTPUT_FOLDER, 'obs_' + basename + '_raw.txt'),'w',encoding="utf-8") as f:
      f.write(str(num_arr[0]))
    with open(os.path.join(OUTPUT_FOLDER, 'obs_' + basename + '_pct.txt'),'w',encoding="utf-8") as f:
      f.write(percentage)
  if WRITE_LS and output_LS:
    pass

def signal_handler(sig, frame):
  global ABORT_REQUESTED
  ABORT_REQUESTED = True

if __name__ == "__main__":
  main()

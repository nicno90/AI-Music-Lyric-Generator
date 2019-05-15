import Generate as gen
import GenerateSong as genSong
import CreateModels as cModels
import os
import sys


def generateModels(filename):
  if filename[-4:] != '.csv':
    print('Error: Invalid file type using default')
    filename = 'Data/songdata.csv'
  cModels.run(filename)

def fileExsists(path):
  return os.path.isfile(path)

def handelgenMainModel(inp):
  if len(inp) == 0:
    generateMainModel(['-txt','sampleArtists.txt'])
  elif inp[0] == '-sample':
    generateMainModel(['-txt','sampleArtists.txt'])
  elif len(inp) >= 1:
    generateMainModel(inp)
  else:
    print('Error: Missing paramaters. Running defaults')
    generateMainModel(['-txt','sampleArtists.txt'])

def generateMainModel(args):
  gen.run(args)

def setMainModel(filename):
  if (not fileExsists(filename)):
    print('Cant find Model at: ', filename)
    return
  f = open(filename, 'r')
  json = f.readline()
  amount = f.readline()
  print('Found model with',f.readline(),'songs')
  if f.readline() != '':
    print('Weird format: Possible data loss')
  f.close()
  f = open('models/main.model', 'w+')
  f.write(json)
  f.close()
  print('main.model changed')

def setArtist(args):
  artist = cModels.formatArtistName(args)
  if (not fileExsists('models/'+artist+'.model')):
    print('Cant find Model at: ', 'models/'+artist+'.model')
    return
  f = open('models/'+artist+'.model', 'r')
  json = f.readline()
  amount = int(f.readline())
  print('Found model with',amount,'songs')
  if f.readline() != '':
    print('Weird format: Possible data loss')
  f.close()
  f = open('models/main.model', 'w+')
  f.write(json)
  f.close()
  print('main.model changed')

def printHelp():
  f = open('help.txt')
  line = f.readline()
  while line != '':
    print(line)
    line = f.readline()
  f.close()


def handleCommand(cmd):
  cmdA = cmd.split()
  if (cmd == '-h' or cmd == '-help'):
    printHelp()
  elif (cmdA[0] == 'newSong'):
    print()
    if len(cmdA) < 2:
      print('Error: missing song length param')
    genSong.run('models/main.model', int(cmdA[1]))
  elif (cmd == 'setup'):
    setup()
  elif (cmdA[0] == 'setMainModel'):
    if (len(cmdA) != 2):
      print('Error: Strange params:\nShould be: setMainModel path/modelName.model')
    setMainModel(cmdA[1])
  elif (cmdA[0] == 'newModel'):
    handelgenMainModel(cmdA[1:])
  elif (cmdA[0] == 'setArtist'):
    if (len(cmdA) < 2):
      print('Error: Strange params:\nShould be: setArtist Artist_Name')
    setArtist(cmdA[1:])
  elif (cmdA[0] == 'artistExsist'):
    if (len(cmdA) != 2):
      print('Error: Strange params:\nShould be: artistsExsist Artist_Name')
    if (fileExsists('model/'+cmd[1]+'.model')):
      print('Found Artist')
    else:
      print('Counldn\'t find artist')
  else:
    print('Unkown Command')

def setup():
  print('>Generate Models of Data/songsdata.csv?')
  print(">(recomended dif this is your first time running or new data has been entered)")
  inp = input('(y/n)>')
  if (inp == 'y'):
    cModels.run('Data/songdata.csv')
  elif (inp != 'n'):
    print('Error: Expected "y" or "no"')
    return
  print('\n>Generate Main Model:')
  print('>(leave blank to set model from sampleArtists.txt)')
  inp = input('>')
  handelgenMainModel(inp.split())

if __name__ == '__main__':
  print(">Welcome to the Lyric Generator! (-h for help)")
  inp = input('>')
  while inp != '-q' and inp != 'quit':
    handleCommand(inp)

    inp = input('>')
  print('>Closing Lyric Generator.')
  
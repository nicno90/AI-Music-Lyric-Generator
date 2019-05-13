import markovify as mkfy
import sys


def readModel(filename):
  f = open(filename, 'r')
  json = f.readline()
  if f.readline() != '':
    print('Weird format: Possible data loss')
  f.close()
  model = mkfy.Text.from_json(json)
  return model

def newSong(model, length):
  print('New Song:')
  for i in range(length):
    print(model.make_sentence())


if len(sys.argv) != 3:
  print('Error: python GenerateSong.py [ModelName] [songLength]')
else:
  print(sys.argv)
  model = readModel(sys.argv[1])
  length = int(sys.argv[2])
  newSong(model, length)


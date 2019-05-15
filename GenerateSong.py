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
  for i in range(length):
    sent = model.make_sentence().replace('*', '\'')
    # sent = sent.replace('#', '\n')
    print(sent)

def run(model, length):
  newSong(readModel(model), length)

def main():
  if len(sys.argv) != 3:
    print('Error: python GenerateSong.py [ModelName] [songLength]')
  else:
    print(sys.argv)
    model = readModel(sys.argv[1])
    length = int(sys.argv[2])
    newSong(model, length)

#main()
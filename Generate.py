import markovify as mkfy
import os
import time as time
import sys

def formatArtistName(artist):
  artist = artist.replace(' ', '_')
  artist = artist.replace('.', '')
  return artist

def handelArguments(args=['-txt', 'sampleArtists.txt']):
  dirc = 'models/'
  dic = 'artistsIndex.idx'
  artists = []
  search = []
  print('args:',args)
  if (len(args) > 0):
    if (len(args) > 1):
      if '-txt' in args:
        index = args.index('-txt')
        args.remove('-txt')
        bands = args[index]
        args.remove(bands)
        f = open(bands, 'r')
        txt = f.readline().split()
        i = 0
        while i < len(txt):
          if (txt[i][0] == '"'):
            out = txt[i][1:]
            while txt[i][-1] != '"':
              i += 1
              out = out +'_'+ txt[i]
            out = out[:-1]
            #print('out:',out)
            search.append(out)
          else:
            #print('txt[i]',txt[i])
            search.append(txt[i])
          i += 1
    search.extend(args)
    print('Searching for:', search)
    for i in range(len(search)):
      if (os.path.isfile(dirc+formatArtistName(search[i])+'.model')):
        print('+Found', formatArtistName(search[i]), 'in Models')
        artists.append(formatArtistName(search[i]))
      else:
        print('-Could not find',search[i])
  return dirc, dic, artists

def readArtists(dirc, dic):
  f = open(dirc+dic, 'r')
  artist = f.readline()[:-1]
  artists = []
  while artist != '':
    artists.append(artist)
    artist = f.readline()[:-1]
  return artists

def readModel(filename):
  f = open(filename, 'r')
  json = f.readline()
  amount = f.readline()
  if f.readline() != '':
    print('Weird format: Possible data loss')
  f.close()
  model = mkfy.Text.from_json(json)
  return model, amount

def makeModel(dirc, search):
  model = None
  total = 0
  print('Amount of Artist:', len(search))
  for i in range(len(search)):
    #if (artists[i] in search):
    m, amount = readModel(dirc+search[i]+'.model')
    amount = int(amount)
    print(i,':\tAdding:', amount, '\tfrom artist:\t',search[i])
    if model == None:
      model = m
      total += amount
    else:
      model = mkfy.combine([model, m], [total, amount])
      total += amount
    m = None
  print('Amount of Songs:', total)
  return model


def saveModel(model, dirc, name):
  print('Saving:', dirc+name+'.model')
  f = open(dirc+name+'.model', 'w+')
  json = model.to_json()
  f.write(json)
  f.close()

def run(args):
  start = time.time()
  dirc, dic, search = handelArguments(args)
  if (type(dic) == int): return -1
  artists = readArtists(dirc, dic)
  model = makeModel(dirc, search)
  saveModel(model, dirc, 'main')
  print('Time:',int(time.time() - start),'seconds')

def main():
  start = time.time()
  dirc, dic, search = handelArguments(sys.argv[1:])
  if (type(dic) == int): return -1
  artists = readArtists(dirc, dic)
  model = makeModel(dirc, artists, search)
  saveModel(model, dirc, 'main')
  print('Time:',(time.time() - start))

# main()
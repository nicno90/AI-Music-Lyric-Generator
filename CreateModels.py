import markovify as mkfy
import sys


def fixLine(line):
  orig = line
  line = line.replace('(', '')
  line = line.replace(')', '')
  line = line.replace('[', '')
  line = line.replace(']', '')
  line = line.replace('\'', '*')
  line = line.replace('"', '')
  return line


def readSong(file):
  # line = file.readline()[1:]
  text = ""
  
  line = file.readline()
  #print('quote at song start:' ,line)
  line = file.readline()
  #print('first line of song:' ,line)
  while line != "\"--\n":
    text = text + fixLine(line) + ' #'
    # print('readSong: line:', line)
    line = file.readline()
    #print(len(line))
    if ((line == '  \n' or line=='\n') and (text[-3] != '.' or text[-3] != '!' or text[-3] != '?')):
      text = text[:-3] + '.\n'
      #print(line)
  if line != "\"--\n":
    print('Error:',line)
  # print('readSong: nextInfo:', line)

  # print('After:\n',text)
  return mkfy.Text(text, retain_original=False)
  #return mkfy.NewlineText(text, retain_original=False)
  

def concatArtist(file, info):
  artist = info[0]
  # print('New Artist:', artist)
  if artist == "\"--\n":
      raise Exception('Error: Artist name is marker: "--')
      return None
  models = []
  amnt = 0
  while artist == info[0]:
    model = readSong(file)
    info = file.readline().split(',')
    models.append(model)
    amnt += 1
  print('Found\t', amnt, '\tsongs from\t', artist)
  return mkfy.combine(models), info, amnt

def formatArtistName(info):
  # print('info[0]:', info)
  artist = info[0]
  if artist[0] == "\"":
    for i in range(1, len(info)):
      artist = artist +'_' + info[i]
      if info[i][-1] == "\"":
        artist = artist[1:-1]
        #print('Fixed artist name:', info, artist)
        break
  artist = artist.replace(' ', '_')
  artist = artist.replace('.', '')
  return artist

def concatData(file):
  models = []
  info = file.readline().split(',')
  artists = []
  songs = []
  while info[0] != "END_OF_DATA":
    artist = formatArtistName(info)

    if artist in artists:
      index = artists.index(artist)
      model, info, amount = concatArtist(file, info)
      models[index] = mkfy.combine([models[index], model])
      songs[index] = songs[index]+amount
      # print('Adding to artist[',index,']:',amount,'\tmore songs to', artist)
    else:
      artists.append(artist)
      model, info, amount = concatArtist(file, info)
      # print('Found new artist[',len(artists)-1,']:',amount,'\tsongs from', artist)
      songs.append(amount)
      models.append(model)
    
  return models, artists, songs

def writeModelsFiles(models, artists, songs, artistFilename='artistsIndex.idx', dir='models/'):
  print('Saving Artists...')
  if len(models) != len(artists):
    print('Error: Model:',len(models),'Artists',len(artists))
  f = open(dir+artistFilename, 'w+')
  for i in range(len(artists)):
    f.write(artists[i]+'\n')
  f.close()
  print('Index Saved!\nSaving Models:')
  for i in range(len(models)):
    print('Saving:',dir+artists[i]+'.model')
    f = open(dir+artists[i]+'.model', 'w+')
    f.write(models[i].to_json() + '\n' + str(songs[i]))
    f.close()
  print('Models Saved!')

def run(filename):
  print('Reading', filename)
  print('Loading... (this might take a minute or 2)')
  file = open(filename, 'r')
  headers = file.readline()
  # print('Headers:', headers)
  models, artists, songs = concatData(file)
  print('Found', len(artists), len(models), 'artists in the data-set!')
  file.close()
  # fullModel = mkfy.combine(models, weights)
  writeModelsFiles(models, artists, songs)
  print('Models have been generated')

def main():
  file = open('Data/songdata.csv', 'r')
  headers = file.readline()
  # print('Headers:', headers)
  models, artists, songs = concatData(file)
  print('Found', len(artists), len(models), 'artists in the data-set!')
  file.close()
  # fullModel = mkfy.combine(models, weights)
  writeModelsFiles(models, artists, songs)
  print('Models have been generated')

# main()
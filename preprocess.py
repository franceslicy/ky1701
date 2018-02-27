import sys
import math
from itertools import groupby
from pprint import *
from music21 import *

def fillRestAndQuantify(pn_list, isTrain=False):
	# prev note list
	prev = None
	prev_list = []
	for (beat, n) in pn_list:
		prev_list.append((beat, prev))
		if not n.isRest:
			prev = (beat, n)
	# next note list
	nex = None
	nex_list = []
	for (beat, n) in pn_list[::-1]:
		nex_list.append((beat, nex))
		if not n.isRest:
			nex = (beat, n)
	# fill rest
	prev_dict = dict(prev_list)
	nex_dict = dict(nex_list)
	out_list = []
	label = None
	for (beat, n) in pn_list:
		filled_n = None
		if not n.isRest:
			filled_n = n
		else:
			prev = prev_dict[beat]
			nex = nex_dict[beat]
			if prev is None:
				if nex is None:
					filled_n = None
				else:
					filled_n = nex[1]
			else:
				if nex is None:
					filled_n = prev[1]
				else:
					# compare prev & nex
					if math.floor(beat) == math.floor(prev[0]):
						filled_n = prev[1]
					elif math.floor(beat) == math.floor(nex[0]):
						filled_n = nex[1]
					elif beat-prev[0] >= nex[0]-beat:
						filled_n = prev[1]
					else:
						filled_n = nex[1]
		
		if filled_n is not None:
			if filled_n.isChord:
				for filled_subn in filled_n:
					out_list.append((beat, filled_subn.pitch.midi%12))
			else:
				out_list.append((beat, filled_n.pitch.midi%12))

		# output chord label for train mode
		if isTrain:
			if len(n.lyrics)==1 and n.lyrics[0].text:
				label = n.lyrics[0].text
			out_list.append((beat, label))

	return out_list


# output to tuple: 
# training mode: ((measureNumber, beat), [12-param vector], label)
# apply mode: ((measureNumber, beat), [12-param vector])
def parameterize(measure, beat, param_list, isTrain=False):
	vector = [0]*12
	label = None
	for param in param_list:
		if isinstance(param, int) and param >= 0 and param <= 11:
			vector[param] = 1

		# output chord label for train mode
		if isTrain and isinstance(param, str):
			label = param

	if isTrain:
		return ((measure,beat),vector,label)
	else:
		return ((measure,beat),vector)



def preProcess(s, isTrain=False):
	measureNumber = len(s.parts[0].getElementsByClass('Measure'))
	# preProcess on score
	n_list = s.recurse().getElementsByClass(note.Note)
	for n in n_list:
		if n.duration.isGrace:
			s.remove(n, recurse=True)
	ns = figuredBass.checker.getVoiceLeadingMoments(s)
	ns = ns.voicesToParts()

	normalized_data = []
	for mNumber in range(1,measureNumber+1):
		m = ns.measure(mNumber)
		n_list = []
		label_list = []
		for p in m.parts:
			pn_list = [(n.beat,n) for n in p.recurse().getElementsByClass('GeneralNote')]
			pn_list = fillRestAndQuantify(pn_list, isTrain)
			n_list.extend(pn_list)
		n_list = sorted(n_list, key=lambda x: x[0])
		beat_list = [(beat, [pitch for _, pitch in g]) for beat, g in groupby(n_list, key=lambda x: x[0])]
		for (beat, param_list) in beat_list:
			normalized_data.append(parameterize(mNumber, beat, param_list, isTrain))
	return normalized_data

xmlName = sys.argv[1]
isTrain = sys.argv[2] if len(sys.argv) == 3 else False
s = converter.parse(xmlName)
data = preProcess(s, isTrain=="train");
pprint(data);

# notes:
# n.addLyric("text"): add chord label to the note
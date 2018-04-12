import csv
class ProgressionBank(object):

	# Object for accessing progression table csv
	# provide function for examining major or minor progression is valid or not
	def __readCSV(self, source):
		bank = {}
		keys = []
		with open(source, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if row[0] == "KEY":
					keys = list(row)
				else:
					bank[row[0]] = list(row)
		return (bank, keys)

	def verifyMajor(self, before=None, after=None):
		return self.__verify(bank=self._majorBank, keys=self._majorKeys, before=before, after=after)

	def verifyMinor(self, before=None, after=None):
		return self.__verify(bank=self._minorBank, keys=self._minorKeys, before=before, after=after)

	def __verify(self, bank, keys, before=None, after=None):
		if before is None or after is None or before == "" or after == "":
			return "NULL"
		if before in bank:
			try:
				index = keys.index(after)
			except ValueError:
				index = keys.index(before)
			return bank[before][index]
		return "NULL"

	def __init__(self):
		majorSource = "ChordIdentifier/majorProgression.csv"
		minorSource = "ChordIdentifier/minorProgression.csv"
		(self._majorBank, self._majorKeys) = self.__readCSV(source=majorSource)
		(self._minorBank, self._minorKeys) = self.__readCSV(source=minorSource)

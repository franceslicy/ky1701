# Task 1

## Overview
* task1.1: print scale notes of a key
* task1.2: print chord notes of a given key and chord number
* task1.3: print possible chord numbers with a given key and chord notes

### task1.1
In the terminal, run the script with the following pattern
```
<your python3 executable> task1_1.py <key> <scale>
```
for example
```
python3.6 task1_1.py Db major
```
This will print the Db major scale notes.
You can use keys from C to B and major/minor scale as the input.

### task1.2
In the terminal, run the script with the following pattern
```
<your python3 executable> task1_2.py <key> <scale> <chord>
```
for example
```
python3.6 task1_2.py Db major I
```
This will print the Db major tonic chord.
You can use keys from C to B and major/minor scale as the input.

For the chord, the program is currently working for major and minor triad chords (I, II ..., VII). It can be further developed for other diminished/seventh chords.

### task1.3
In the terminal, run the script with the following pattern
```
<your python3 executable> task1_3.py <key> <chord notes splited by whitespaces>
```
for example
```
python3.6 task1_3.py C C E G
```
This will print all possible chord numbers for the given key and chord notes
You can use keys from C to B and any notes as the input.

## Progress
### 24/9
* Finish the first two subtasks

### 07/10
* Revise the code for the first two subtasks
* Finish the total match case for the third subtask
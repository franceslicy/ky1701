major_chord_tree = {
 'M6': {'M7': {'M2': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P4': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'result': ['VII 7']},
       'P1': {'M2': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'M3': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'P4': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'P5': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['II 7', 'IV', 'VI']},
       'M2': {'M7': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P1': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'P4': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'result': ['II', 'VII 7']},
       'M3': {'P1': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'P4': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P5': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['IV 7', 'VI']},
       'P4': {'M7': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P1': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'M2': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'M3': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['II', 'IV', 'VII 7']},
       'P5': {'P1': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M3': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['VI 7']},
       'result': []},
 'm6': {'M7': {'M2': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P4': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'result': ['VII dim7']},
        'P1': {'M2': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'result': ['VI b']},
        'M2': {'M7': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P4': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'A4': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre', 'VII dim7']},
        'm2': {'P4': {'result': ['II b']}, 'result': ['II b']},
        'm3': {'P1': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
               'A4': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI b']},
        'P4': {'M7': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'M2': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'm2': {'result': ['II b']},
              'result': ['II b', 'VII dim7']},
        'A4': {'P1': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
               'M2': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
               'm3': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ita']},
        'result': []},
 'M7': {'M6': {'M2': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P4': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'result': ['VII 7']},
       'm6': {'M2': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P4': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'result': ['VII dim7']},
       'P1': {'M3': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'P5': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'result': ['I 7']},
       'M2': {'M6': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'm6': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M3': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P4': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P5': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'result': ['III 7', 'V', 'VII']},
       'M3': {'P1': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'M2': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P5': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'result': ['I 7', 'III']},
       'P4': {'M6': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'm6': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M2': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P5': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['V 7', 'VII']},
       'P5': {'P1': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'M2': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'M3': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'P4': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['I 7', 'III', 'V']},
       'result': []},
 'P1': {'M6': {'M2': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'M3': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'P4': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'P5': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['II 7', 'IV', 'VI']},
       'm6': {'M2': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'result': ['VI b']},
       'M7': {'M3': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'P5': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'result': ['I 7']},
       'M2': {'M6': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'm6': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'P4': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'A4': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'result': ['II 7', 'VI Fre']},
       'M3': {'M6': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'M7': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'P4': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P5': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'result': ['I', 'IV 7', 'VI']},
       'm3': {'m6': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI b']},
       'P4': {'M6': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'M2': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'M3': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['II 7', 'IV']},
       'A4': {'m6': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'M2': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI Ita']},
       'P5': {'M6': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M7': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'M3': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'result': ['I', 'VI 7']},
       'result': []},
 'M2': {'M6': {'M7': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P1': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'P4': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'result': ['II', 'VII 7']},
       'm6': {'M7': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P4': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'A4': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre', 'VII dim7']},
       'M7': {'M6': {'P4': {'result': ['VII 7']}, 'result': ['VII 7']},
             'm6': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M3': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P4': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P5': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'result': ['III 7', 'V', 'VII']},
       'P1': {'M6': {'P4': {'result': ['II 7']}, 'result': ['II 7']},
             'm6': {'A4': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'P4': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'A4': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'result': ['II 7', 'VI Fre']},
       'M3': {'M7': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P5': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'result': ['III 7']},
       'P4': {'M6': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'm6': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M7': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P1': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'P5': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['II', 'V 7', 'VII']},
       'A4': {'m6': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P1': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre']},
       'P5': {'M7': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'M3': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'P4': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['III 7', 'V']},
       'result': []},
 'm2': {'m6': {'P4': {'result': ['II b']}, 'result': ['II b']},
        'P4': {'m6': {'result': ['II b']}, 'result': ['II b']},
        'result': []},
 'M3': {'M6': {'P1': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'P4': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P5': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['IV 7', 'VI']},
       'M7': {'P1': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'M2': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P5': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'result': ['I 7', 'III']},
       'P1': {'M6': {'P4': {'result': ['IV 7']},
                   'P5': {'result': ['VI 7']},
                   'result': ['IV 7', 'VI']},
             'M7': {'P5': {'result': ['I 7']}, 'result': ['I 7']},
             'P4': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P5': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'result': ['I', 'IV 7', 'VI']},
       'M2': {'M7': {'P5': {'result': ['III 7']}, 'result': ['III 7']},
             'P5': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'result': ['III 7']},
       'P4': {'M6': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P1': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['IV 7']},
       'P5': {'M6': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M7': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'P1': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'M2': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'result': ['I', 'III', 'VI 7']},
       'result': []},
 'm3': {'m6': {'P1': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
               'A4': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI b']},
        'P1': {'m6': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI b']},
        'A4': {'m6': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'P1': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ger']},
        'result': []},
 'P4': {'M6': {'M7': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'P1': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'M2': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'M3': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['II', 'IV', 'VII 7']},
       'm6': {'M7': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'M2': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'm2': {'result': ['II b']},
              'result': ['II b', 'VII dim7']},
       'M7': {'M6': {'M2': {'result': ['VII 7']}, 'result': ['VII 7']},
             'm6': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M2': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P5': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['V 7', 'VII']},
       'P1': {'M6': {'M2': {'result': ['II 7']},
                   'M3': {'result': ['IV 7']},
                   'result': ['II 7', 'IV']},
             'M2': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'M3': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['II 7', 'IV']},
       'M2': {'M6': {'M7': {'result': ['VII 7']},
                   'P1': {'result': ['II 7']},
                   'result': ['II', 'VII 7']},
             'm6': {'M7': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M7': {'M6': {'result': ['VII 7']},
                   'm6': {'result': ['VII dim7']},
                   'P5': {'result': ['V 7']},
                   'result': ['V 7', 'VII']},
             'P1': {'M6': {'result': ['II 7']}, 'result': ['II 7']},
             'P5': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['II', 'V 7', 'VII']},
       'm2': {'m6': {'result': ['II b']}, 'result': ['II b']},
       'M3': {'M6': {'P1': {'result': ['IV 7']}, 'result': ['IV 7']},
             'P1': {'M6': {'result': ['IV 7']}, 'result': ['IV 7']},
             'result': ['IV 7']},
       'P5': {'M7': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'M2': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['V 7']},
       'result': []},
 'A4': {'m6': {'P1': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
               'M2': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
               'm3': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ita']},
        'P1': {'m6': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'M2': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI Ita']},
        'M2': {'m6': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P1': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre']},
        'm3': {'m6': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'P1': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ger']},
        'result': []},
 'P5': {'M6': {'P1': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M3': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'result': ['VI 7']},
       'M7': {'P1': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'M2': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'M3': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'P4': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['I 7', 'III', 'V']},
       'P1': {'M6': {'M3': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M7': {'M3': {'result': ['I 7']}, 'result': ['I 7']},
             'M3': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'result': ['I', 'VI 7']},
       'M2': {'M7': {'M3': {'result': ['III 7']},
                   'P4': {'result': ['V 7']},
                   'result': ['III 7', 'V']},
             'M3': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'P4': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['III 7', 'V']},
       'M3': {'M6': {'P1': {'result': ['VI 7']}, 'result': ['VI 7']},
             'M7': {'P1': {'result': ['I 7']},
                   'M2': {'result': ['III 7']},
                   'result': ['I 7', 'III']},
             'P1': {'M6': {'result': ['VI 7']},
                   'M7': {'result': ['I 7']},
                   'result': ['I', 'VI 7']},
             'M2': {'M7': {'result': ['III 7']}, 'result': ['III 7']},
             'result': ['I', 'III', 'VI 7']},
       'P4': {'M7': {'M2': {'result': ['V 7']}, 'result': ['V 7']},
             'M2': {'M7': {'result': ['V 7']}, 'result': ['V 7']},
             'result': ['V 7']},
       'result': []},
 'result': []
}

minor_chord_tree = {
 'M6': {'P1': {'P4': {'result': ['IV +']}, 'result': ['IV +']},
       'P4': {'P1': {'result': ['IV +']}, 'result': ['IV +']},
       'result': []},
 'm6': {'M7': {'M2': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P4': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'result': ['VII dim7']},
        'P1': {'M2': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
              'm3': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'P4': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
              'A4': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'result': ['II 7', 'IV', 'VI b']},
        'M2': {'M7': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
              'P4': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
              'A4': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['II', 'VI Fre', 'VII dim7']},
        'm2': {'P4': {'result': ['II b']}, 'result': ['II b']},
        'm3': {'P1': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
               'A4': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI b']},
        'P4': {'M7': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
              'M2': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
              'm2': {'result': ['II b']},
              'result': ['II', 'II b', 'IV', 'VII dim7']},
        'A4': {'P1': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
               'M2': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
               'm3': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ita']},
        'result': []},
 'M7': {'m6': {'M2': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P4': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'result': ['VII dim7']},
       'M2': {'m6': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'P4': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'P5': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'result': ['V +', 'VII dim']},
       'P4': {'m6': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M2': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'P5': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +7', 'VII dim']},
       'P5': {'M2': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'P4': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +']},
       'result': []},
 'm7': {'M2': {'P4': {'result': ['VII']},
              'P5': {'result': ['V']},
              'result': ['V', 'VII']},
        'm3': {'P5': {'result': ['III']}, 'result': ['III']},
        'P4': {'M2': {'result': ['VII']}, 'result': ['VII']},
        'P5': {'M2': {'result': ['V']},
              'm3': {'result': ['III']},
              'result': ['III', 'V']},
        'result': []},
 'P1': {'M6': {'P4': {'result': ['IV +']}, 'result': ['IV +']},
       'm6': {'M2': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
              'm3': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'P4': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
              'A4': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'result': ['II 7', 'IV', 'VI b']},
       'M2': {'m6': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
             'P4': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'A4': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'result': ['II 7', 'VI Fre']},
       'M3': {'P5': {'result': ['I +']}, 'result': ['I +']},
       'm3': {'m6': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'P5': {'result': ['I']},
              'result': ['I', 'VI b']},
       'P4': {'M6': {'result': ['IV +']},
             'm6': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
             'M2': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'result': ['II 7', 'IV', 'IV +']},
       'A4': {'m6': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'M2': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI Ita']},
       'P5': {'M3': {'result': ['I +']},
             'm3': {'result': ['I']},
             'result': ['I', 'I +']},
       'result': []},
 'M2': {'m6': {'M7': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
              'P4': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
              'A4': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['II', 'VI Fre', 'VII dim7']},
       'M7': {'m6': {'P4': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'P4': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'P5': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'result': ['V +', 'VII dim']},
       'm7': {'P4': {'result': ['VII']},
              'P5': {'result': ['V']},
              'result': ['V', 'VII']},
       'P1': {'m6': {'P4': {'result': ['II 7']},
                    'A4': {'result': ['VI Fre']},
                    'result': ['II 7', 'VI Fre']},
             'P4': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'A4': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
             'result': ['II 7', 'VI Fre']},
       'P4': {'m6': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
             'M7': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'm7': {'result': ['VII']},
             'P1': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'P5': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['II', 'V +7', 'VII', 'VII dim']},
       'A4': {'m6': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P1': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre']},
       'P5': {'M7': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'm7': {'result': ['V']},
             'P4': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V', 'V +']},
       'result': []},
 'm2': {'m6': {'P4': {'result': ['II b']}, 'result': ['II b']},
        'P4': {'m6': {'result': ['II b']}, 'result': ['II b']},
        'result': []},
 'M3': {'P1': {'P5': {'result': ['I +']}, 'result': ['I +']},
       'P5': {'P1': {'result': ['I +']}, 'result': ['I +']},
       'result': []},
 'm3': {'m6': {'P1': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
               'A4': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI b']},
        'm7': {'P5': {'result': ['III']}, 'result': ['III']},
        'P1': {'m6': {'A4': {'result': ['VI Ger']}, 'result': ['VI b']},
              'A4': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'P5': {'result': ['I']},
              'result': ['I', 'VI b']},
        'A4': {'m6': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'P1': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ger']},
        'P5': {'m7': {'result': ['III']},
              'P1': {'result': ['I']},
              'result': ['I', 'III']},
        'result': []},
 'P4': {'M6': {'P1': {'result': ['IV +']}, 'result': ['IV +']},
       'm6': {'M7': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
              'P1': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
              'M2': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
              'm2': {'result': ['II b']},
              'result': ['II', 'II b', 'IV', 'VII dim7']},
       'M7': {'m6': {'M2': {'result': ['VII dim7']}, 'result': ['VII dim7']},
             'M2': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'P5': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +7', 'VII dim']},
       'm7': {'M2': {'result': ['VII']}, 'result': ['VII']},
       'P1': {'M6': {'result': ['IV +']},
             'm6': {'M2': {'result': ['II 7']}, 'result': ['II 7', 'IV']},
             'M2': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'result': ['II 7', 'IV', 'IV +']},
       'M2': {'m6': {'M7': {'result': ['VII dim7']},
                    'P1': {'result': ['II 7']},
                    'result': ['II', 'VII dim7']},
             'M7': {'m6': {'result': ['VII dim7']},
                   'P5': {'result': ['V +7']},
                   'result': ['V +7', 'VII dim']},
             'm7': {'result': ['VII']},
             'P1': {'m6': {'result': ['II 7']}, 'result': ['II 7']},
             'P5': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['II', 'V +7', 'VII', 'VII dim']},
       'm2': {'m6': {'result': ['II b']}, 'result': ['II b']},
       'P5': {'M7': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'M2': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +7']},
       'result': []},
 'A4': {'m6': {'P1': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
               'M2': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
               'm3': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ita']},
        'P1': {'m6': {'M2': {'result': ['VI Fre']},
                     'm3': {'result': ['VI Ger']},
                     'result': ['VI Ita']},
              'M2': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'm3': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
              'result': ['VI Ita']},
        'M2': {'m6': {'P1': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'P1': {'m6': {'result': ['VI Fre']}, 'result': ['VI Fre']},
              'result': ['VI Fre']},
        'm3': {'m6': {'P1': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'P1': {'m6': {'result': ['VI Ger']}, 'result': ['VI Ger']},
               'result': ['VI Ger']},
        'result': []},
 'P5': {'M7': {'M2': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'P4': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +']},
       'm7': {'M2': {'result': ['V']},
              'm3': {'result': ['III']},
              'result': ['III', 'V']},
       'P1': {'M3': {'result': ['I +']},
             'm3': {'result': ['I']},
             'result': ['I', 'I +']},
       'M2': {'M7': {'P4': {'result': ['V +7']}, 'result': ['V +']},
             'm7': {'result': ['V']},
             'P4': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V', 'V +']},
       'M3': {'P1': {'result': ['I +']}, 'result': ['I +']},
       'm3': {'m7': {'result': ['III']},
              'P1': {'result': ['I']},
              'result': ['I', 'III']},
       'P4': {'M7': {'M2': {'result': ['V +7']}, 'result': ['V +7']},
             'M2': {'M7': {'result': ['V +7']}, 'result': ['V +7']},
             'result': ['V +7']},
       'result': []},
 'result': []
}

major_chord = {
  "I": ["P1","M3","P5"],
  "I 7": ["P1","M3","P5","M7"],
  "II b": ["m2","P4","m6"],
  "II": ["M2","P4","M6"],
  "II 7": ["M2","P4","M6","P1"],
  "III": ["M3","P5","M7"],
  "III 7": ["M3","P5","M7","M2"],
  "IV": ["P4","M6","P1"],
  "IV 7": ["P4","M6","P1","M3"],
  "V": ["P5","M7","M2"],
  "V 7": ["P5","M7","M2","P4"],
  "VI b": ["m6","P1","m3"],
  "VI Ger": ["m6","P1","m3","A4"],
  "VI Fre": ["m6","P1","M2","A4"],
  "VI Ita": ["m6","P1","A4"],
  "VI": ["M6","P1","M3"],
  "VI 7": ["M6","P1","M3","P5"],
  "VII": ["M7","M2","P4"],
  "VII 7": ["M7","M2","P4","M6"],
  "VII dim7": ["M7","M2","P4","m6"],
}

minor_chord = {
  "I": ["P1","m3","P5"],
  "I +": ["P1", "M3", "P5"],
  "II b": ["m2","P4","m6"],
  "II": ["M2","P4","m6"],
  "II 7": ["M2","P4","m6","P1"],
  "III": ["m3","P5","m7"],
  "IV": ["P4","m6","P1"],
  "IV +": ["P4","M6","P1"],
  "V": ["P5","m7","M2"],
  "V +": ["P5","M7","M2"],
  "V +7": ["P5","M7","M2","P4"],
  "VI b": ["m6","P1","m3"],
  "VI Ger": ["m6","P1","m3","A4"],
  "VI Fre": ["m6","P1","M2","A4"],
  "VI Ita": ["m6","P1","A4"],
  "VII": ["m7","M2","P4"],
  "VII dim": ["M7","M2","P4"],
  "VII dim7": ["M7","M2","P4","m6"],
}
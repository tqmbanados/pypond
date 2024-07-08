# pypond
Library for creating LilyPond code using Python OOP. Optimized for small code snippets, that can be procedurally created and rendered on the go. Pypond is not 
optimized to create human-readable files, but rather the final result of said file in the preferred format.

Among other things, Pypond is used in the interactive piece ["A Taste of Control"](https://github.com/tqmbanados/aTasteProgram)

### General Functionality

Pypond uses python classes to represent different elements of Lilypond code. Here is an overview of each file:

##### PondFile.py
Contains classes required for finishing, saving and rendering your code. 
1. **PondDoc**: This class manages all the different first level elements of a Lilypond file; such as the header, the paper parameters, custom commands, and the score.
      The method `create_file` returns a string object that can then be saved into a .ly file as Lilypond code. This is best done through the `PondRender` class.
2. **PondRender**: This class stores important variables about the file, the version, the output format and path. Use this class to complete the rendering of 
    your Lilypond files.
    
##### PondCore.py
Contains important classes for managing general aspects of Pypond.

1. **PondObject**: Central object from which most Pypond classes inherit.
2. **CustomFunction**: Pond Object used to create custom commands. These can then be added to the PondDoc object with the method `add_function`.
3. **DurationInterface**: Class Interface that manages certain queries regarding duration; mainly converting between music time (quavers, whole notes, etc) to real time, and obtaining the duration of certain fragments of music. Mostly used internaly by classes, but may provide external use. **Important Note**: The duration interface takes the duration "1" as the duration of the quarter note. This means that the real duration will always depend on the Tempo, which is not taken into acount. 

##### PondMarks.py
Contains Classes with parameters for certain Lilypond keywords and commands. Used to simplify working with python code.

##### PondCommands.py
Contains several of the main commands used in Lilypond. Also contains the class `AbstractCommand` which can be used to personalize own commands. 

##### PondScore.py
Contains classes relating to the `score` lilypond command. 
1. **PondScore**: Contains the music data of the lilypond file. Allows for the creation of multiple staves.
2. **PondTimeSignature**: Class to create Time Signatures and render them in a Lilypond Format.
3. **PondKey**: Class to create Key Signatures and render them in a Lilypond Format.
4. **PondStaff**: Class to create single staves within a score. Each staff can have multiple voices. Time Signature and Key classes must be added to the PondStaff object using the respective methods.

##### PondMusic.py
Central File which contains the classes used to create music data. 

1. **PondMelody**: Central class that represents sections of one voice. This class should be used to contain the totality of the voice in the score, and is optimized for that. The `append_fragment` and `insert_fragment` can be used to add notes and note groups. These methods can take a `PondPitch`, `PondMelody` or `PondNote` class, and renderes them recursively. The `ordered_notes` method returns all the `PondNotes` containted in the `PondMelody`.
2. **PondFragment**: Inherits from **PondMelody**. Optimzed for shorter fragments of the musical voice.
3. **PondPhrase**: Similar to `PondFragment`, but adds a phrase mark (*legato*) between all the notes it contains. Bear in mind this can also be done manually in the `PondNote` class.
4. **PondTuplet**: Also inherits from `PondMelody`. Used to create tuplets. The tuplet type must be entered upon creation. Care must be taken for the `PondTuplet` to be "complete" upon rendering, this can be done with the `DurationInterface`.
5. **PondNote**: Central class for notes in Lilypond. Contains data for the pitch, the duration, articulation, dynamics, expression, trills, and others. Very customizable if required. 
6. **PondChord**: Inherits from `PondNote`. Simlar in everything, but created for chords.
7. **PondNoteGroup**: Deprecated.
8. **PondPitch**: Class that manages pitches in Pypond. Pitches are understood as both two integers (one determines pitch name within the octave, the other which octave) or as an absolute integer that represents both values, 0 being `c` in Lilypond code, 12 being therefore `c'`. Bear in mind Pypond only works with absolute pitch names. 

##### Tree Structure

Pypond code tends to follow a tree like structure, where each fragment of the tree represents different sections of the Lilypond file. 
> PondRender -> PondFile -> PondScore, PondHeader, etc -> PondStaff -> PondMelody -> PondFragment -> PondNote -> PondPitch




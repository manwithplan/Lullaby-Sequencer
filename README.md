# Lullaby Sequencer
 A sample step sequencer built in python, to play through lullabies in an interactive way.
 
 This is the interactive sample step sequencer of a project I worked on.
 The project uses Schenker's theory of musical analysis to generate lullabies, that are played back interactively with real-time sound and motion readings. These readings would have an impact on the tempo and intensity of playback.
 
 The sequencer takes an example lullaby notated in lists. A list is an array that contains shorthands to which notes should be played, and how long the duration of each one is.
 
 As an example : 
 
 > [2,'1b',1,1,'2a',2,4,3,4,3,'3b',2,'2b',1,1,'2a',2,'2b',1,2,1,'1a',2,'99a',3,'3a',4,1,'2a',2,3,3,4,3,2,2,3,'99a',2,0,1,3,2,4,6,99]
 > [2,2,4,2,2,2,2,4,4,4,4,2,2,4,2,2,2,2,4,4,4,4,1,1,1,1,4,2,2,2,2,4,4,4,4,4,1,1,1,1,4,2,2,8,4,4]   
 
 The first line constitutes the melody notes, and the second the duration of each one. numbers 0 to 6 correspond with chord notes over 2 octaves and the appendix 'a' or 'b' mark the note above or below that chord note in the Major Scale. 
 
The samples came from an actual music box sampler and are located in /S/

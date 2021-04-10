The sharpness of a chess position refers to the tactical margin-for-error in a chess position;
while a non-sharp chess position can have many playable moves, a sharp position may have only one or two.
This project aims to evaluate methods for measuring chess sharpness and identifying how sharp a position
is using a computer. While chess engines are good at measuring who is winning a chess position and by how
much, they aren't good at measuring sharpness, as they see a winning variation easily regardless of how
difficult it may be for a human to find those same moves. Here, two methods of evaluation are considered.

Firstly is the number of times an engine fluctuates between recommended moves as depth is increased. This is
analogous to a human chess master changing their considered move as they think for longer. The rationale behind
this measure is that the longer a computer must think before settling on a move, the sharper and more complex
the position is. This method is discussed in this paper: 
https://en.chessbase.com/news/2006/world_champions2006.pdf

Secondly is the mean loss of a chess position - that is the average difference between the computer's evaluation
of the best chess move compared to its average evaluation of the remaining possible moves. For this measure
I used the next 8 best moves to calculate the average, not all possible moves, since the lower moves on those
lists should be obviously bad, even to a weak human player, and thus not qualify for "sharpening" the position.
The mean loss must also be extended to future positions and averaged, otherwise only the sharpness of the
immediate position is considered, while the expected sharpness of future moves stemming from that position
should also be considered. For this I used two methods to generate future moves. The first was a tree of engine
recommended moves for a given depth; while this accurately encompasses all playable (according to the engine
and an arbitrary loss threshold) moves it is extremely computationally expensive and thus can only feasibly be
used for a low depth. The second method was to simulate engine games and find the sharpness of those positions.

These methods of evaluation were considered by an application to a number of chess opening positions with
varying commonly considered degrees of sharpness. The engine fluctuation method was tested using Stockfish 13
and Stockfish 8 to see if using an older engine with a weaker evaluation function could better emulate the
thought process of a chess master. Of these methods the average mean loss method performed well, particularly
for the simulated method, reading comparatively high sharpness for openings thought to be sharp, and low
sharpness for quieter openings.
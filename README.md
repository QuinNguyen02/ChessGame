# Chineese Chess Game

# The story behind this game 📚
This game was developed during the summer of 2022 while I was spending time in Vietnam with my family. Our big family has a tradition of playing chess whenever we gather for dinner on weekends. Typically, the grandchildren take turns playing with each other as well as with the adults. However, I found it inconvenient to carry such a large chessboard around when visiting my uncle's house. Thus, this online version was created. The background music is also my grandfather's favorite song.

# General Implementation 🛠️
1. **One-Player Mode**: The computer opponent is implemented using the minimax algorithm, which enables it to make the best possible moves by considering subsequent results.
2. **Scoring System**: To emphasize the importance of the King, its score is set significantly higher than that of other pieces, penalizing its loss more heavily.

# Room for Improvement 📈
1. **One-Player Mode**:  I could improve the one-player mode by incorporating alpha-beta pruning into the minimax algorithm to eliminate unnecessary expansions in future steps.
2. **Difficulty Level**: Implement three different difficulty levels—Easy, Medium, and Hard—in the one-player mode, possibly by adjusting the depth of the search tree by setting bounds.

# Demo Video 🎥
For one player: https://drive.google.com/file/d/1d7jyFBSz4o8uecEOs1zwd5WYfIck0Bg3/view?usp=sharing
For two player: https://drive.google.com/file/d/1OiaLpuAe-h3G8JPsLQkbwcKo_Qa4dVx_/view?usp=sharing

<div align="center">
    <img src="https://github.com/QuinNguyen02/ChessGame/blob/main/mainPhoto.png" 
    alt="Demo Photo" width="250" height="300" border="10" />
</div>

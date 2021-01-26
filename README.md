# text-chess-piece-moves-v2
Visit [https://varigarble.com/](https://varigarble.com/) to run this project!

Enter a chess piece and coordinate and this will display a chessboard showing the location of the piece and the possible 
squares it can move to. 

This project uses the code from text-chess-piece-moves with a Flask front-end. The empty chessboard is stored as a text 
file and rendered as html in a Flask template so it can be reused without dealing with multiple Flask inheritance 
routings. The output html text is printed to stdout, which is captured and sent to a Flask template. Optional code is 
included to print the output html to, and render from, a text file.

Known issues: Heroku deployment may display previously entered data in jinja templates.

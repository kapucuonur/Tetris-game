# Tetris Game

This project is a web-based version of the classic console-based Tetris game. It has been developed using the Flask framework.

## How It Works

- The application runs as an HTTP server.
- You can view the Tetris board in your web browser.
- Tetrominoes automatically fall and the board updates in real-time.

## Features

- Simple Tetris gameplay with falling tetrominoes.
- Web-based interface for easy access.
- Built using Python and Flask.

## Installation

1. Install Python and pip if you haven't already.
2. Clone or download this repository.
3. Run the following commands in your terminal:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

4. Open your browser and navigate to http://localhost:8000 to play the game.

Deployment
To deploy this application on Render or any other platform:

1. Push the code to a GitHub repository.
2. Connect the repository to Render.
3. Set the following settings:
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
4. Deploy the service, and Render will provide you with a live URL.

Technologies Used

. Python: For backend logic and game mechanics.
. Flask: To serve the game via a web interface.
. HTML: For rendering the game board in the browser.

Contributing

Contributions are welcome! If you have any ideas for improvements or find any bugs, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

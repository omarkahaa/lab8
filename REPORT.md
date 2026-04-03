# REPORT

## Project
lab8-pygame

## Objective
The goal of this lab was to create a simple pygame application with moving squares, then extend it by improving the movement and structure of the program.

## What I implemented
I created a pygame application that opens a window and displays 100 squares moving on the screen.

Each square has:
- a random size
- a random position
- a random color
- a movement direction based on horizontal and vertical speed values

I added global constants for:
- window size
- number of squares
- minimum square size
- maximum square size
- global maximum speed
- angle jitter
- FPS

I also implemented a max speed rule for each square based on its size, so that larger squares move more slowly than smaller ones. This follows the lab extension and makes the animation more varied.

Another feature I added was direction jitter. Each square changes direction slightly over time, which makes the movement less rigid and more natural than only moving in straight lines.

The squares bounce when they hit the borders of the window, and I also added an FPS counter displayed on the screen.

## Program structure
The project is organized around a `Square` class.

The class handles:
- square creation
- movement
- random direction jitter
- speed limiting
- drawing

The rest of the program is handled in the `main()` function, which:
- initializes pygame
- creates the window
- creates all squares
- runs the main loop
- updates movement
- draws the objects
- updates the display
- controls frame rate
- quits pygame when the program is closed

## Main choices
I chose to use a class because it made the code easier to read and easier to extend. It also helped keep the square behavior grouped in one place.

I used `dx` and `dy` values to represent movement, because this made it easier to add jitter and speed control.

I kept global constants at the top of the file so the project could be adjusted more easily without changing the logic everywhere.

## Difficulties
The main difficulty was making the movement look random without making it look chaotic. Another difficulty was keeping the squares inside the screen while still allowing them to move smoothly.

I also had to be careful that the jitter changed direction without breaking the speed limit rule.

## What I learned
This project helped me better understand:
- the pygame application loop
- frame-by-frame updates
- basic animation logic
- border collision handling
- organizing code with a class
- how small movement changes affect the final behavior on screen

I also learned that even a small graphical project becomes easier to manage when the logic is split into clear methods.

## Conclusion
The final version is a working pygame project that goes beyond the basic moving squares version. It includes 100 animated squares, speed depending on size, direction jitter, border bouncing, and FPS display.

The project also helped me practice using Copilot in a more controlled way, by working feature by feature instead of trying to generate everything at once.
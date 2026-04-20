# REPORT

## Project
lab8

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
- flee distance
- flee force
- minimum and maximum life span

I also implemented a max speed rule for each square based on its size, so that larger squares move more slowly than smaller ones. This follows the lab extension and makes the animation more varied.

Another feature I added was direction jitter. Each square changes direction slightly over time, which makes the movement less rigid and more natural than only moving in straight lines.

I also added a flee behavior. Smaller squares check nearby bigger squares and move away from them when they are close enough. I implemented this using the movement vectors already used in the project (`dx` and `dy`). This keeps the behavior simple and consistent with the rest of the code. The movement still stays partly random because the jitter is still applied at each update.

The squares bounce when they hit the borders of the window, and I also added an FPS counter displayed on the screen.

I added a life span and rebirth feature. Each square is given a random life span between 30 and 180 seconds. The square tracks its age using a timer that increments with `dt` each frame. When its age exceeds its life span, it is replaced by a new square with fresh random values.

I also added time-based movement. Instead of moving by a fixed amount per frame, each square now moves based on the elapsed time (`dt`), which makes the movement more consistent across different frame rates.

I added type hints to all methods and functions.

## Program structure
The project is organized around a `Square` class.

The class handles:
- square creation
- movement
- random direction jitter
- flee behavior
- speed limiting
- drawing

The class also stores the life span and age of each square.

The rest of the program is handled in the `main()` function, which:
- initializes pygame
- creates the window
- creates all squares
- runs the main loop
- updates each square's age
- replaces dead squares with new ones
- updates movement
- draws the objects
- updates the display
- controls frame rate
- quits pygame when the program is closed

## Main choices
I chose to use a class because it made the code easier to read and easier to extend. It also helped keep the square behavior grouped in one place.

I used `dx` and `dy` values to represent movement, because this made it easier to add jitter, speed control, and the flee behavior.

I kept global constants at the top of the file so the project could be adjusted more easily without changing the logic everywhere.

For the flee behavior, I chose to use vectors instead of angles. Since the program already uses horizontal and vertical speed values, it was simpler to compute the direction away from a bigger square and add a small force directly to `dx` and `dy`.

For the life span feature, I used an `age` float that increments by `dt` each frame and compared it against a random `life_span` value. I used `range(len(squares))` in the main loop instead of a regular for loop so I could replace dead squares by index.

For time-based movement, I multiplied `dx` and `dy` by `dt * FPS` so the speed stays more consistent across different frame rates.

## Difficulties
The main difficulty was making the movement look random without making it look chaotic. Another difficulty was keeping the squares inside the screen while still allowing them to move smoothly.

I also had to be careful that the jitter changed direction without breaking the speed limit rule.

For the flee behavior, the difficulty was keeping it simple enough to explain while still making the smaller squares react visibly to bigger ones.

## What I learned
This project helped me better understand:
- the pygame application loop
- frame-by-frame updates
- basic animation logic
- border collision handling
- organizing code with a class
- how small movement changes affect the final behavior on screen
- how to use delta time for more frame-rate independent movement
- how to manage object lifetimes in an animation loop
- how type hints improve code readability

I also learned that even a small graphical project becomes easier to manage when the logic is split into clear methods.

The flee feature also helped me practice using distances and vectors in a simple animation.

## Conclusion
The final version includes 100 animated squares, speed depending on size, direction jitter, border bouncing, FPS display, flee behavior, time-based movement, type hints, and a life span and rebirth system where each square dies and is replaced after a random amount of time.

## Chasing behavior idea

For the chasing feature, I wanted to do something simple and close to the flee feature I already had.

My idea was that I did not need to create a completely new system because the code already had the loop on the squares, the size comparison, and the movement with `dx` and `dy`.

So I used the same logic as before, but this time for bigger squares going toward smaller ones.

I check the other squares, and if one is smaller and close enough, I compare its position with the current square.
If it is on the right, I increase `dx`.
If it is on the left, I decrease `dx`.
I do the same for `dy` depending on whether it is above or below.

I kept it simple on purpose because it was enough for the behavior I wanted and it matches the style of the rest of my code.

I also kept the jitter, so even when a square is chasing another one, the movement still looks a bit natural and not too exact.
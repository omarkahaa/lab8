# REPORT

## Project
lab8-pygame

## Objective
The goal of this project was to create a pygame animation with moving squares and improve it by adding more behaviors and interactions between them.

## What I implemented
I created a pygame program that opens a window and displays 100 squares moving on the screen.

Each square has:
- a random size
- a random position
- a random color
- a movement direction using `dx` and `dy`

I used constants for the window size, number of squares, square sizes, speed, jitter, fleeing, chasing, life span, and FPS.

I also made bigger squares slower than smaller ones by giving each square a maximum speed based on its size.

## Chasing behavior
One of the new features I added is chasing.

The idea is simple:
- if a square is bigger than another square
- and the smaller square is close enough
- then the bigger square moves toward it

To do this, I compare the positions of the two squares.
If the smaller square is more to the right, I increase `dx`.
If it is more to the left, I decrease `dx`.
I do the same with `dy` for up and down.

I kept this implementation simple on purpose so it matches the rest of my code and stays easy to understand.

## Fleeing behavior
I also kept the fleeing behavior.

If a square is smaller than another nearby square, it moves away from it.

So now the behavior is:
- small squares flee
- big squares chase

This makes the animation more interesting because the squares react differently depending on their size.

## Random movement
I kept the jitter in the program so the squares do not move in perfectly straight lines.

At each frame, their angle changes a little randomly.
This makes the movement look more natural.

## Life span and rebirth
Each square has a random life span between 3 and 9 seconds.

Its age increases during the game loop.
When it reaches the end of its life span, it is replaced by a new square with new random values.

This keeps the animation changing over time.

## FPS display
I display the FPS in the top-left corner of the screen.

This helped me test the program and see if it was running correctly.

## How I approached it
I tried to keep the code simple and reuse what I already had.

For the chasing feature, I used the same general structure as the fleeing feature:
- loop through the squares
- compare sizes
- check the distance
- update movement

Instead of building a completely new system, I added the new behavior on top of the existing movement.

## Result
The final animation has several behaviors working together:
- random movement
- border bounce
- fleeing
- chasing
- rebirth after life span

Because of this, the squares do not all move the same way and the animation feels more alive.

## What I learned
With this project, I practiced:
- using classes in Python
- working with pygame
- updating many objects in a loop
- controlling movement with `dx` and `dy`
- adding behaviors step by step

## Conclusion
This version of the project is more dynamic than the first one.

Adding chasing made the squares interact more with each other, while still keeping the code simple and readable.
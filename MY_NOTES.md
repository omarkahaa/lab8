# MY_NOTES

## Idea
I added a flee behavior to the squares.

## Strategy
The main movement of the squares was already random with jitter.

Then I added one simple rule:
- if a square sees a bigger square near it,
- it moves a little away from it

## How it works
For each square, I check the other squares on the screen.

If the other square is bigger:
- I calculate the horizontal and vertical difference
- I calculate the distance
- if the distance is small enough, I add a small movement away from the bigger square

I used `dx` and `dy` because the program already uses them for movement.

## Edge cases
- the square must not compare with itself
- only bigger squares should affect smaller ones
- only nearby squares should trigger the flee behavior
- speed must still stay limited

## Result
The movement stays random, but smaller squares now react to bigger nearby squares by escaping from them.
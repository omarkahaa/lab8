# Architecture Documentation

## Project Overview

`lab8` is a simple `pygame` simulation where 100 colored squares move around a window and interact through local steering rules. The project is implemented in a single Python module (`main.py`) and follows a classic game loop architecture.

## Key Components

### `main.py`
- Initializes `pygame` and the display window.
- Defines global constants for window size, square count, motion parameters, and behavior thresholds.
- Contains the `Square` class and the `main()` game loop.

### `Square` class
- Encapsulates one square's state and behavior.
- Attributes include position (`x`, `y`), velocity (`dx`, `dy`), size, color, lifespan, and age.
- Responsible for one-frame behavior: jitter, fleeing, chasing, velocity limiting, boundary bouncing, movement, and rendering.

### Global constants
- `WIDTH`, `HEIGHT`: screen dimensions.
- `NUM_SQUARES`: number of square objects.
- `MIN_SIZE`, `MAX_SIZE`: randomized square size range.
- `GLOBAL_MAX_SPEED`: base speed factor.
- `ANGLE_JITTER`: directional noise applied every frame.
- `FLEE_DISTANCE`, `FLEE_FORCE`: parameters for avoidance behavior.
- `CHASE_DISTANCE`, `CHASE_FORCE`: parameters for pursuit behavior.
- `MIN_LIFE`, `MAX_LIFE`: randomized lifetime range for each square.
- `FPS`: target frame rate.

## Runtime Flow

### Initialization
1. `pygame.init()`
2. Create window surface with `pygame.display.set_mode((WIDTH, HEIGHT))`
3. Create font for FPS rendering.
4. Build `squares: list[Square]` with `NUM_SQUARES` instances.
5. Enter the main loop.

### Main loop
Each frame performs:
- Event handling (`pygame.event.get()`), including quit detection.
- Clear screen with background color.
- Update each square:
  - Increment `age` by elapsed time.
  - Replace the square if its `life_span` is exceeded.
  - Execute `move(squares, dt)` and `draw(screen)`.
- Render the FPS counter.
- Flip the display with `pygame.display.flip()`.

### Square update and rendering
`Square.move(squares, dt)` executes the following pipeline:
1. `apply_jitter()` adds small angular noise to velocity.
2. `flee(squares)` pushes smaller squares away from larger neighbors within `FLEE_DISTANCE`.
3. `chase(squares)` pulls larger squares toward smaller neighbors within `CHASE_DISTANCE`.
4. `limit_speed()` clamps velocity so it does not exceed `max_speed`.
5. Update position using `dx`, `dy`, `dt`, and `FPS`.
6. Bounce from window borders by reversing velocity when hitting an edge.

`Square.draw(screen)` renders the square as a filled rectangle on the screen surface.

## Behavioral Rules

- Squares are initialized with a random speed and direction.
- Larger squares move more slowly because `max_speed` is scaled inversely with size.
- Smaller squares flee from larger squares within `FLEE_DISTANCE`.
- Larger squares chase smaller squares within `CHASE_DISTANCE`.
- Each square has a finite lifetime and is replaced when it expires, creating continuous turnover.

## Architecture Diagrams

### Component Diagram

```mermaid
graph LR
    A[main()] --> B[pygame subsystem]
    A --> C[Square objects]
    B --> D[Window Surface]
    A --> E[Event handling]
    A --> F[Render loop]
    C --> G[Movement logic]
    C --> H[Rendering logic]
    G --> I[apply_jitter()]
    G --> J[flee()]
    G --> K[chase()]
    G --> L[limit_speed()]
    G --> M[boundary bounce]
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant main
    participant Square
    participant pygame

    User->>main: launch program
    main->>pygame: init(), set_mode(), SysFont()
    main->>Square: create list of squares
    loop every frame
    main->>pygame: poll events
    main->>Square: update age, respawn if expired
    main->>Square: move(squares, dt)
    Square->>Square: apply_jitter(), flee(), chase(), limit_speed(), boundary bounce
    main->>Square: draw(screen)
    main->>pygame: blit FPS text
    main->>pygame: display.flip()
```

## Design Notes

- This project is organized as a single-module prototype, which is appropriate for a small lab assignment.
- The program separates update logic (`move`) from render logic (`draw`) within `Square`.
- The system uses simple pairwise interactions among squares, making the behavior emergent and visually interesting.
- Additional architecture improvements could include splitting classes into separate modules, adding a `Game` controller class, and isolating physics from rendering.

## Running the project

Use:

```bash
python main.py
```

Make sure `pygame` is installed from `requirements.txt`.

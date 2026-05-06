# JavaScript Port Strategy: Moving Squares Simulation

## Project Overview
**Original**: Pygame-based physics simulation with dynamic squares that move, interact, collide, and age.
**Target**: HTML5 Canvas with requestAnimationFrame loop, preserving all logic and class structure.

---

## 1. Class-by-Class Mapping

### Square Class (Python → JavaScript)

#### Constructor
```
Python:
  def __init__(self, size: float) -> None:
    - self.size = size
    - self.x, self.y = random positions
    - self.max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / self.size)
    - self.dx, self.dy = velocity from random angle and speed
    - self.color = (r, g, b) tuple
    - self.life_span = random lifespan
    - self.age = 0.0

JavaScript:
  constructor(size) {
    - this.size = size
    - this.x = Math.random() * (WIDTH - this.size)
    - this.y = Math.random() * (HEIGHT - this.size)
    - this.max_speed = GLOBAL_MAX_SPEED * (MIN_SIZE / this.size)
    - angle = random angle, speed = random speed
    - this.dx = Math.cos(angle) * speed
    - this.dy = Math.sin(angle) * speed
    - this.color = {r, g, b}
    - this.life_span = random in [MIN_LIFE, MAX_LIFE]
    - this.age = 0.0
  }
```

#### Instance Methods

| Python Method | JavaScript Method | Mapping Notes |
|---|---|---|
| `center_x()` | `centerX()` | Returns x + size/2 |
| `center_y()` | `centerY()` | Returns y + size/2 |
| `check_collision(other)` | `checkCollision(other)` | AABB collision: compare rectangles |
| `eat(squares)` | `eat(squares)` | Iterate array, grow on collision, respawn eaten |
| `apply_jitter()` | `applyJitter()` | Random angle perturbation |
| `limit_speed()` | `limitSpeed()` | Cap velocity magnitude |
| `flee(squares)` | `flee(squares)` | Repulsion from larger squares |
| `chase(squares)` | `chase(squares)` | Attraction to smaller squares |
| `move(squares, dt)` | `move(squares, dt)` | Physics update: apply behaviors, move, handle boundaries |
| `draw(screen)` | `draw(ctx)` | Render to Canvas context (brightness-adjusted color) |

---

## 2. Function/Method Equivalents with Parameter Translations

### Coordinate System
```
Python:        pygame.Rect(x, y, width, height)
JavaScript:    canvas.fillRect(x, y, width, height)
```
**Translation**: All x, y coordinates remain the same. Canvas API uses same convention.

### Random Number Generation
```
Python:        random.uniform(a, b)      → JavaScript:  Math.random() * (b - a) + a
Python:        random.randint(a, b)      → JavaScript:  Math.floor(Math.random() * (b - a + 1)) + a
```

### Velocity Vector Math
```
Python:        angle = math.atan2(dy, dx)
JavaScript:    angle = Math.atan2(dy, dx)

Python:        distance = math.hypot(dx, dy)
JavaScript:    distance = Math.hypot(dx, dy)  [ES2015+]
                or: distance = Math.sqrt(dx*dx + dy*dy)
```

### Collision Detection
```
Python:
  my_rect = pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))
  other_rect = pygame.Rect(...)
  return my_rect.colliderect(other_rect)

JavaScript:
  // AABB (Axis-Aligned Bounding Box) collision
  return !(this.x + this.size <= other.x || 
           other.x + other.size <= this.x ||
           this.y + this.size <= other.y ||
           other.y + other.size <= this.y)
```

### Drawing & Rendering
```
Python:
  pygame.draw.rect(screen, (r, g, b), (x, y, size, size))

JavaScript:
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`
  ctx.fillRect(x, y, size, size)
```

### Text Rendering (FPS Display)
```
Python:
  font = pygame.font.SysFont(None, 30)
  fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
  screen.blit(fps_text, (10, 10))

JavaScript:
  ctx.font = "30px Arial"
  ctx.fillStyle = "rgb(0, 0, 0)"
  ctx.fillText(`FPS: ${Math.round(currentFps)}`, 10, 10)
```

---

## 3. Event/Input Strategy

### Pygame Event Loop
```python
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
```

### JavaScript Equivalent (requestAnimationFrame Pattern)
```javascript
let animationId = null;

function animate() {
  // Main game loop body (draw, update, etc.)
  
  // Continue looping
  animationId = requestAnimationFrame(animate);
}

// Graceful exit (optional button or window close)
window.addEventListener('beforeunload', () => {
  if (animationId) cancelAnimationFrame(animationId);
});

animate(); // Start the loop
```

**No explicit event handling needed for quit** — page unload/reload handles cleanup automatically.

---

## 4. Graphics/Canvas Equivalents

### Pygame → Canvas Context (ctx)

| Pygame Operation | Canvas Equivalent | Notes |
|---|---|---|
| `screen.fill(color)` | `ctx.fillStyle = "rgb(r,g,b)"; ctx.fillRect(0, 0, WIDTH, HEIGHT)` | Clear canvas to background color |
| `pygame.draw.rect(screen, color, (x, y, w, h))` | `ctx.fillStyle = "rgb(...)"; ctx.fillRect(x, y, w, h)` | Fill rectangle |
| `screen.blit(text_surface, (x, y))` | `ctx.fillText(text, x, y)` | Render text at position |
| `pygame.display.flip()` | (automatic with Canvas) | Canvas updates immediately; no explicit flip needed |

### Color Representation
```python
color = (red, green, blue)           # Python tuple
```
```javascript
color = {r: red, g: green, b: blue}  // JavaScript object
```

### Display Setup
```python
pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")
```

```javascript
const canvas = document.getElementById('gameCanvas');
canvas.width = WIDTH;
canvas.height = HEIGHT;
document.title = "Moving Squares"; // or update document.querySelector('title')
```

---

## 5. Simulation Loop Approach

### Pygame: Clock-Based FPS
```python
clock = pygame.time.Clock()
FPS = 60

while running:
    dt = clock.tick(FPS) / 1000.0  # Returns milliseconds, convert to seconds
    # ... update game state with dt
```

**Behavior**: `clock.tick(FPS)` blocks execution until sufficient time has passed, ensuring consistent FPS.

### JavaScript: requestAnimationFrame + Delta Time

```javascript
const FPS = 60;
const FRAME_TIME = 1000 / FPS;  // milliseconds per frame

let lastTime = Date.now();
let lag = 0.0;

function animate() {
  const now = Date.now();
  const delta = now - lastTime;
  lastTime = now;
  lag += delta;

  // Fixed timestep updates (optional but recommended for physics stability)
  while (lag >= FRAME_TIME) {
    update(FRAME_TIME / 1000.0);  // Convert to seconds
    lag -= FRAME_TIME;
  }

  draw();
  requestAnimationFrame(animate);
}
```

**Equivalent Behavior**:
- `dt` in Python = time since last frame (seconds) = `delta / 1000.0` in JavaScript
- Both approaches accumulate time and advance game state
- **Key difference**: Python blocks; JavaScript loops are non-blocking
- **Porting strategy**: Use `delta / 1000.0` as dt parameter, or implement fixed timestep with lag accumulation

---

## 6. Module & Global Constants

### Constants Translation
```python
WIDTH = 800
HEIGHT = 600
BIG_SQUARES = 5
MEDIUM_SQUARES = 10
SMALL_SQUARES = 30
GROWTH_RATE = 0.5
MAX_SIZE = 70
BIG_SIZE = 25
MEDIUM_SIZE = 10
SMALL_SIZE = 4
MIN_SIZE = SMALL_SIZE
GLOBAL_MAX_SPEED = 6
ANGLE_JITTER = 0.15
BACKGROUND_COLOR = (255, 255, 255)
FPS = 60
FLEE_DISTANCE = 100
FLEE_FORCE = 0.2
CHASE_DISTANCE = 100
CHASE_FORCE = 0.08
MIN_LIFE = 3
MAX_LIFE = 9
MIN_BRIGHTNESS = 0.25
```

**JavaScript equivalent:**
```javascript
const WIDTH = 800;
const HEIGHT = 600;
const BIG_SQUARES = 5;
// ... etc (exact same values)
const BACKGROUND_COLOR = {r: 255, g: 255, b: 255};
```

---

## 7. Data Structure Transformations

### Squares List
```python
squares: list[Square] = []
for _ in range(BIG_SQUARES):
    squares.append(Square(BIG_SIZE))
```

**JavaScript:**
```javascript
let squares = [];
for (let i = 0; i < BIG_SQUARES; i++) {
    squares.push(new Square(BIG_SIZE));
}
```

### Random Color Tuple
```python
self.color = (
    random.randint(50, 255),
    random.randint(50, 255),
    random.randint(50, 255),
)
```

**JavaScript:**
```javascript
this.color = {
    r: Math.floor(Math.random() * 206) + 50,
    g: Math.floor(Math.random() * 206) + 50,
    b: Math.floor(Math.random() * 206) + 50
};
```

---

## 8. Main Function & Application Structure

### Pygame Main Entry
```python
def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    squares = []  # Initialize
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        # ... event handling, update, draw
    pygame.quit()

if __name__ == "__main__":
    main()
```

### JavaScript Equivalent
```javascript
// Initialize globals and DOM
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = WIDTH;
canvas.height = HEIGHT;

let squares = [];
let animationId = null;
let lastTime = Date.now();

function initializeGame() {
    for (let i = 0; i < BIG_SQUARES; i++) squares.push(new Square(BIG_SIZE));
    for (let i = 0; i < MEDIUM_SQUARES; i++) squares.push(new Square(MEDIUM_SIZE));
    for (let i = 0; i < SMALL_SQUARES; i++) squares.push(new Square(SMALL_SIZE));
}

function animate() {
    const now = Date.now();
    const dt = (now - lastTime) / 1000.0;
    lastTime = now;

    update(dt);
    draw();

    animationId = requestAnimationFrame(animate);
}

// Start on page load
window.addEventListener('DOMContentLoaded', () => {
    initializeGame();
    animate();
});
```

---

## 9. Port Validation Checklist

✓ **Class Structure** — `Square` class exists with all methods
✓ **Constructor Logic** — Position, velocity, color, life_span initialization matches
✓ **Physics** — Movement, jitter, fleeing, chasing, eating all preserved
✓ **Rendering** — Canvas drawing with brightness interpolation
✓ **Game Loop** — requestAnimationFrame with dt-based timing
✓ **Collision** — AABB detection using rectangle overlap
✓ **Boundary Wrapping** — Squares bounce off edges, position clamped

---

## 10. Porting Order (Recommended)

1. **HTML & Canvas Setup** — Create `index.html` with canvas element
2. **Constants & Color Utility** — Define all global constants and color conversion helper
3. **Square Class** — Implement constructor, utility methods (centerX, centerY, etc.)
4. **Physics Methods** — applyJitter, limitSpeed, flee, chase, move
5. **Collision & Interaction** — checkCollision, eat
6. **Rendering** — draw method with brightness calculation
7. **Game Loop** — animate, initialize, FPS display
8. **HTML Template** — Create minimal index.html linking to JS
9. **Testing** — Verify all squares move, collide, age, and regenerate correctly

---

## 11. Notes & Edge Cases

- **Type Conversions**: Python `int()` conversions for pixel coordinates should be preserved in JavaScript (use `Math.floor()` or `Math.round()`)
- **Floating-Point Arithmetic**: Python and JavaScript handle floats similarly; no special concern
- **Array Mutation**: Python's `squares[i] = Square(...)` replaces array element; JavaScript's `squares[i] = new Square(...)` does the same
- **Random Seeding**: No seeding in original; if needed, use a library like `seedrandom` for reproducibility
- **Performance**: Canvas rendering is typically fast enough for 45 squares; consider optimization only if FPS drops below 30


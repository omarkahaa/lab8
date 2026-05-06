# JavaScript Port Validation: Moving Squares Simulation

## 1. Side-by-Side Method Mapping Table

| Python Method | JavaScript Method | Signature | Equivalent Behavior | Status |
|---|---|---|---|---|
| `Square.__init__(size)` | `constructor(size)` | `new Square(size)` | Initialize square with random position, velocity, color, lifespan | ✓ Map |
| `center_x()` | `centerX()` | `→ number` | Return center X coordinate (x + size/2) | ✓ Map |
| `center_y()` | `centerY()` | `→ number` | Return center Y coordinate (y + size/2) | ✓ Map |
| `check_collision(other)` | `checkCollision(other)` | `→ boolean` | AABB collision test (rectangle overlap) | ✓ Map |
| `eat(squares)` | `eat(squares)` | `(array) → void` | Consume smaller colliding squares, grow, respawn eaten | ✓ Map |
| `apply_jitter()` | `applyJitter()` | `() → void` | Apply random angle perturbation to velocity | ✓ Map |
| `limit_speed()` | `limitSpeed()` | `() → void` | Cap velocity magnitude to max_speed | ✓ Map |
| `flee(squares)` | `flee(squares)` | `(array) → void` | Move away from larger squares within FLEE_DISTANCE | ✓ Map |
| `chase(squares)` | `chase(squares)` | `(array) → void` | Move toward smaller squares within CHASE_DISTANCE | ✓ Map |
| `move(squares, dt)` | `move(squares, dt)` | `(array, number) → void` | Apply behaviors, update position, handle boundaries | ✓ Map |
| `draw(screen)` | `draw(ctx)` | `(CanvasRenderingContext2D) → void` | Render square with brightness-adjusted color | ✓ Map |
| `main()` | (Game loop) | (requestAnimationFrame) | Initialize, loop, update, draw, cleanup | ✓ Map |

---

## 2. Data Structure Transformations

### Squares Array

| Python | JavaScript | Transformation |
|---|---|---|
| `squares: list[Square]` | `let squares = []` | Mutable array holding Square instances |
| `squares.append(Square(...))` | `squares.push(new Square(...))` | Add new square to array |
| `squares[i] = Square(...)` | `squares[i] = new Square(...)` | Replace square at index i |
| `for i in range(len(squares)):` | `for (let i = 0; i < squares.length; i++)` | Iterate by index |

### Color Representation

| Python | JavaScript | Context | Transformation |
|---|---|---|---|
| `self.color = (r, g, b)` | `this.color = {r, g, b}` | Storage | Tuple → Object |
| `(red, green, blue)` | `` `rgb(${red}, ${green}, ${blue})` `` | Canvas fillStyle | Tuple → CSS string |
| `color[0], color[1], color[2]` | `color.r, color.g, color.b` | Access | Indexing → Property access |

### Position & Velocity

| Python | JavaScript | Transformation |
|---|---|---|
| `self.x, self.y` | `this.x, this.y` | Position (float) |
| `self.dx, self.dy` | `this.dx, this.dy` | Velocity (float) |
| `self.size` | `this.size` | Width/height of square (float) |
| `self.max_speed` | `this.maxSpeed` | Speed cap (float) |

### Lifecycle Attributes

| Python | JavaScript | Transformation |
|---|---|---|
| `self.age` | `this.age` | Time since creation (seconds, float) |
| `self.life_span` | `this.lifeSpan` | Time until regeneration (seconds, float) |

---

## 3. Behavioral Equivalence Checklist

### Input Handling
- **Python**: `pygame.event.get()` checks for QUIT event
- **JavaScript**: No explicit event handling needed; page unload/reload handles cleanup
- **Equivalence**: ✓ Behavior equivalent (loop terminates on page close)

### Movement & Physics
- **Python**: `move(squares, dt)` applies jitter, flee, chase, limits speed, updates position with dt scaling
- **JavaScript**: `move(squares, dt)` performs identical operations
- **Equivalence**: ✓ Position updates use same formula: `x += dx * dt * FPS`
- **Critical Parameter**: `dt` must be in seconds; ensure conversion: `ms / 1000.0`

### Collision Detection
- **Python**: `pygame.Rect.colliderect()` performs AABB test
- **JavaScript**: Manual AABB formula (no rect object)
- **Equivalence**: ✓ Mathematically equivalent
  ```
  Rects overlap iff NOT (a_right <= b_left OR a_left >= b_right OR a_bottom <= b_top OR a_top >= b_bottom)
  ```

### Eating Behavior
- **Python**: `eat(squares)` iterates all squares, grows if collision with smaller, respawns eaten square
- **JavaScript**: Identical logic
- **Equivalence**: ✓ Array mutation preserved (replace eaten square with new Square at same size)
- **Position Centering**: Both preserve center position during growth; clamping to bounds is identical

### Aging & Regeneration
- **Python**: `age += dt` each frame; if `age >= life_span`, create new square
- **JavaScript**: Identical logic
- **Equivalence**: ✓ Timing preserved via dt parameter

### Rendering & Display
- **Python**: `draw(screen)` renders filled rect with brightness-adjusted color to pygame surface
- **JavaScript**: `draw(ctx)` renders filled rect to canvas context
- **Equivalence**: ✓ Brightness calculation identical
  ```
  brightness = 1 - (age / life_span)
  if brightness < MIN_BRIGHTNESS: brightness = MIN_BRIGHTNESS
  color_component = int(original_component * brightness)
  ```

### FPS Display
- **Python**: Render text using `pygame.font` and `screen.blit()`
- **JavaScript**: Render text using `ctx.fillText()`
- **Equivalence**: ✓ Displays FPS counter at position (10, 10)
- **FPS Calculation**: Varies by implementation; both can estimate from frame timing

---

## 4. Constants & Configuration

| Constant | Python Value | JavaScript Equivalent | Purpose |
|---|---|---|---|
| `WIDTH` | 800 | 800 | Canvas width |
| `HEIGHT` | 600 | 600 | Canvas height |
| `BIG_SQUARES` | 5 | 5 | Initial count of large squares |
| `MEDIUM_SQUARES` | 10 | 10 | Initial count of medium squares |
| `SMALL_SQUARES` | 30 | 30 | Initial count of small squares |
| `GROWTH_RATE` | 0.5 | 0.5 | Size increase when eating (fraction of eaten size) |
| `MAX_SIZE` | 70 | 70 | Maximum square size |
| `BIG_SIZE` | 25 | 25 | Initial size of big squares |
| `MEDIUM_SIZE` | 10 | 10 | Initial size of medium squares |
| `SMALL_SIZE` | 4 | 4 | Initial size of small squares |
| `MIN_SIZE` | 4 (from SMALL_SIZE) | 4 | Minimum size (used in max_speed calc) |
| `GLOBAL_MAX_SPEED` | 6 | 6 | Base speed cap |
| `ANGLE_JITTER` | 0.15 | 0.15 | Max angle deviation (radians) |
| `BACKGROUND_COLOR` | (255, 255, 255) | {r: 255, g: 255, b: 255} | White background |
| `FPS` | 60 | 60 | Target frames per second |
| `FLEE_DISTANCE` | 100 | 100 | Max distance to trigger flee behavior |
| `FLEE_FORCE` | 0.2 | 0.2 | Repulsion acceleration magnitude |
| `CHASE_DISTANCE` | 100 | 100 | Max distance to trigger chase behavior |
| `CHASE_FORCE` | 0.08 | 0.08 | Attraction acceleration magnitude |
| `MIN_LIFE` | 3 | 3 | Minimum lifespan (seconds) |
| `MAX_LIFE` | 9 | 9 | Maximum lifespan (seconds) |
| `MIN_BRIGHTNESS` | 0.25 | 0.25 | Minimum color brightness (aging floor) |

---

## 5. Math Function Equivalents

| Concept | Python | JavaScript | Notes |
|---|---|---|---|
| Random float in [a, b) | `random.uniform(a, b)` | `Math.random() * (b - a) + a` | Inclusive of a, exclusive of b |
| Random int in [a, b] | `random.randint(a, b)` | `Math.floor(Math.random() * (b - a + 1)) + a` | Inclusive both ends |
| Distance | `math.hypot(dx, dy)` | `Math.hypot(dx, dy)` or `Math.sqrt(dx*dx + dy*dy)` | Euclidean distance |
| Angle from velocity | `math.atan2(dy, dx)` | `Math.atan2(dy, dx)` | Returns radians in [-π, π] |
| Cosine, Sine | `math.cos(angle)`, `math.sin(angle)` | `Math.cos(angle)`, `Math.sin(angle)` | Standard trig |
| Absolute value | `abs(x)` | `Math.abs(x)` | Sign removal |
| Min, Max | `min(a, b)`, `max(a, b)` | `Math.min(a, b)`, `Math.max(a, b)` | Constrain value |

---

## 6. Loop Structure Equivalence

### Pygame Loop
```python
while running:
    dt = clock.tick(FPS) / 1000.0  # Blocks until frame time elapsed
    # Poll events
    # Update game state
    # Render
    pygame.display.flip()           # Update display
pygame.quit()                        # Cleanup
```

### JavaScript Loop
```javascript
let lastTime = Date.now();

function animate() {
    const now = Date.now();
    const dt = (now - lastTime) / 1000.0;  // Non-blocking
    lastTime = now;
    
    // Update game state
    // Render
    // (Canvas updates immediately, no explicit flip)
    
    animationId = requestAnimationFrame(animate);  // Schedule next frame
}

animate();  // Start loop

// Cleanup happens automatically on page unload
```

**Key Differences**:
1. Pygame blocks until frame time; JavaScript schedules asynchronously
2. Both achieve similar FPS via timing control
3. Canvas updates happen immediately (no flip needed)
4. Cleanup is implicit in JavaScript (GC on unload)

---

## 7. Port Testing Checklist

### Functional Tests
- [ ] **Square spawns** at random position within bounds
- [ ] **Color is random** RGB tuple (50-255 per channel)
- [ ] **Velocity is random** with angle from 0-2π and speed from 1 to max_speed
- [ ] **Life span is random** between MIN_LIFE and MAX_LIFE seconds
- [ ] **Square moves** in direction of velocity, scaled by dt and FPS
- [ ] **Boundary wrapping** reverses velocity when hitting edge, clamps position
- [ ] **Jitter applies** random angle perturbation each frame
- [ ] **Speed is limited** to max_speed (which decreases as size increases)
- [ ] **Fleeing behavior** repels from larger squares within FLEE_DISTANCE
- [ ] **Chasing behavior** attracts to smaller squares within CHASE_DISTANCE
- [ ] **Collision detection** correctly identifies overlapping rectangles
- [ ] **Eating mechanic** grows larger square, respawns eaten square at new size
- [ ] **Center preservation** maintains square center during growth
- [ ] **Aging advances** by dt each frame
- [ ] **Regeneration** creates new square when age >= life_span
- [ ] **Brightness decays** from 1.0 to MIN_BRIGHTNESS over lifespan
- [ ] **FPS counter displays** and updates each frame

### Equivalence Tests
- [ ] **All 5 big, 10 medium, 30 small** squares initialize
- [ ] **Physics math identical** (position updates match Python)
- [ ] **Collision list preserved** (no missing squares)
- [ ] **Colors match** original RGB palette
- [ ] **Aging synchronized** with dt timing
- [ ] **Boundary behavior identical** (bounce + clamp)

### Performance Tests
- [ ] **FPS stays ≥ 30** with all 45 squares active
- [ ] **No visual stuttering** or frame drops
- [ ] **Memory stable** (no leak during aging/regeneration)

---

## 8. Known Edge Cases & Gotchas

### 1. **Delta Time (dt) Parameter**
- **Python**: `clock.tick(FPS)` returns milliseconds → divide by 1000.0 to get seconds
- **JavaScript**: `Date.now()` returns milliseconds → divide by 1000.0 to get seconds
- **Gotcha**: If dt is in milliseconds, all movement will be 60x faster than intended
- **Check**: Print dt value; should be ~0.0167 seconds at 60 FPS

### 2. **Array Mutation During Iteration**
- **Python**: `squares[i] = Square(other.size)` replaces element after eating
- **JavaScript**: Must use identical pattern; do NOT use `Array.filter()` or shift/unshift as it changes indices
- **Gotcha**: If using `forEach()` or dynamic array methods, eat behavior will break
- **Check**: Verify squares count stays at 45 throughout simulation

### 3. **Integer Conversion for Pixel Coordinates**
- **Python**: `pygame.Rect(int(self.x), int(self.y), ...)`
- **JavaScript**: Should use `Math.floor()` or `Math.round()` for canvas coordinates
- **Gotcha**: Floating-point pixel positions can cause subtle visual differences
- **Check**: Consistency across drawing and collision (both should round same way)

### 4. **Floating-Point Precision in Collision**
- **Python**: Uses pygame's Rect with integer truncation
- **JavaScript**: AABB formula with floats (no truncation)
- **Gotcha**: Collisions may occur at slightly different boundaries
- **Mitigation**: Acceptable difference; both are AABB collision tests

### 5. **Brightness Calculation Order**
- **Python**: `brightness = 1 - (self.age / self.life_span); if brightness < MIN_BRIGHTNESS: brightness = MIN_BRIGHTNESS`
- **JavaScript**: Identical logic with `Math.max(MIN_BRIGHTNESS, 1 - age/lifeSpan)` or explicit if
- **Gotcha**: Minimum brightness must be applied after subtraction, not before
- **Check**: Old squares should never go completely black

### 6. **Random Angle Initialization**
- **Python**: `angle = random.uniform(0, 2 * math.pi)`
- **JavaScript**: `const angle = Math.random() * 2 * Math.PI`
- **Gotcha**: Different RNG algorithms may produce visibly different distributions (acceptable)
- **Check**: Squares should move in all directions uniformly

### 7. **Canvas Coordinate System**
- **Python/Pygame**: Origin (0, 0) at top-left, X right, Y down
- **JavaScript/Canvas**: Origin (0, 0) at top-left, X right, Y down
- **Equivalence**: ✓ Identical coordinate systems, no transformation needed

---

## 9. Validation Sign-Off

**Port is complete when:**
1. All methods above are implemented and callable
2. All constants match Python values
3. Game loop runs at ~60 FPS on modern browser
4. All 45 squares spawn, move, interact, age, and regenerate
5. FPS counter displays and updates
6. No console errors or warnings
7. Visual behavior matches Python version (colors, movement, aging)
8. Boundary bouncing is smooth and consistent
9. Collision-based eating grows squares correctly
10. Behavior changes (fleeing, chasing) are observable in motion


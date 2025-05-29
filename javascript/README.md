# Pathfinding Visualizer (A\*)

A simple browser-based visualizer for the A\* pathfinding algorithm on a 2D grid.  
Click to set start/end points, draw walls by clicking or click-and-drag, and watch A\* find the shortest path in real time.

---

## 📋 Features

- **Dynamic Grid**: Default to 50×50 cells; you can change rows/columns on the fly.
- **Start & End**: First two clicks choose the start (blue) and end (red) nodes.
- **Draw Walls**: Click cells or click-and-drag (after mousedown) to create/remove walls (black cells).
- **A\* Visualization**  
  - Open set (light green) vs. closed set (dark green) coloring  
  - Final shortest path highlighted in dark green
- **Animation Speed**: Set a delay (ms) to slow down traversal for better demonstration.
- **Reset/Clear**: Instantly reset the grid and controls to try another scenario.

---

## 🚀 Installation & Running Locally

1. **Clone or download** this folder so that you have:
   - `index.html`
   - `app.js`
2. Open a terminal in that folder and run any simple HTTP server. For example, with Python:
   ```bash
   python3 -m http.server 9090
   ```

3. In your browser, navigate to:

   ```
   http://localhost:9090
   ```

---

## 🖱 Controls & Usage

1. **Grid Size**

   * Adjust **Rows** and **Cols** inputs (5–100)
   * Click **Set Grid** to re-draw the empty grid
2. **Select Start & End**

   * Click one cell → it becomes **Start (blue)**
   * Click a different cell → it becomes **End (red)**
3. **Draw Walls**

   * **Click** on any non-start/end cell to toggle wall on/off
   * **Click & Drag** (mousedown + move) to paint walls rapidly
4. **Animation Speed**

   * Enter a delay in milliseconds (0 = instant)
5. **Start A\***

   * Click **Start A\*** once both start & end are set
   * Watch nodes move from light green (open) → dark green (closed)
   * Final path drawn in dark green
6. **Clear**

   * At any time (before, during, or after a run), click **Clear** to reset the grid and controls

---

## 📐 Configuration Defaults

* **Rows / Cols**: `50 × 50`
* **Cell Size**: `16px × 16px`
* **Default Delay**: `0 ms`

You can easily tweak cell size or initial defaults by editing the CSS/JS in `index.html` and `app.js`.

---

## 🛠️ File Structure

```
├── index.html   # Main page with controls & grid container
└── app.js       # All JavaScript logic: grid init, event handling, A* algorithm
```

---

## 🧑‍💻 Contributing

1. Fork this repository.
2. Create your feature branch: `git checkout -b my-feature`
3. Commit your changes: `git commit -m "Add awesome feature"`
4. Push to the branch: `git push origin my-feature`
5. Open a pull request.

---

## 📄 License

This project is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute!

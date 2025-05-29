let rows = 50, cols = 50, speed = 0;
const gridEl     = document.getElementById('grid');
const clearBtn   = document.getElementById('clearBtn');
const startBtn   = document.getElementById('startBtn');
const algoSelect = document.getElementById('algoSelect');

let startNode = null, endNode = null;
let cells     = [];  // 2D array of node objects

// track mouse state for drawing
let isMouseDown = false;
document.body.addEventListener('mousedown', () => isMouseDown = true);
document.body.addEventListener('mouseup',   () => isMouseDown = false);

// Control events
document.getElementById('setGrid').addEventListener('click', () => {
  rows = +document.getElementById('rows').value;
  cols = +document.getElementById('cols').value;
  reset();
});
clearBtn.addEventListener('click', reset);
document.getElementById('speed').addEventListener('input', e => {
  speed = +e.target.value;
});
startBtn.addEventListener('click', () => {
  if (!startNode || !endNode) {
    alert('Please pick a start and end.');
    return;
  }
  disableControls();
  runAlgorithm();
});

function reset() {
  // re-enable everything
  document.querySelectorAll('input, button, select').forEach(el => el.disabled = false);

  startNode = endNode = null;
  cells = [];
  gridEl.innerHTML = '';
  gridEl.style.gridTemplate = `repeat(${rows}, 1fr) / repeat(${cols}, 1fr)`;

  for (let r = 0; r < rows; r++) {
    cells[r] = [];
    for (let c = 0; c < cols; c++) {
      const div = document.createElement('div');
      div.classList.add('cell');
      gridEl.appendChild(div);

      const node = { r, c, div, wall: false, g: Infinity, f: Infinity, parent: null };
      div.addEventListener('mousedown', () => onCellClick(node));
      div.addEventListener('mouseover', () => {
        if (isMouseDown && startNode && endNode && node !== startNode && node !== endNode) {
          node.wall = true;
          node.div.classList.add('wall');
        }
      });
      cells[r][c] = node;
    }
  }
}

function onCellClick(node) {
  if (!startNode) {
    startNode = node;
    node.div.classList.add('start');
  } else if (!endNode && node !== startNode) {
    endNode = node;
    node.div.classList.add('end');
  } else if (node !== startNode && node !== endNode) {
    node.wall = !node.wall;
    node.div.classList.toggle('wall', node.wall);
  }
}

function disableControls() {
  document.querySelectorAll('input, button, select').forEach(el => {
    if (el !== clearBtn) el.disabled = true;
  });
}

function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function runAlgorithm() {
  const algo = algoSelect.value;
  // reset node visuals & scores
  for (const row of cells) {
    for (const n of row) {
      n.g = Infinity; n.f = Infinity; n.parent = null;
      n.div.classList.remove('open','closed','path');
    }
  }

  switch (algo) {
    case 'astar':    await aStar();    break;
    case 'dijkstra': await dijkstra(); break;
    case 'bfs':      await bfs();      break;
    case 'dfs':      await dfs();      break;
  }
}

// A* (with Manhattan heuristic)
async function aStar() {
  const openSet = [];
  startNode.g = 0;
  startNode.f = heuristic(startNode, endNode);
  openSet.push(startNode);
  startNode.div.classList.add('open');

  while (openSet.length) {
    openSet.sort((a,b) => a.f - b.f);
    const current = openSet.shift();
    current.div.classList.replace('open','closed');

    if (current === endNode) { reconstructPath(current); return; }
    for (const nbr of neighbors(current)) {
      if (nbr.wall || nbr.div.classList.contains('closed')) continue;
      const tentative = current.g + 1;
      if (tentative < nbr.g) {
        nbr.parent = current;
        nbr.g = tentative;
        nbr.f = tentative + heuristic(nbr, endNode);
        if (!openSet.includes(nbr)) {
          openSet.push(nbr);
          nbr.div.classList.add('open');
        }
      }
    }
    if (speed) await sleep(speed);
  }
  alert('No path found');
}

// Dijkstra = A* with zero heuristic
async function dijkstra() {
  const openSet = [];
  startNode.g = 0;
  openSet.push(startNode);
  startNode.div.classList.add('open');

  while (openSet.length) {
    openSet.sort((a,b) => a.g - b.g);
    const current = openSet.shift();
    current.div.classList.replace('open','closed');

    if (current === endNode) { reconstructPath(current); return; }
    for (const nbr of neighbors(current)) {
      if (nbr.wall || nbr.div.classList.contains('closed')) continue;
      const tentative = current.g + 1;
      if (tentative < nbr.g) {
        nbr.parent = current;
        nbr.g = tentative;
        if (!openSet.includes(nbr)) {
          openSet.push(nbr);
          nbr.div.classList.add('open');
        }
      }
    }
    if (speed) await sleep(speed);
  }
  alert('No path found');
}

// Breadth-First Search
async function bfs() {
  const queue = [startNode];
  startNode.div.classList.add('open');

  while (queue.length) {
    const current = queue.shift();
    current.div.classList.replace('open','closed');

    if (current === endNode) { reconstructPath(current); return; }
    for (const nbr of neighbors(current)) {
      if (nbr.wall || nbr.div.classList.contains('open') || nbr.div.classList.contains('closed')) continue;
      nbr.parent = current;
      queue.push(nbr);
      nbr.div.classList.add('open');
    }
    if (speed) await sleep(speed);
  }
  alert('No path found');
}

// Depth-First Search
async function dfs() {
  const stack = [startNode];
  startNode.div.classList.add('open');

  while (stack.length) {
    const current = stack.pop();
    current.div.classList.replace('open','closed');

    if (current === endNode) { reconstructPath(current); return; }
    for (const nbr of neighbors(current)) {
      if (nbr.wall || nbr.div.classList.contains('open') || nbr.div.classList.contains('closed')) continue;
      nbr.parent = current;
      stack.push(nbr);
      nbr.div.classList.add('open');
    }
    if (speed) await sleep(speed);
  }
  alert('No path found');
}

function reconstructPath(node) {
  let p = node;
  while (p) {
    if (p !== startNode && p !== endNode) p.div.classList.add('path');
    p = p.parent;
  }
}

function neighbors({ r, c }) {
  const list = [];
  [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr, dc]) => {
    const nr = r + dr, nc = c + dc;
    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
      list.push(cells[nr][nc]);
    }
  });
  return list;
}

function heuristic(a, b) {
  return Math.abs(a.r - b.r) + Math.abs(a.c - b.c);
}

// initial render
reset();

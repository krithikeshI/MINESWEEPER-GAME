const rows = 10;
const cols = 10;
const minesCount = 15;
let board = [];
let revealedCount = 0;

const boardDiv = document.getElementById("board");
const statusText = document.getElementById("status");

// Initialize the board
function createBoard() {
  boardDiv.innerHTML = "";
  board = Array.from({ length: rows }, () => Array(cols).fill(0));

  // Place mines
  let minePositions = [];
  while (minePositions.length < minesCount) {
    const pos = Math.floor(Math.random() * rows * cols);
    if (!minePositions.includes(pos)) minePositions.push(pos);
  }

  for (let pos of minePositions) {
    const r = Math.floor(pos / cols);
    const c = pos % cols;
    board[r][c] = "M";
  }

  // Calculate numbers
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (board[r][c] === "M") continue;
      let mines = 0;
      for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
          const nr = r + i, nc = c + j;
          if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc] === "M") {
            mines++;
          }
        }
      }
      board[r][c] = mines;
    }
  }

  // Create buttons
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("button");
      cell.classList.add("cell");
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.addEventListener("click", () => revealCell(r, c));
      boardDiv.appendChild(cell);
    }
  }
}

function revealCell(r, c) {
  const cell = document.querySelector(`button[data-row='${r}'][data-col='${c}']`);
  if (cell.classList.contains("revealed")) return;

  cell.classList.add("revealed");
  if (board[r][c] === "M") {
    cell.textContent = "💣";
    cell.classList.add("mine");
    gameOver();
  } else {
    cell.textContent = board[r][c] === 0 ? "" : board[r][c];
    revealedCount++;
    if (board[r][c] === 0) {
      for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
          const nr = r + i, nc = c + j;
          if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) revealCell(nr, nc);
        }
      }
    }
    checkWin();
  }
}

function gameOver() {
  statusText.textContent = "💀 Game Over!";
  document.querySelectorAll(".cell").forEach(btn => btn.disabled = true);
}

function checkWin() {
  if (revealedCount === rows * cols - minesCount) {
    statusText.textContent = "🎉 You Win!";
    document.querySelectorAll(".cell").forEach(btn => btn.disabled = true);
  }
}

createBoard();

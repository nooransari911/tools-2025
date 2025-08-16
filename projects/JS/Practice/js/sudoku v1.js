// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', InitializeApp);

/**
 * @description Initializes the application, sets up the grid, and attaches event listeners.
 */
function InitializeApp() {
    const gridContainer = document.getElementById('sudoku-grid');
    const solveButton = document.getElementById('solve-button');
    const clearButton = document.getElementById('clear-button');
    const messageArea = document.getElementById('message-area');

    CreateGrid(gridContainer);
    
    // Attach event listeners using named functions, avoiding inline callbacks
    solveButton.addEventListener('click', HandleSolveClick);
    clearButton.addEventListener('click', HandleClearClick);
}

/**
 * @description Creates the 9x9 input grid dynamically.
 * @param {HTMLElement} gridContainer - The container element for the grid.
 */
function CreateGrid(gridContainer) {
    gridContainer.innerHTML = ''; // Clear any existing content
    for (let i = 0; i < 9; i++) {
        const row = document.createElement('div');
        row.className = 'grid grid-cols-9 gap-0.5';
        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('input');
            cell.type = 'number';
            cell.className = 'sudoku-cell bg-white';
            cell.min = '1';
            cell.max = '9';
            // Prevent non-numeric input
            cell.addEventListener('input', () => {
                if (cell.value.length > 1) {
                    cell.value = cell.value.slice(0, 1);
                }
            });
            row.appendChild(cell);
        }
        gridContainer.appendChild(row);
    }
}


/**
 * @description Handles the click event for the 'Solve' button.
 */
function HandleSolveClick() {
    const messageArea = document.getElementById('message-area');
    messageArea.textContent = 'Solving...';
    messageArea.classList.remove('text-red-500', 'text-green-500');
    messageArea.classList.add('text-gray-600');

    // Use a timeout to allow the UI to update before the potentially long-running solve operation
    setTimeout(() => {
        const board = GetBoardState();
        if (SolveSudoku(board)) {
            SetBoardState(board);
            messageArea.textContent = 'Puzzle Solved!';
            messageArea.classList.add('text-green-500');
        } else {
            messageArea.textContent = 'No solution exists for this puzzle.';
            messageArea.classList.add('text-red-500');
        }
    }, 10);
}

/**
 * @description Handles the click event for the 'Clear' button.
 */
function HandleClearClick() {
    const gridContainer = document.getElementById('sudoku-grid');
    const messageArea = document.getElementById('message-area');
    
    const cells = gridContainer.getElementsByTagName('input');
    for (let cell of cells) {
        cell.value = '';
    }
    
    messageArea.textContent = '';
}

/**
 * @description Reads the current values from the HTML input grid into a 2D array.
 * @returns {number[][]} A 9x9 array representing the Sudoku board. Empty cells are 0.
 */
function GetBoardState() {
    const board = [];
    const gridContainer = document.getElementById('sudoku-grid');
    const rows = gridContainer.children;

    for (let i = 0; i < 9; i++) {
        const row = [];
        const cells = rows[i].children;
        for (let j = 0; j < 9; j++) {
            const value = parseInt(cells[j].value, 10) || 0;
            row.push(value);
        }
        board.push(row);
    }
    return board;
}

/**
 * @description Populates the HTML input grid from a 2D array.
 * @param {number[][]} board - A 9x9 array with the Sudoku solution.
 */
function SetBoardState(board) {
    const gridContainer = document.getElementById('sudoku-grid');
    const rows = gridContainer.children;

    for (let i = 0; i < 9; i++) {
        const cells = rows[i].children;
        for (let j = 0; j < 9; j++) {
            cells[j].value = board[i][j];
        }
    }
}

/**
 * @description Solves the Sudoku puzzle using a backtracking algorithm.
 * @param {number[][]} board - The Sudoku board to solve.
 * @returns {boolean} True if a solution is found, false otherwise.
 */
function SolveSudoku(board) {
    const find = FindEmptyCell(board);
    if (!find) {
        return true; // Puzzle is solved
    }

    const { row, col } = find;

    for (let num = 1; num <= 9; num++) {
        if (IsSafe(board, row, col, num)) {
            board[row][col] = num;

            if (SolveSudoku(board)) {
                return true;
            }

            board[row][col] = 0; // Backtrack
        }
    }

    return false; // No number worked, trigger backtracking
}

/**
 * @description Finds the next empty cell (represented by 0) in the grid.
 * @param {number[][]} board - The Sudoku board.
 * @returns {{row: number, col: number}|null} An object with row and col, or null if no empty cell is found.
 */
function FindEmptyCell(board) {
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            if (board[row][col] === 0) {
                return { row, col };
            }
        }
    }
    return null;
}

/**
 * @description Checks if placing a number in a specific cell is valid.
 * @param {number[][]} board - The Sudoku board.
 * @param {number} row - The row index.
 * @param {number} col - The column index.
 * @param {number} num - The number to check.
 * @returns {boolean} True if the placement is valid, false otherwise.
 */
function IsSafe(board, row, col, num) {
    return !UsedInRow(board, row, num) &&
           !UsedInCol(board, col, num) &&
           !UsedInBox(board, row - row % 3, col - col % 3, num);
}

/**
 * @description Checks if a number is already used in the given row.
 * @param {number[][]} board - The Sudoku board.
 * @param {number} row - The row index to check.
 * @param {number} num - The number to check for.
 * @returns {boolean} True if the number is used, false otherwise.
 */
function UsedInRow(board, row, num) {
    for (let col = 0; col < 9; col++) {
        if (board[row][col] === num) {
            return true;
        }
    }
    return false;
}

/**
 * @description Checks if a number is already used in the given column.
 * @param {number[][]} board - The Sudoku board.
 * @param {number} col - The column index to check.
 * @param {number} num - The number to check for.
 * @returns {boolean} True if the number is used, false otherwise.
 */
function UsedInCol(board, col, num) {
    for (let row = 0; row < 9; row++) {
        if (board[row][col] === num) {
            return true;
        }
    }
    return false;
}

/**
 * @description Checks if a number is already used in the 3x3 sub-grid.
 * @param {number[][]} board - The Sudoku board.
 * @param {number} boxStartRow - The starting row index of the 3x3 box.
 * @param {number} boxStartCol - The starting column index of the 3x3 box.
 * @param {number} num - The number to check for.
 * @returns {boolean} True if the number is used, false otherwise.
 */
function UsedInBox(board, boxStartRow, boxStartCol, num) {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            if (board[row + boxStartRow][col + boxStartCol] === num) {
                return true;
            }
        }
    }
    return false;
}

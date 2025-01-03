var id=0;
var amount=0;
function showEditMenu(expense_id,expense_amount){
    document.getElementById('edit_menu').style.display='block';

    // expense id is globalized to share it to other functions as well

    id=expense_id;
    amount=expense_amount;
    document.getElementById("exp_id_edit").textContent=id;
    document.getElementById('return_amount').textContent=amount;
}

function edit_expense(){
    
    document.getElementById('edit_expense').style.display="block";
    document.getElementById('add_amount_form').style.display="none";
    const form = document.getElementById('edit_expense');
    form.action = `/edit_expense/${id}`;
    
}

function add_amount(){
    document.getElementById('add_amount_form').style.display="block";
    document.getElementById('edit_expense').style.display="none";
    const form = document.getElementById('add_amount_form');
    form.action = `/add_amount/${id}`;
    
}

function close_menu(){
    document.getElementById('add_amount_form').style.display='none';
    document.getElementById('edit_expense').style.display='none';
    document.getElementById('edit_menu').style.display='none';
}

let originalOrder = []; // Stores the default order of rows.

function sortTable(columnIndex, header) {
    const table = document.querySelector("table tbody");
    const rows = Array.from(table.rows);

    // Save original order only once
    if (originalOrder.length === 0) {
        originalOrder = rows.map(row => row.cloneNode(true));
    }

    // Get current sort order from the header
    const currentOrder = header.getAttribute("data-sort-order");
    let newOrder;

    if (currentOrder === "none" || currentOrder === "desc") {
        // Sort in ascending order
        newOrder = rows.sort((rowA, rowB) => {
            const cellA = rowA.cells[columnIndex].innerText.trim();
            const cellB = rowB.cells[columnIndex].innerText.trim();
            return isNaN(cellA) ? cellA.localeCompare(cellB) : parseFloat(cellA) - parseFloat(cellB);
        });
        header.setAttribute("data-sort-order", "asc");
    } else if (currentOrder === "asc") {
        // Sort in descending order
        newOrder = rows.sort((rowA, rowB) => {
            const cellA = rowA.cells[columnIndex].innerText.trim();
            const cellB = rowB.cells[columnIndex].innerText.trim();
            return isNaN(cellA) ? cellB.localeCompare(cellA) : parseFloat(cellB) - parseFloat(cellA);
        });
        header.setAttribute("data-sort-order", "desc");
    } else {
        // Restore to default order
        newOrder = originalOrder;
        header.setAttribute("data-sort-order", "none");
    }

    // Clear the table and append the sorted rows
    table.innerHTML = "";
    newOrder.forEach(row => table.appendChild(row));

    // Reset other headers' sort order
    document.querySelectorAll("thead th").forEach(th => {
        if (th !== header) {
            th.setAttribute("data-sort-order", "none");
        }
    });
}


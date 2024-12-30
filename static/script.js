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

// function show_cart(){
//     for(let i = 1; i < 4; i++){
//         id = `item_cell_${i}`
//         console.log(id);
//         item_cell = document.getElementById(id);
//         console.log(item_cell);
//     }   
// }


if (window.location.href == 'http://127.0.0.1:8000/page/basket/'){
    items = document.getElementsByClassName('item_name');
    
    for (let i = 0; i < 8; i++){
        console.log(items[i].textContent);
        if (items[i].textContent == ''){
            console.log(i);
            let cell = document.getElementById(`cart-cell-${i + 1}`);
            cell.style.display = 'none';
        }
    }
}


function cart_encrease_item(button_id){
    let h_quanity = document.getElementsByClassName(`item_quantity_${button_id}`);
    let quanity = h_quanity[0].textContent;
    let price = document.getElementsByClassName(`item_price_${button_id}`)[0].textContent;
    let h_fullprice = document.getElementsByClassName(`item_fullprice_${button_id}`);
    let fullprice = h_fullprice[0].textContent;

    h_quanity[0].textContent = String(parseInt(quanity) + 1);
    h_fullprice[0].textContent = String((parseInt(quanity) + 1) * parseInt(price));

}


function cart_decrease_item(button_id){
    let h_quanity = document.getElementsByClassName(`item_quantity_${button_id}`);
    let quanity = h_quanity[0].textContent;
    let price = document.getElementsByClassName(`item_price_${button_id}`)[0].textContent;
    let h_fullprice = document.getElementsByClassName(`item_fullprice_${button_id}`);
    let fullprice = h_fullprice[0].textContent;
    if (parseInt(quanity) == 1){
        return 0
    }

    h_quanity[0].textContent = String(parseInt(quanity) - 1);
    h_fullprice[0].textContent = String((parseInt(quanity) - 1) * parseInt(price));
}

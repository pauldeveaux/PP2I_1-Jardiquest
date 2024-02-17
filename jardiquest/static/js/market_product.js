/** Change the display value for the cost */
document.querySelectorAll(".buy_quantity").forEach((element) => {
  element.onchange = () => {
    let quantity = parseFloat(element.value);
    let price = parseFloat(element.parentNode.parentNode.querySelector(".price").innerHTML);
    let total = (quantity * price).toFixed(2);
    element.parentNode.querySelector(".cost_float").innerHTML = total; 
  }  
});

if (document.querySelector("#sort_sellings")){
  document.querySelector("#sort_sellings").onchange = (ev) => {
    element = ev.target
    parent = element.parentNode.parentNode
    nodes = parent.querySelectorAll(".market_product_selling")
    array = []
    nodes.forEach((node) => {
      array.push(node)
      node.remove()
    })
    if (element.value.toLowerCase() == "price") {sort_by_price(array)}
    else if (element.value.toLowerCase() == "quantity") {sort_by_quantity(array)}
    else if (element.value.toLowerCase() == "date") {sort_by_date(array)}
    array.forEach((node) => {
      parent.appendChild(node)
    });
  }
}



function sort_by_price(data) {
  data.sort((a, b) => {
    return parseFloat(a.querySelector(".price").innerHTML) - parseFloat(b.querySelector(".price").innerHTML);
  });
};

function sort_by_quantity(data){
  data.sort((b, a) => {
    return parseFloat(a.querySelector(".quantity_float").innerHTML) - parseFloat(b.querySelector(".quantity_float").innerHTML);
  });
}

function sort_by_date(data){
  data.sort((b, a) => {
    return new Date(a.querySelector(".date").innerHTML) - new Date(b.querySelector(".date").innerHTML);
  });
}


/* Buy confirmation */
document.querySelectorAll(".buy_form").forEach((node) => {
  node.addEventListener("submit", (ev) => {
    document.querySelector("#button_confirm_buy").onclick = () => {
      ev.target.submit()
    }
    ev.preventDefault()
  });
})

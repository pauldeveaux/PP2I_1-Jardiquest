/** Sort */
parent = document.querySelector("#market_products")
document.querySelector("#sort_products").onchange = (ev) => {
    element = ev.target
    nodes = parent.querySelectorAll(".product")
    array = []
    nodes.forEach((node) => {
      array.push(node)
      node.remove()
    })
    if (element.value.toLowerCase() == "price") {sort_by_price(array)}
    else if (element.value.toLowerCase() == "quantity") {sort_by_quantity(array)}
    else if (element.value.toLowerCase() == "type") {sort_by_type(array)}
    else if (element.value.toLowerCase() == "name") {sort_by_name(array)}
    array.forEach((node) => {
      parent.appendChild(node)
    });
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

function sort_by_name(data){
data.sort((a, b) => {
    return a.querySelector(".name").innerHTML.localeCompare(b.querySelector(".name").innerHTML);
});
}
function sort_by_type(data){
data.sort((a, b) => {
    return a.querySelector(".type").innerHTML.localeCompare(b.querySelector(".type").innerHTML);
});
}

/* Filter */
document.querySelector("#filter_type").onchange = (ev) => {
    nodes = parent.querySelectorAll(".product")
    nodes.forEach((node) => {
        if (node.querySelector(".type").innerHTML.toLowerCase() == ev.target.value.toLowerCase()){
            node.style.display = node.previousDisplay
        }
        else if (ev.target.value.toLowerCase() == "all"){
            node.style.display = node.previousDisplay
        }
        else {
            if(window.getComputedStyle(node).display != "none"){
                node.previousDisplay = window.getComputedStyle(node).display
            }
            node.style.display = "none";
        }
    });
}
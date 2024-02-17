parent = document.querySelector("#orders")
if (document.querySelector("#orders_sort") ){
  document.querySelector("#orders_sort").onchange = (ev) => {
    element = ev.target
    nodes = parent.querySelectorAll(".order")
    array = []
    nodes.forEach((node) => {
      array.push(node)
      node.remove()
    })
    if (element.value.toLowerCase() == "user") {sort_by_user(array)}
    else if (element.value.toLowerCase() == "date") {sort_by_date(array)}
    array.forEach((node) => {
      parent.appendChild(node)
    });
}
}


function sort_by_user(array) {
    array.sort((a, b) => {
        return a.querySelector(".username").innerHTML.localeCompare(b.querySelector(".username").innerHTML);
    });
}

function sort_by_date(data){
    data.sort((b, a) => {
      return new Date(a.querySelector(".date").innerHTML) - new Date(b.querySelector(".date").innerHTML);
    });
  }


/* Filter */
if(document.querySelector("#filter_states")){
  document.querySelector("#filter_states").onchange = (ev) => {
    nodes = parent.querySelectorAll(".order")
    nodes.forEach((node) => {
        if (node.querySelector(".state_value").innerHTML.toLowerCase() == ev.target.value.toLowerCase()){
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
}
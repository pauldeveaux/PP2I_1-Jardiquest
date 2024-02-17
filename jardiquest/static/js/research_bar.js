/** Need to define an html class for :
 * - the research bar (#research_bar)
 * - the research items (.searching_items)
 * - the property of the research (.searching_property)
 */
searchingItems = document.querySelectorAll(".searching_items");
document.querySelector("#research_bar").addEventListener("input", function(e) {
    searchingItems.forEach(function(item) {        
        if (item.querySelector(".searching_property").textContent.toLowerCase().includes(e.target.value.toLowerCase())){
            item.style.display = item.previousDisplay
        }
        else {
            if(window.getComputedStyle(item).display != "none"){
                item.previousDisplay = window.getComputedStyle(item).display
            }
            item.style.display = "none";
        }
    });
});


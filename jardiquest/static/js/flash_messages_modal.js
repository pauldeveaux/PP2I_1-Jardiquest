window.addEventListener("load", function() { 
    if (this.document.querySelector("#flash_messages")) {
        let html = `
        <div class="modal fade" id="flash_modal" role="dialog">
            <div class="modal-dialog">
            
            <!-- Modal content-->
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="brown-orange-style"><p>${document.querySelector("#category_message").innerHTML}</p></h4>
                </div>
                <div class="modal-body">
                    <p>${document.querySelector("#flash_message").innerHTML}</p>
                </div>
                <div class="modal-footer">
                    ${document.querySelector("#flash_message_buttons").innerHTML }
                </div>
            </div>        
        </div>`;
        let div = document.createElement('div')
        div.innerHTML = html;
        let a = document.querySelector("#flash_messages")
        a.append(div);
        
        $("#flash_modal").modal();
    };
});
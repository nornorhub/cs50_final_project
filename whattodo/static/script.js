
// Creates an item in the list
$('#CreateItem').click(() => {
    $('#List').append(`
    
    <li style='list-style-type:none'>

        <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <div class="input-group-text bg-primary">
                        <input type="checkbox" aria-label="Checkbox for following text input">
                    </div>
                </div>
                <input type="text" class="form-control" aria-label="Text input with checkbox">
                <div class="input-group-append">
                    <button class="btn btn-danger" type="button" id="button-addon2">Delete Item</button>
                </div>
        </div>

    </li>

    `)
})


// Deletes an item
$(document).on('click', '.btn-danger', (e) => {
    let listItem = e.target.parentNode.parentNode.parentNode
    listItem.innerHTML = ''
    listItem.parentNode.removeChild(listItem)
})


// Saves the list and validates list items' values
$("#SaveList").click(() => {

    let todoList = document.querySelectorAll('.input-group')
    let list_values = []
    for (let i = 0; i < todoList.length; i++)
    {
        let item = todoList[i];
        list_values[i] = {
            "todo": item.children[1].value,
            "checked": item.children[0].children[0].children[0].checked
        }
        
    }

    if (todoList.length > 0)
    {
        for (let i = 0; i < list_values.length; i++)
        {
            if (list_values[i].todo == "")
            {
                
                $('.container').prepend(`
        
                    <div class="alert alert-warning alert-dismissible fade show" role="alert">
                        List hasn't been saved. Item ${i + 1} can not be empty.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>

                `)
                return;                
            }
        }
    }
    else
    {
        $('.container').prepend(`
        
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
            You have to create at least one item.
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
        </div>

        `)
        return;
    }

    $.ajax({
        type: "POST",
        url: '/',
        data: JSON.stringify(list_values),
        success: (data) => {
            $('.container').prepend(`
        
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${data}
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>

            `)
        },
        contentType: 'application/json'
    })

})

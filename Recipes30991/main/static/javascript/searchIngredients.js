// Gets all the selected checkboxes.
function getSelectCheckboxes() {
    var entryList, cBoxes, item, cBoxChecked;
    entryList = document.getElementById("ingredientList");
    cBoxes = entryList.getElementsByTagName("input");
    cBoxChecked = [];
    for (i = 0; i < cBoxes.length; i++) {
        if (cBoxes[i].checked) {
            cBoxChecked.push(cBoxes[i]);
        }
    }
    return cBoxChecked;
}

// Gets a list of select checkboxes.
function updateSelectList() {
    var cBoxes, selectList;
    cBoxes = getSelectCheckboxes();
    selectList = document.getElementById("ingredientsSelected");
    selectList.innerHTML = "";
    for (i = 0; i < cBoxes.length; i++) {
        var node = document.createElement("span");
        node.className = "badge badge-primary";
        node.style = "margin:2px;";
        node.innerHTML = cBoxes[i].value;
        selectList.appendChild(node);
    }
}

// Unchecks all the checkboxes.
function clearSelections() {
    var entryList, cBoxes, item;
    entryList = document.getElementById("ingredientList");
    cBoxes = entryList.getElementsByTagName("input");
    for (i = 0; i < cBoxes.length; i++) {
        item = cBoxes[i]
        if (item.type == "checkbox") {
            item.checked = false;
        }
    }
    updateSelectList()
}

// Function used to check if searchbar is blank.
function searchIsBlank(txt){
    return txt === null || txt.match(/^ *$/) !== null;
}

// Function used to hide checkboxes. It uses searchbar as reference.
function searchIngredients() {
	var input, filter, entryList, entries, item, i, n, txtValue;
	input = document.getElementById("ingredientInput");
	filter = input.value.toLowerCase();
	entryList = document.getElementById("ingredientList");
	entries = entryList.getElementsByTagName("tr");
	// Don't display the results when the searchbar is empty.
	if (searchIsBlank(filter)) {
	    for (i = 0; i < entries.length; i++) {
	        entries[i].style.display = "none";
	    }
	// Display the results when the searchbar is not empty. One character required!
	} else {
	    n = 0;
	    for (i = 0; i < entries.length; i++) {
			item = entries[i];
			txtValue = item.id;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                item.style.display = "";
                n += 1;
                // Coloring for visible elements.
                if (n % 2 == 0) {
                    item.className = "table-light";
                } else {
                    item.className = "";
                }
            } else {
                item.style.display = "none";
            }
	    }
	}
}
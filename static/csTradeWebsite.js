//filter data
var datapack = []
function filter(form) {
    var params = []
    event.preventDefault()
    var params = {'from':form.from.value, 'to':form.to.value, 'min':form.min.value, 'max':form.max.value}
    var paramjson = JSON.stringify(params)
    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
    });
    $.post("/filtersubmit", paramjson, function( data ) {
        datapack = []
        datapack = JSON.parse(data)
        datapack.sort(sortFunction);
        function sortFunction(a, b) {
            if (a[3] === b[3]) {
                return 0;
            }
            else {
                return (a[3] < b[3]) ? -1 : 1;
            }
        }
        rendertable(datapack)
        if (percentdown == false){
            sortpercent(false)
        }
        if (selldown == false){
            sortsellprice(false)
        }
        if (buydown == false) {
            sortbuyprice(false)
        }
    });
}

function rendertable(datapack) {
    var table = document.getElementById('datatable')
    tableleng = table.rows.length-1
    for(i = 0; i < tableleng; i++) {
        table.deleteRow(0)
    }
    for(i in datapack){
        var row = table.insertRow(1)
        var c1 = row.insertCell(0)
        var c2 = row.insertCell(0)
        var c3 = row.insertCell(0)
        var c4 = row.insertCell(0)
        c4.id = 'namecell'
        c1.innerHTML = datapack[i][3]
        c2.innerHTML = datapack[i][2]
        c3.innerHTML = datapack[i][1]
        c4.innerHTML = datapack[i][0]
    } 
}

function refDirectory(site) {
    var url = document.getElementById(site).options[document.getElementById(site).selectedIndex].text
    if(url == 'swap.gg') { //replace url with the referal link 
        url = 'swap.gg'
    }
    else if (url == tradeit.gg) {
        url = 'https://tradeit.gg/r/3RB6TX5'
    }
    window.open("https://tradeit.gg/r/3RB6TX5", "_blank");
}

//sort data
var sortactiveprevious = 0
var sortactive = 0
var percentdown = true
var selldown = true
var buydown = true
descending = true


function sortsellprice(sorting) {
    sorttriangle = document.getElementById('selltriangle')
    sortactive = 1
    selldown = arrowflip(sorttriangle, selldown, sortactive)
    if(sorting != false) {
        sortdata(1)
        rendertable(datapack)
    }
}

function sortbuyprice(sorting) {
    sorttriangle = document.getElementById('buytriangle')
    sortactive = 2
    buydown = arrowflip(sorttriangle, buydown, sortactive)
    if(sorting != false) {
        sortdata(2)
        rendertable(datapack)
    }
}

function sortpercent(sorting) {
    sorttriangle = document.getElementById('percenttriangle')
    sortactive = 3
    percentdown = arrowflip(sorttriangle, percentdown, sortactive)
    if(sorting != false) {
        sortdata(3)
        rendertable(datapack)
    }
}
function arrowflip(triangle, position, sortactive) {    
    if(sortactiveprevious == 2 && sortactive != 2) { //fixing buy sort
        document.getElementById('buytriangle').classList.remove('sort-by-desc')
        document.getElementById('buytriangle').classList.toggle('sortrectangle')
        document.getElementById('buytriangle').style.transform = 'rotateX(0deg)'
        buydown = true
    }
    if(sortactiveprevious == 1 && sortactive != 1) { //fixing sell sort
        document.getElementById('selltriangle').classList.remove('sort-by-desc')
        document.getElementById('selltriangle').classList.toggle('sortrectangle')
        document.getElementById('selltriangle').style.transform = 'rotateX(0deg)'
        selldown = true
    }
    if(sortactiveprevious == 3 && sortactive != 3) { //fixing sell sort
        document.getElementById('percenttriangle').classList.remove('sort-by-desc')
        document.getElementById('percenttriangle').classList.toggle('sortrectangle')
        document.getElementById('percenttriangle').style.transform = 'rotateX(0deg)'
        percentdown = true
    }
    if(sortactiveprevious != sortactive) {
        descending = true
        triangle.classList.toggle('sort-by-desc')
        triangle.classList.remove("sortrectangle")
        sortactiveprevious = sortactive
        position = true
        return position
    }
    else if (position == false) { //rotates the correct arrow
        triangle.style.transform = 'rotateX(0deg)'
        position = true
        descending = true
        return position
    }
    else {
        triangle.style.transform = 'rotateX(180deg)'
        position = false
        descending = false
        return position
    }
}
function sortdata(type) {
    var num;
    if (type == 1) {
        num = 2
    }
    if (type == 2) (
        num = 1
    )
    if (type == 3) {
        num = 3
    }
    datapack.sort(sortFunction)
    function sortFunction(a, b) {
        if(descending == false) {
            if (a[num] === b[num]) {
                return 0;
            }
            else {
                return (a[num] > b[num]) ? -1 : 1;
            }  
        }
        else if(descending == true) {
            if (a[num] === b[num]) {
                return 0;
            }
            else {
                return (a[num] < b[num]) ? -1 : 1;
            }  
        }
    }
}
function searchData() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchbox");
    filter = input.value;
    table = document.getElementById("datatable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length-1; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.indexOf(filter) > -1) {
          tr[i].style.display = "";
        } 
        else {
          tr[i].style.display = "none";
          console.log(txtValue)
        }
        }
    }
}
window.onload = function() {
    filter(document.getElementById("filterform"))
}
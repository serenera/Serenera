
var __name__ = "__main__";
var a, b;
a = 20;
b = 20;
function addition() {
    //document.getElementById("result").innerHTML = a + b;
    //window.open("http://127.0.0.1:5000/"); 
// Requiring fs module in which  
// readFile function is defined. 
     var xhr = new XMLHttpRequest();
     xhr.open('GET', chrome.extension.getURL('try'), true);
     xhr.onreadystatechange = function()
     {
          if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200)
         {
        //... The content has been read in xhr.responseText
         document.getElementById("result").innerHTML = xhr.responseText;
         }
};
xhr.send();


}


function add() {
    //document.getElementById("result").innerHTML = a + b;
    window.open("http://127.0.0.1:5000/"); 
// Requiring fs module in which  
// readFile function is defined. 
     var xhr = new XMLHttpRequest();
     xhr.open('GET', chrome.extension.getURL('try'), true);
     xhr.onreadystatechange = function()
     {
          if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200)
         {
        //... The content has been read in xhr.responseText
         document.getElementById("result").innerHTML = xhr.responseText;
         }
};
xhr.send();


}




document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('compute');
    // onClick's logic below:
    link.addEventListener('click', function() {
	addition();
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('details');
    // onClick's logic below:
    link.addEventListener('click', function() {
	add();
    });
});



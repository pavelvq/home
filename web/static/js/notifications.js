function notificator() {
	var x = document.getElementById("snackbar");
	x.className = ""; 
	fetch("/notifications?request=last").then((response) => {  
	  response.text().then((text) => {
		if (text != "") {
			var n = JSON.parse(text)
			if (n.type == "error") {
				x.style.backgroundColor = "#d20033";
			}
			else if (n.type == "warn") {
				x.style.backgroundColor = "#d1d200";
			}
			else if (n.type == "info") {
				x.style.backgroundColor = "#00d25b";
			}
			x.innerHTML = "<b>"+n.from+"</b> | "+n.message;
			x.className = "show";
		}
	  });
	});
	
	setTimeout(notificator, 4000);
}

//function notificator2() {
//  	var x = document.getElementById("ncdrop");
//	  
//  	fetch("/notifications?request=all").then((response) => {
//  	  response.text().then((text) => {
//  		if (text != "") {
//  			for (const element of JSON.parse(text)) {
//  			  console.log(element);
//  			}
//  		}
//  	  });
//  	});
//	
//  	setTimeout(notificator2, 10000);
//}

function nclear() {
	fetch("/notifications?request=clear")
}

setTimeout(notificator, 1000);
function standard(ssid) {
	var modal = $('#controlModal');
	modal.find('.modal-title').text('Set standard');
	modal.find('.modal-body').find('.ssid input').val(ssid);
	setpass(modal.find('.modal-body').find('.password input'), ssid);
	modal.find('.modalsend').attr('onClick','sendstandard()');
	modal.modal('show');
}

function sendstandard() {
	var status = $('#statustext');
	if (status.text() != "loading...") {
		var modal = $('#controlModal');
		var ssid = modal.find('.modal-body').find('.ssid input').val().replace(" ", "");
		var password = modal.find('.modal-body').find('.password input').val().replace(" ", "");
		if (password.length > 7 && ssid.length > 0) {
			status.text("loading...");
			modal.modal('hide');
			fetch("/module/wifi?request=standard&ssid="+ssid+"&pass="+password).then((response) => {  
			  response.text().then((text) => {
				if (text == "ok") {
					fetch("/module/wifi/scan").then((response) => {
					  response.text().then((text) => {
						status.text("Completed");
						document.getElementsByClassName("dbname")[0].textContent = "Wifi List";
						document.getElementsByClassName("dbtable")[0].innerHTML = text;
					  });
					});
				}
				else {
					status.text("Error");
				}
			  });
			});
		}
	}
}

function connect(ssid) {
	var modal = $('#controlModal');
	modal.find('.modal-title').text('Connect');
	modal.find('.modal-body').find('.ssid input').val(ssid);
	setpass(modal.find('.modal-body').find('.password input'), ssid);
	modal.find('.modalsend').attr('onClick','sendconnect()');
	modal.modal('show');
}

function sendconnect() {
	var status = $('#statustext');
	if (status.text() != "loading...") {
		var modal = $('#controlModal');
		var ssid = modal.find('.modal-body').find('.ssid input').val().replace(" ", "");
		var password = modal.find('.modal-body').find('.password input').val().replace(" ", "");
		if (password.length > 7 && ssid.length > 0) {
			status.text("loading...");
			modal.modal('hide');
			fetch("/module/wifi?request=connect&ssid="+ssid+"&pass="+password).then((response) => {  
			  response.text().then((text) => {
				if (text == "ok") {
					fetch("/module/wifi/scan").then((response) => {
					  response.text().then((text) => {
						status.text("Completed");
						document.getElementsByClassName("dbname")[0].textContent = "Wifi List";
						document.getElementsByClassName("dbtable")[0].innerHTML = text;
					  });
					});
					fetch("/module/wifi?request=getconnected").then((response) => {
					  response.text().then((text) => {
						$('#connectedto').text(text);
					  });
					});
				}
				else {
					status.text("Error");
				}
			  });
			});
		}
	}
}

function setpass(element, ssid) {
	fetch("/module/wifi?request=getpass&ssid="+ssid).then((response) => {
	  response.text().then((text) => {
		element.val(text);
	  });
	});
}

function disconnect() {
	var status = $('#statustext');
	if (status.text() != "loading...") {
		status.text("loading...");
		fetch("/module/wifi?request=disconnect").then((response) => {
		  response.text().then((text) => {
			if (text == "ok") {
				fetch("/module/wifi/scan").then((response) => {
				  response.text().then((text) => {
					status.text("Completed");
					document.getElementsByClassName("dbname")[0].textContent = "Wifi List";
					document.getElementsByClassName("dbtable")[0].innerHTML = text;
				  });
				});
				fetch("/module/wifi?request=getconnected").then((response) => {
				  response.text().then((text) => {
					$('#connectedto').text(text);
				  });
				});
			}
			else {
				status.text("Error");
			}
		  });
		});
	}
}

function rstandard() {
	var status = $('#statustext');
	if (status.text() != "loading...") {
		status.text("loading...");
		fetch("/module/wifi?request=rstandard").then((response) => {
		  response.text().then((text) => {
			if (text == "ok") {
				fetch("/module/wifi/scan").then((response) => {
				  response.text().then((text) => {
					status.text("Completed");
					document.getElementsByClassName("dbname")[0].textContent = "Wifi List";
					document.getElementsByClassName("dbtable")[0].innerHTML = text;
				  });
				});
			}
			else {
				status.text("Error");
			}
		  });
		});
	}
}

function showpass(field) {
	var f = $('#passfield'+field);
	if (f.attr('type') == "password") {
		f.attr('type','text');
	}
	else {
		f.attr('type','password');
	}
}
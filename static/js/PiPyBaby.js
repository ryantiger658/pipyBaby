// Function to get the enviroment information
function getEnv() {
	$.getJSON("env", function(data) {
		$("#theCurrentTemp").text(data.temperature);
		$("#theCurrentHumid").text(data.humidity);
	});
}

$(document).ready(function(){
	// Try to get the enviroment information as soon as the page is ready
	getEnv();
});

// Get the enviroment information every 35 seconds
window.setInterval(function(){
	getEnv();
}, 5000);


function load() {
                   
//get daily JSON file code ref: Practical Solutions class notes
    var xmlhttp = new XMLHttpRequest();
    var travelroute = document.getElementById('item_id').value
    var weather = document.getElementById('weather_id').value
    var traveltime = document.getElementById('traveltime').value
	var url =  "getResult?travelroute="+ travelroute + "&traveltime=" + encodeURIComponent(traveltime) + "&weather=" + weather;

                
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        
        //Parse the JSON data to a JavaScript variable
    
           var parsedObj = JSON.parse(xmlhttp.responseText);
        // This function is defined below and deals with the JSON data parsed from the file. 
           // alert(parsedObj);
            var average = parsedObj.average;
            document.getElementById("average").innerHTML = "<h3> Total expected time for route " + travelroute + ":<br>" + average + " minutes.</h3>";
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
    mapmarker();
    
}




function mapmarker() {
                   
//get daily JSON file code ref: Practical Solutions class notes
    var xmlhttp = new XMLHttpRequest();
    var travelroute = document.getElementById('item_id').value
   
	var url =  "getStops?travelroute="+ travelroute;
            
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        
        //Parse the JSON data to a JavaScript variable
    
           var parsedObj = JSON.parse(xmlhttp.responseText);
        // This function is defined below and deals with the JSON data parsed from the file. 
            alert(parsedObj);
            var average = parsedObj.average;
            document.getElementById("average").innerHTML = "<h3> Total expected time for route " + travelroute + ":<br>" + average + " minutes.</h3>";
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
}

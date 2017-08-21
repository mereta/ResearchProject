function load() {
                  
	// Get Weather
	
    var xmlhttpweather = new XMLHttpRequest();
      var urlweather = "http://api.openweathermap.org/data/2.5/forecast/daily?q=Dublin,IE&cnt=16&units=metric&APPID=6664879b703f55def17f2918f6e6c711";

                  
      xmlhttpweather.onreadystatechange = function () {
          if (xmlhttpweather.readyState == 4 && xmlhttpweather.status == 200) {
          
          //Parse the JSON data to a JavaScript variable
              var parsedObj = JSON.parse(xmlhttpweather.responseText);
          // This function is defined below and deals with the JSON data parsed from the file. 
              var ret = getWeather(parsedObj);
          }
      };

      xmlhttpweather.open("GET", urlweather, true);
      xmlhttpweather.send();
      
      
      
	//get daily JSON file code ref: Practical Solutions class notes
    var xmlhttp = new XMLHttpRequest();
    var travelroute = document.getElementById('item_id').value;
    var weather = ret
    var traveltime = document.getElementById('traveltime').value;

    var direction = document.getElementById('direction').value;
    var from_stop = document.getElementById('fromSelect').value;
    var to_stop = document.getElementById('toSelect').value;
    var to = document.getElementById("toSelect");
    var to_text = to.options[to.selectedIndex].text;
   
    

	var url =  "getResult?travelroute="+ travelroute + "&traveltime=" + encodeURIComponent(traveltime) + "&weather=" + weather + "&direction=" + direction + "&from=" + from_stop + "&to=" + to_stop;

                
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        
        //Parse the JSON data to a JavaScript variable
    
           var parsedObj = JSON.parse(xmlhttp.responseText);
        // This function is defined below and deals with the JSON data parsed from the file. 
           // alert(parsedObj);
            var depart = parsedObj.depart;
            var arr = parsedObj.arr;
            document.getElementById("average").innerHTML = "<h4><b> Expected Arrival Time at " + to_text + " is: " + arr + "</b></h4>";
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
            //alert(parsedObj);
           // var average = parsedObj.average;
           // document.getElementById("average").innerHTML = "<h3> Total expected time for route " + travelroute + ":<br>" + average + " minutes.</h3>";
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
    
}




function getWeather(obj) {
	

	var dt = new Date(); 
	var traveltime = document.getElementById('traveltime').value;
	var spacesplit = traveltime.split(" ");
	var hypsplit = spacesplit[0].split("-");
	
	var dt1 = new Date(hypsplit[0], hypsplit[1]-1, hypsplit[2]); 
	var one_day=1000*60*60*24;
	var result = Math.ceil((dt1.getTime()-dt.getTime())/(one_day));
	

    
    if(result < 15){
    	var dailyWeather = obj.list;
        var weatherid = dailyWeather[result].weather[0].id;
        if(weatherid > 799){
      	     	
        	ret  = "Dry";
        }
        else{
        	
        	ret = "Wet";
        }
   
        
       
    }
    else{
    	
    	ret = "Dry";
    }
   return ret;
}



function timeConverter(UNIX_timestamp){
	  var a = new Date(UNIX_timestamp * 1000);
	  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
	  var year = a.getFullYear();
	  var month = months[a.getMonth()];
	  var date = a.getDate();
	  var hour = a.getHours();
	  var min = a.getMinutes();
	  var sec = a.getSeconds();
	  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
	  return time;
	}


function getDate(timestamp) { // code ref = https://gist.github.com/kmaida/6045266
    var d = new Date(timestamp * 1000),	
	yyyy = d.getFullYear(),
	mm = ('0' + (d.getMonth() + 1)).slice(-2),	
	dd = ('0' + d.getDate()).slice(-2),			
	hh = d.getHours(),
	h = hh,
	min = ('0' + d.getMinutes()).slice(-2),		
	ampm = 'AM',
	time;


time = yyyy + "-" + mm + "-" + dd;
	
return time;
}
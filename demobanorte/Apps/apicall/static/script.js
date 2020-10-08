window.onload = function() { 
	var eliminocta =  document.getElementById('eliminocta_div');
	//console.log(eliminocta);
	if (typeof(eliminocta) != 'undefined' && eliminocta != null){
		var tarjeta = document.getElementsByClassName("tarjeta");
		var button  = document.getElementById('eliminocta_btn');
		//console.log("hidden: " + button.classList.contains("hidden"));
		if(tarjeta.length==0){
			//document.getElementById('eliminocta_btn').add
			if(!button.classList.contains("hidden")){
				button.classList.add("hidden");
			}
		}else{
			//document.getElementById('eliminocta_btn').add
			if(button.classList.contains("hidden")){
				button.classList.remove("hidden");
			}
		}
	}
}





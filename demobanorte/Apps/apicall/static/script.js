window.onload = function() { 
	var eliminocta =  document.getElementById('eliminocta_div');
	//console.log(eliminocta);
	if (typeof(eliminocta) != 'undefined' && eliminocta != null){
		var tarjeta = document.getElementsByClassName("tarjeta");
		var buttonCta  = document.getElementById('eliminocta_btn');
		var buttonCons  = document.getElementById('eliminoconsent_btn');
		//console.log("hidden: " + button.classList.contains("hidden"));
		if(tarjeta.length==0){
			//document.getElementById('eliminocta_btn').add
			if(!buttonCta.classList.contains("hidden")){
				buttonCta.classList.add("hidden");
			}
			if(!buttonCons.classList.contains("hidden")){
				buttonCons.classList.add("hidden");
			}
		}else{
			//document.getElementById('eliminocta_btn').add
			if(buttonCta.classList.contains("hidden")){
				buttonCta.classList.remove("hidden");
			}
			if(buttonCons.classList.contains("hidden")){
				buttonCons.classList.remove("hidden");
			}
		}
	}



	var menus = document.getElementsByClassName('main-menu');
	for(var i=0; i<menus.length; i++){
		if(String(menus[i].href).search(window.location.pathname)>=0){
			menus[i].classList.add('active');
		}
	}
	//console.log(window.location.pathname);




	/*
	var tarjeta = document.getElementsByClassName('tarjeta');
	console.log("Tarjeta: "+tarjeta);
	if(tarjeta.length>0){
		tarjeta.addEventListener('click', function(event){
			console.log("Tarjeta click");
		});
	}
	*/

}





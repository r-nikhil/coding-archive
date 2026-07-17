	function hideModal(){
		var mdlCover=document.querySelector("#mdl-cover");
		var modal=document.querySelector("#modal");

		mdlCover.style.height='0';
		mdlCover.style.backgroundColor='rgba(0,0,0,0)';
		modal.style.transform='translateY(-110%)';
		document.removeEventListener("click",callHideModal);
	};

	function callHideModal(event){
		if (event.target.id == 'mdl-cover' || event.target.id == 'mdl-hide') {
			hideModal();
		};
	};

	function showModal(){
		var mdlCover=document.querySelector("#mdl-cover");
		var modal=document.querySelector("#modal");

		mdlCover.style.height='100%';
		mdlCover.style.backgroundColor='rgba(0,0,0,0.75)';
		modal.style.transform='translateY(10%)';
		document.addEventListener("click",callHideModal);
	};

	var mdlShow=document.getElementsByClassName('mdl-show');

	for (i=0; i<mdlShow.length; i++){
		mdlShow[i].onclick=showModal;
	};



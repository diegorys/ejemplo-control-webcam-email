<?php

if(isset($_GET["command"]) && $_GET["command"] != ""){
	$command = $_GET["command"];
	mail ("xxxxx@gmail" , $command, "");
	echo $command;
}

?>

<form action="" method="get">

	<select name="command">
		<option value="">Selecciona comando</option>
		<option value="Comando derecha">Derecha</option>
		<option value="Comando izquierda">Izquierda</option>
		<option value="Comando centrar">Centro</option>
		<option value="Comando foto">Foto</option>
		<option value="Comando salir">Salir</option>
	</select>
	
	<input type="submit">

</form>
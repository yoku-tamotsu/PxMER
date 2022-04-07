<?php

$dbConfJson = file_get_contents('./db.conf.json');
$dbConf = json_decode($dbConfJson);

$conn = new mysqli($dbConf->address, $dbConf->username, $dbConf->password, $dbConf->database);

$tmp->color = 'green';
$tmp->msg = 'Database connected succesfully';
	
if($conn->connect_error){
	$tmp->color = 'red';
	$tmp->msg = 'Database connection fail: ' . $conn->connect_error;
}

?>

<!DOCKTYPE html>
<html>
	<head>
		<style>
			body {
				font-size: 1.5rem;
				text-align: center;
				text-transform: uppercase;
				background: black;
				margin: 3cm;
				color: <?php echo $tmp->color ?>
			}
		</style>
	</head>
	<body>
		<?php echo $tmp->msg ?>
	</body>
</html>

	

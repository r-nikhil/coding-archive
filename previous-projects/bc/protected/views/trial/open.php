<?php
/* @var $this TrialController */

$this->breadcrumbs=array(
	'Trial'=>array('/trial'),
	'Open',
);
?>
<h1><?php echo $this->id . '/' . $this->action->id; ?></h1>

<p>
	You may change the content of this page by modifying
	the file <tt><?php echo __FILE__; ?></tt>.
    <h3><?php echo date("D M j G:i:s T Y"); 
        $this->bolo();
        
        ?></h3>
</p>

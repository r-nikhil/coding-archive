<?php
/* @var $this ExpertController */
/* @var $model Expert */

$this->breadcrumbs=array(
	'Experts'=>array('index'),
	'Create',
);

$this->menu=array(
	array('label'=>'List Expert', 'url'=>array('index')),
	array('label'=>'Manage Expert', 'url'=>array('admin')),
);
?>

<h1>Create Expert</h1>

<?php $this->renderPartial('_form', array('model'=>$model)); ?>
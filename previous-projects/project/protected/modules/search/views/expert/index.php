<?php
/* @var $this ExpertController */
/* @var $dataProvider CActiveDataProvider */

$this->breadcrumbs=array(
	'Experts',
);

$this->menu=array(
	array('label'=>'Create Expert', 'url'=>array('create')),
	array('label'=>'Manage Expert', 'url'=>array('admin')),
);
?>

<h1>Experts</h1>

<?php $this->widget('zii.widgets.CListView', array(
	'dataProvider'=>$dataProvider,
	'itemView'=>'_view',
)); ?>

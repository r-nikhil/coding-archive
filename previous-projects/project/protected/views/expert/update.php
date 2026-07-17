<?php
/* @var $this ExpertController */
/* @var $model Expert */

$this->breadcrumbs=array(
	'Experts'=>array('index'),
	$model->name=>array('view','id'=>$model->id),
	'Update',
);

$this->menu=array(
	array('label'=>'List Expert', 'url'=>array('index')),
	array('label'=>'Create Expert', 'url'=>array('create')),
	array('label'=>'View Expert', 'url'=>array('view', 'id'=>$model->id)),
	array('label'=>'Manage Expert', 'url'=>array('admin')),
);
?>

<h1>Update Expert <?php echo $model->id; ?></h1>

<?php $this->renderPartial('_form', array('model'=>$model)); ?>
<?php
/* @var $this ExpertController */
/* @var $data Expert */
?>

<div class="view">

	<b><?php echo CHtml::encode($data->getAttributeLabel('id')); ?>:</b>
	<?php echo CHtml::link(CHtml::encode($data->id), array('view', 'id'=>$data->id)); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('name')); ?>:</b>
	<?php echo CHtml::encode($data->name); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('exp')); ?>:</b>
	<?php echo CHtml::encode($data->exp); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('cost')); ?>:</b>
	<?php echo CHtml::encode($data->cost); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('topic1')); ?>:</b>
	<?php echo CHtml::encode($data->topic1); ?>
	<br />

	<b><?php echo CHtml::encode($data->getAttributeLabel('topic2')); ?>:</b>
	<?php echo CHtml::encode($data->topic2); ?>
	<br />


</div>
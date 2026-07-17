<?php
/* @var $this ExpertController */
/* @var $model Expert */
/* @var $form CActiveForm */
?>

<div class="form">

<?php $form=$this->beginWidget('CActiveForm', array(
	'id'=>'expert-form',
	// Please note: When you enable ajax validation, make sure the corresponding
	// controller action is handling ajax validation correctly.
	// There is a call to performAjaxValidation() commented in generated controller code.
	// See class documentation of CActiveForm for details on this.
	'enableAjaxValidation'=>false,
)); ?>

	<p class="note">Fields with <span class="required">*</span> are required.</p>

	<?php echo $form->errorSummary($model); ?>

	<div class="row">
		<?php echo $form->labelEx($model,'name'); ?>
		<?php echo $form->textField($model,'name',array('size'=>60,'maxlength'=>255)); ?>
		<?php echo $form->error($model,'name'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'exp'); ?>
		<?php echo $form->textField($model,'exp'); ?>
		<?php echo $form->error($model,'exp'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'cost'); ?>
		<?php echo $form->textField($model,'cost'); ?>
		<?php echo $form->error($model,'cost'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'topic1'); ?>
		<?php echo $form->textField($model,'topic1',array('size'=>60,'maxlength'=>255)); ?>
		<?php echo $form->error($model,'topic1'); ?>
	</div>

	<div class="row">
		<?php echo $form->labelEx($model,'topic2'); ?>
		<?php echo $form->textField($model,'topic2',array('size'=>60,'maxlength'=>255)); ?>
		<?php echo $form->error($model,'topic2'); ?>
	</div>

	<div class="row buttons">
		<?php echo CHtml::submitButton($model->isNewRecord ? 'Create' : 'Save'); ?>
	</div>

<?php $this->endWidget(); ?>

</div><!-- form -->
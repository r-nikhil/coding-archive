<?php

/**
 * This is the model class for table "expert".
 *
 * The followings are the available columns in table 'expert':
 * @property integer $id
 * @property string $name
 * @property integer $exp
 * @property integer $cost
 * @property string $topic1
 * @property string $topic2
 */
class Expert extends CActiveRecord
{
	/**
	 * @return string the associated database table name
	 */
	public function tableName()
	{
		return 'expert';
	}

	/**
	 * @return array validation rules for model attributes.
	 */
	public function rules()
	{
		// NOTE: you should only define rules for those attributes that
		// will receive user inputs.
		return array(
			array('name, exp, cost, topic1, topic2', 'required'),
			array('exp, cost', 'numerical', 'integerOnly'=>true),
			array('name, topic1, topic2', 'length', 'max'=>255),
			// The following rule is used by search().
			// @todo Please remove those attributes that should not be searched.
			array('id, name, exp, cost, topic1, topic2', 'safe', 'on'=>'search'),
		);
	}

	/**
	 * @return array relational rules.
	 */
	public function relations()
	{
		// NOTE: you may need to adjust the relation name and the related
		// class name for the relations automatically generated below.
		return array(
		);
	}

	/**
	 * @return array customized attribute labels (name=>label)
	 */
	public function attributeLabels()
	{
		return array(
			'id' => 'ID',
			'name' => 'Name',
			'exp' => 'Exp',
			'cost' => 'Cost',
			'topic1' => 'Topic1',
			'topic2' => 'Topic2',
		);
	}

	/**
	 * Retrieves a list of models based on the current search/filter conditions.
	 *
	 * Typical usecase:
	 * - Initialize the model fields with values from filter form.
	 * - Execute this method to get CActiveDataProvider instance which will filter
	 * models according to data in model fields.
	 * - Pass data provider to CGridView, CListView or any similar widget.
	 *
	 * @return CActiveDataProvider the data provider that can return the models
	 * based on the search/filter conditions.
	 */
	public function search()
	{
		// @todo Please modify the following code to remove attributes that should not be searched.

		$criteria=new CDbCriteria;

		$criteria->compare('id',$this->id);
		$criteria->compare('name',$this->name,true);
		$criteria->compare('exp',$this->exp);
		$criteria->compare('cost',$this->cost);
		$criteria->compare('topic1',$this->topic1,true);
		$criteria->compare('topic2',$this->topic2,true);

		return new CActiveDataProvider($this, array(
			'criteria'=>$criteria,
		));
	}

	/**
	 * Returns the static model of the specified AR class.
	 * Please note that you should have this exact method in all your CActiveRecord descendants!
	 * @param string $className active record class name.
	 * @return Expert the static model class
	 */
	public static function model($className=__CLASS__)
	{
		return parent::model($className);
	}
}

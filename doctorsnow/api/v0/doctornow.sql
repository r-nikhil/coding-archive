-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2015 at 04:04 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

   use doctornowold ;




--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE IF NOT EXISTS `appointment` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `patient_id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL,
  `time` int(12) NOT NULL,
  `date` date NOT NULL,
  `details` text NOT NULL,
  `previous_med` text NOT NULL,
  `confirm` int(2) NOT NULL,
  `chat_url` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `category1`
--

CREATE TABLE IF NOT EXISTS `category1` (
  `id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `category2`
--

CREATE TABLE IF NOT EXISTS `category2` (
  `id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `category3`
--

CREATE TABLE IF NOT EXISTS `category3` (
  `id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `category4`
--

CREATE TABLE IF NOT EXISTS `category4` (
  `id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `docname_docid`
--

CREATE TABLE IF NOT EXISTS `docname_docid` (
  `id` varchar(20) NOT NULL,
  `patient_id` int(12) NOT NULL,
  `doctor_id` int(12) NOT NULL,
  `confirm` int(12) NOT NULL,
  `busy` int(12) NOT NULL,
  `appointment_id` int(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_clinic`
--

CREATE TABLE IF NOT EXISTS `doc_clinic` (
  `doc_id` int(12) NOT NULL,
  `clinic_name` varchar(255) NOT NULL,
  `clinic_address` text NOT NULL,
  `clinic_phone` int(12) NOT NULL,
  `pincode` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_education`
--

CREATE TABLE IF NOT EXISTS `doc_education` (
  `doc_id` int(12) NOT NULL,
  `doc_college` varchar(255) NOT NULL,
  `doc_degree` varchar(255) NOT NULL,
  `doc_year` int(12) NOT NULL,
  `doc_awards` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_experience`
--

CREATE TABLE IF NOT EXISTS `doc_experience` (
  `doc_id` int(12) NOT NULL,
  `doc_hospital` varchar(255) NOT NULL,
  `doc_exp` int(12) NOT NULL,
  `doc_details` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_login`
--

CREATE TABLE IF NOT EXISTS `doc_login` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_membership`
--

CREATE TABLE IF NOT EXISTS `doc_membership` (
  `doc_id` int(12) NOT NULL,
  `membership` varchar(255) NOT NULL,
  `details` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `doc_profile`
--

CREATE TABLE IF NOT EXISTS `doc_profile` (
  `doc_id` int(12) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `mobile` int(12) NOT NULL,
  `speciality` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `writeup` text NOT NULL,
  `full_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `login_patient`
--

CREATE TABLE IF NOT EXISTS `login_patient` (
  `id` int(12) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `profile_patient`
--

CREATE TABLE IF NOT EXISTS `profile_patient` (
  `id` int(12) NOT NULL,
  `name` varchar(255) NOT NULL,
  `age` int(12) NOT NULL,
  `allergies` varchar(255) NOT NULL,
  `blood` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

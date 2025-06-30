-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2025 at 01:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vms`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `emp_code` varchar(20) NOT NULL,
  `name` text DEFAULT NULL,
  `no_of_payable` text DEFAULT NULL,
  `no_of_days_present` text DEFAULT NULL,
  `nh_fh_ot_days` text DEFAULT NULL,
  `total_days_present` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`emp_code`, `name`, `no_of_payable`, `no_of_days_present`, `nh_fh_ot_days`, `total_days_present`) VALUES
('EMP1', 'R Agalya', '29', '25', '0', '25'),
('EMP2', 'S Kaviya', '29', '25', '0', '25'),
('EMP3', 'I Farhana', '29', '25', '0', '25'),
('EMP4', 'S Swetha', '29', '25', '0', '25'),
('EMP5', 'N Baskar', '29', '25', '0', '25');

-- --------------------------------------------------------

--
-- Table structure for table `bank_details`
--

CREATE TABLE `bank_details` (
  `emp_code` varchar(20) NOT NULL,
  `name` text DEFAULT NULL,
  `bank` text DEFAULT NULL,
  `acctno` text DEFAULT NULL,
  `ifscode` text DEFAULT NULL,
  `ntsalary` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank_details`
--

INSERT INTO `bank_details` (`emp_code`, `name`, `bank`, `acctno`, `ifscode`, `ntsalary`) VALUES
('EMP1', 'R Agalya', 'INDIAN', '78945625874', '89', '14470'),
('EMP2', 'K Sambath', 'RBL', '7412589654', '36', '14470'),
('EMP3', 'I Farhana', 'Axis', '7893653325', '45', '12862'),
('EMP4', 'S Swetha', 'HDFC', '7894561238', '87', '12058'),
('EMP5', 'N Baskar', 'RBL', '741258963', '85', '12862');

-- --------------------------------------------------------

--
-- Table structure for table `designation`
--

CREATE TABLE `designation` (
  `designation` varchar(20) NOT NULL,
  `basic` text DEFAULT NULL,
  `da` text DEFAULT NULL,
  `Conveyance` text DEFAULT NULL,
  `allowance` text DEFAULT NULL,
  `fixed_salary` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `designation`
--

INSERT INTO `designation` (`designation`, `basic`, `da`, `Conveyance`, `allowance`, `fixed_salary`) VALUES
('A', '9000', '5087', '960', '2953', '18000'),
('AA', '8000', '5087', '960', '1953', '16000'),
('B', '7500', '5087', '960', '1453', '15000'),
('BB', '7000', '5087', '460', '1453', '14000'),
('C', '6500', '5087', '960', '453', '13000'),
('D', '6000', '5087', '460', '453', '12000');

-- --------------------------------------------------------

--
-- Table structure for table `employeepayroll`
--

CREATE TABLE `employeepayroll` (
  `emp_code` varchar(20) NOT NULL,
  `Desgination` varchar(20) DEFAULT NULL,
  `name` text DEFAULT NULL,
  `age` text DEFAULT NULL,
  `gender` text DEFAULT NULL,
  `email` text DEFAULT NULL,
  `hired_location` text DEFAULT NULL,
  `doj` text DEFAULT NULL,
  `dob` text DEFAULT NULL,
  `experience` text DEFAULT NULL,
  `proof_id` text DEFAULT NULL,
  `contactno` text DEFAULT NULL,
  `status` text DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employeepayroll`
--

INSERT INTO `employeepayroll` (`emp_code`, `Desgination`, `name`, `age`, `gender`, `email`, `hired_location`, `doj`, `dob`, `experience`, `proof_id`, `contactno`, `status`, `address`) VALUES
('EMP1', 'A', 'R Agalya', '24', 'Female', 'aga@gmail.com', 'Mart', '2021-04-15', '1999-05-20', '2', '7412589630', '123456789', 'Primary', 'uwruifbae wuabvuiea eurvbeiuqbav\n\n'),
('EMP2', 'A', 'K Sambath', '35', 'Male', 'sam@gmail.com', 'Mart', '2010-02-18', '1988-07-20', '13', '1234567890', '9874563210', 'Primary', 'reinveoa nveia vineaivn \n'),
('EMP3', 'AA', 'I Farhana', '21', 'Female', 'far@gmail.com', 'Mart', '2023-02-15', '2002-07-18', '0', '4125874521', '45678991230', 'Secondary', 'sejbjsv enuvneai vheaihvi \n'),
('EMP4', 'B', 'S Swetha', '22', 'Female', 'swe@gmail.com', 'Mart', '2020-01-15', '2001-09-05', '4', '741258963', '4568977412', 'Primary', 'bsiu aevuhavbveaub vbauv bavububvaiub\n'),
('EMP5', 'AA', 'N Baskar', '20', 'Male', 'bas@gmail@.com', 'Mart', '2019-01-16', '2003-09-15', '5', '741025825', '1236547890', 'Secondary', 'bsjviae vbuaehv uhuivshzui \n');

-- --------------------------------------------------------

--
-- Table structure for table `salary_details`
--

CREATE TABLE `salary_details` (
  `emp_code` varchar(20) DEFAULT NULL,
  `name` text DEFAULT NULL,
  `designation` varchar(20) DEFAULT NULL,
  `fixed_salary` text DEFAULT NULL,
  `no_of_payable` text DEFAULT NULL,
  `no_of_days_present` text DEFAULT NULL,
  `nh_fh_ot_days` text DEFAULT NULL,
  `total_days_present` text DEFAULT NULL,
  `fbasic` text DEFAULT NULL,
  `fda` text DEFAULT NULL,
  `fallowance` text DEFAULT NULL,
  `fconveyance` text DEFAULT NULL,
  `fixed_salary_1` text DEFAULT NULL,
  `ebasic` text DEFAULT NULL,
  `eda` text DEFAULT NULL,
  `eallowance` text DEFAULT NULL,
  `econveyance` text DEFAULT NULL,
  `gross_salary` text DEFAULT NULL,
  `pf` text DEFAULT NULL,
  `esi` text DEFAULT NULL,
  `advance` text DEFAULT NULL,
  `total_deduction` text DEFAULT NULL,
  `other` text DEFAULT NULL,
  `ntsalary` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salary_details`
--

INSERT INTO `salary_details` (`emp_code`, `name`, `designation`, `fixed_salary`, `no_of_payable`, `no_of_days_present`, `nh_fh_ot_days`, `total_days_present`, `fbasic`, `fda`, `fallowance`, `fconveyance`, `fixed_salary_1`, `ebasic`, `eda`, `eallowance`, `econveyance`, `gross_salary`, `pf`, `esi`, `advance`, `total_deduction`, `other`, `ntsalary`) VALUES
('EMP1', 'R Agalya', 'A', '18000', '29', '25', '0', '25', '9000', '5087', '2953', '960', '18000', '7759', '4385', '2546', '828', '15517', '931', '116', '0', '983', '0', '14470'),
('EMP2', 'K Sambath', 'A', '18000', '29', '25', '0', '25', '9000', '5087', '2953', '960', '18000', '7759', '4385', '2546', '828', '15517', '931', '116', '0', '1047', '0', '14470'),
('EMP3', 'I Farhana', 'AA', '16000', '29', '25', '0', '25', '8000', '5087', '1953', '960', '16000', '6897', '4385', '1684', '828', '13793', '828', '103', '0', '931', '0', '12862'),
('EMP4', 'S Swetha', 'B', '15000', '29', '25', '0', '25', '7500', '5087', '1453', '960', '15000', '6466', '4385', '1253', '828', '12931', '776', '97', '0', '810', '0', '12058'),
('EMP5', 'N Baskar', 'AA', '16000', '29', '25', '0', '25', '8000', '5087', '1953', '960', '16000', '6897', '4385', '1684', '828', '13793', '828', '103', '0', '931', '0', '12862');

-- --------------------------------------------------------

--
-- Table structure for table `summaryatten`
--

CREATE TABLE `summaryatten` (
  `emp_code` varchar(20) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `absent` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `summaryatten`
--

INSERT INTO `summaryatten` (`emp_code`, `name`, `absent`) VALUES
('EMP1', 'R Agalya', '4'),
('EMP2', 'S Kaviya', '4'),
('EMP3', 'I Farhana', '4'),
('EMP4', 'S Swetha', '4'),
('EMP5', 'N Baskar', '4');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`emp_code`);

--
-- Indexes for table `bank_details`
--
ALTER TABLE `bank_details`
  ADD PRIMARY KEY (`emp_code`);

--
-- Indexes for table `designation`
--
ALTER TABLE `designation`
  ADD PRIMARY KEY (`designation`);

--
-- Indexes for table `employeepayroll`
--
ALTER TABLE `employeepayroll`
  ADD PRIMARY KEY (`emp_code`);

--
-- Indexes for table `summaryatten`
--
ALTER TABLE `summaryatten`
  ADD PRIMARY KEY (`emp_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

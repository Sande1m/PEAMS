CREATE DATABASE peams;
USE peams;

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `username` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `email`, `password`, `username`) VALUES
(1, 'leah form', 'leah@gmail.com', '$5$rounds=535000$4ZSyZlVGcpJZfrQ.$eyAUxj181QMkfSPB5LPCcmBeLW.xVDc44FSDxtk1D/5', 'coldest'),
(2, 'David Forms', 'forms@gmail.com', '$5$rounds=535000$c00iM6rLA5gFlAFZ$/rv0.f.Yasvw3PQfw/nvGd301VNbLCh68zoxSeZyhw4', 'hot23');

-- --------------------------------------------------------

--
-- Table structure for table `alert`
--

CREATE TABLE `alert` (
  `alert_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `inventory_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `brand` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `quantity`, `brand`, `category`, `expiry_date`) VALUES
('1120774d-79c6-458f-8939-c3d9778a20d1', 1, 'fruitville', 'beverage', '2024-07-19'),
('1e42a81e-f8bf-40af-86f1-e94d92a4ca6f', 1, 'supaloaf', 'bakery', '2024-07-13'),
('47c86a49-32fd-4e5a-a1de-0be8d4fa74dc', 1, 'brookside', 'dairy', '2025-08-01'),
('7625a801-06d1-4d7c-a6e1-fccd77184e1e', 2, 'rockburn', 'bakery', '2024-07-12'),
('80a15d36-bab1-432e-8ae4-9883e946fe3f', 3, 'blueband', 'spread', '2024-07-11'),
('fab11273-3860-4dd5-897c-b0c3662a81ed', 1, 'Daylight Yoghurt', 'Dairy', '2024-08-01');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` varchar(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `inventory_id` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `description`, `price`, `inventory_id`) VALUES
('2f731edd-e2', 'blueband', '500g', '300.00', '80a15d36-bab1-432e-8ae4-9883e946fe3f'),
('31ee258a-78', 'brookside', '500 ml', '60.00', '47c86a49-32fd-4e5a-a1de-0be8d4fa74dc'),
('5f90c117-c8', 'rockburn', '100g', '60.00', '7625a801-06d1-4d7c-a6e1-fccd77184e1e');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `alert`
--
ALTER TABLE `alert`
  ADD PRIMARY KEY (`alert_id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `inventory_id` (`inventory_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `fk_product_inventory` (`inventory_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `alert`
--
ALTER TABLE `alert`
  MODIFY `alert_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;


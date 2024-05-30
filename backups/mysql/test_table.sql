CREATE TABLE `test_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `test_table` (id, name, created_at) VALUES ('1', 'Alice', '2024-05-30 09:25:23');
INSERT INTO `test_table` (id, name, created_at) VALUES ('2', 'Bob', '2024-05-30 09:25:23');
INSERT INTO `test_table` (id, name, created_at) VALUES ('3', 'Charlie', '2024-05-30 09:25:23');

CREATE TABLE `app_1_interest` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE = InnoDB AUTO_INCREMENT = 8 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `app_1_like` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `timestamp` datetime(6) NOT NULL,
    `liked_id` int NOT NULL,
    `liker_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `app_1_like_liker_id_liked_id_bd2e5141_uniq` (`liker_id`, `liked_id`),
    KEY `app_1_like_liked_id_38574c1f_fk_auth_user_id` (`liked_id`),
    CONSTRAINT `app_1_like_liked_id_38574c1f_fk_auth_user_id` FOREIGN KEY (`liked_id`) REFERENCES `auth_user` (`id`),
    CONSTRAINT `app_1_like_liker_id_7ed1de8d_fk_auth_user_id` FOREIGN KEY (`liker_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `app_1_profile` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `bio` longtext NOT NULL,
    `localisation` varchar(70) NOT NULL,
    `photo_de_profil` varchar(100) DEFAULT NULL,
    `utilisateur_id` int NOT NULL,
    `sexe` varchar(8) DEFAULT NULL,
    `age` int DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `utilisateur_id` (`utilisateur_id`),
    CONSTRAINT `app_1_profile_utilisateur_id_f80ad15a_fk_auth_user_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `app_1_profile_interet` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `profile_id` bigint NOT NULL,
    `interest_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `app_1_profile_interet_profile_id_interest_id_db565b8d_uniq` (`profile_id`, `interest_id`),
    KEY `app_1_profile_interet_interest_id_3a0b87bb_fk_app_1_interest_id` (`interest_id`),
    CONSTRAINT `app_1_profile_interet_interest_id_3a0b87bb_fk_app_1_interest_id` FOREIGN KEY (`interest_id`) REFERENCES `app_1_interest` (`id`),
    CONSTRAINT `app_1_profile_interet_profile_id_ffa3867f_fk_app_1_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `app_1_profile` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_group` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(150) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_group_permissions` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `group_id` int NOT NULL,
    `permission_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`, `permission_id`),
    KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
    CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
    CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_permission` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `content_type_id` int NOT NULL,
    `codename` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`, `codename`),
    CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 45 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_user` (
    `id` int NOT NULL AUTO_INCREMENT,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) DEFAULT NULL,
    `is_superuser` tinyint(1) NOT NULL,
    `username` varchar(150) NOT NULL,
    `first_name` varchar(150) NOT NULL,
    `last_name` varchar(150) NOT NULL,
    `email` varchar(254) NOT NULL,
    `is_staff` tinyint(1) NOT NULL,
    `is_active` tinyint(1) NOT NULL,
    `date_joined` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `username` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_user_groups` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `group_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`, `group_id`),
    KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
    CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
    CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `auth_user_user_permissions` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `permission_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`, `permission_id`),
    KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
    CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
    CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `chatapp_messages` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `date` datetime(6) NOT NULL,
    `content` longtext NOT NULL,
    `sender_id` int NOT NULL,
    `receiver_id` int NOT NULL,
    `chatRoom_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `chatapp_messages_sender_id_c0e61ba5_fk_auth_user_id` (`sender_id`),
    KEY `chatapp_messages_chatRoom_id_ddcf0fa7_fk_chatapp_room_id` (`chatRoom_id`),
    KEY `chatapp_messages_receiver_id_0bd778ef_fk_auth_user_id` (`receiver_id`),
    CONSTRAINT `chatapp_messages_chatRoom_id_ddcf0fa7_fk_chatapp_room_id` FOREIGN KEY (`chatRoom_id`) REFERENCES `chatapp_room` (`id`),
    CONSTRAINT `chatapp_messages_receiver_id_0bd778ef_fk_auth_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `auth_user` (`id`),
    CONSTRAINT `chatapp_messages_sender_id_c0e61ba5_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `chatapp_room` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `chatapp_room_friends` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `room_id` bigint NOT NULL,
    `user_id` int NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `chatapp_room_friends_room_id_user_id_16caa156_uniq` (`room_id`, `user_id`),
    KEY `chatapp_room_friends_user_id_44a31984_fk_auth_user_id` (`user_id`),
    CONSTRAINT `chatapp_room_friends_room_id_156bde5f_fk_chatapp_room_id` FOREIGN KEY (`room_id`) REFERENCES `chatapp_room` (`id`),
    CONSTRAINT `chatapp_room_friends_user_id_44a31984_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `django_admin_log` (
    `id` int NOT NULL AUTO_INCREMENT,
    `action_time` datetime(6) NOT NULL,
    `object_id` longtext,
    `object_repr` varchar(200) NOT NULL,
    `action_flag` smallint unsigned NOT NULL,
    `change_message` longtext NOT NULL,
    `content_type_id` int DEFAULT NULL,
    `user_id` int NOT NULL,
    PRIMARY KEY (`id`),
    KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
    KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
    CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
    CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
    CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `django_content_type` (
    `id` int NOT NULL AUTO_INCREMENT,
    `app_label` varchar(100) NOT NULL,
    `model` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`, `model`)
) ENGINE = InnoDB AUTO_INCREMENT = 12 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `django_migrations` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `app` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `applied` datetime(6) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 37 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `django_session` (
    `session_key` varchar(40) NOT NULL,
    `session_data` longtext NOT NULL,
    `expire_date` datetime(6) NOT NULL,
    PRIMARY KEY (`session_key`),
    KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci
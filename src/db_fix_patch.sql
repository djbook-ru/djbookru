BEGIN;

DROP TABLE `admin_tools_dashboard_preferences`;
DROP TABLE `admin_tools_menu_bookmark`;
DROP TABLE `adzone_adbase`;
DROP TABLE `adzone_adcategory`;
DROP TABLE `adzone_adclick`;
DROP TABLE `adzone_adimpression`;
DROP TABLE `adzone_advertiser`;
DROP TABLE `adzone_adzone`;
DROP TABLE `adzone_bannerad`;
DROP TABLE `adzone_textad`;
DROP TABLE `auth_message`;
DROP TABLE `code_review_comment`;
DROP TABLE `code_review_file`;
DROP TABLE `code_review_snipet_rated_by`;
DROP TABLE `code_review_snipet`;
DROP TABLE `google_analytics_analytics`;
DROP TABLE `indexer_index`;
DROP TABLE `poll_choice`;
DROP TABLE `poll_item`;
DROP TABLE `poll_poll_votes`;
DROP TABLE `poll_poll`;
DROP TABLE `poll_queue`;
DROP TABLE `poll_vote`;
DROP TABLE `robots_rule_allowed`;
DROP TABLE `robots_rule_disallowed`;
DROP TABLE `robots_rule_sites`;
DROP TABLE `robots_rule`;
DROP TABLE `robots_url`;
DROP TABLE `sentry_filtervalue`;
DROP TABLE `sentry_groupedmessage`;
DROP TABLE `sentry_message`;
DROP TABLE `south_migrationhistory`;

ALTER TABLE `accounts_announcement` MODIFY `is_active` tinyint(1) NOT NULL;
ALTER TABLE `chunks_chunk` DROP COLUMN `help`;
ALTER TABLE `django_session` ADD INDEX `django_session_de54fa62` (`expire_date`);
ALTER TABLE `examples_category` ADD INDEX `examples_category_70a17ffa` (`order`);
ALTER TABLE `links_archive` ADD INDEX `links_archive_70a17ffa` (`order`);
ALTER TABLE `links_sourcecode` ADD INDEX `links_sourcecode_70a17ffa` (`order`);
ALTER TABLE `links_usefullink` ADD INDEX `links_usefullink_70a17ffa` (`order`);
ALTER TABLE `oembed_storedprovider` MODIFY `active` tinyint(1) NOT NULL;
ALTER TABLE `oembed_storedprovider` MODIFY `provides` tinyint(1) NOT NULL;

# Fix social-auth tables
CREATE TABLE `social_auth_code` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `email` varchar(75) NOT NULL, `code` varchar(32) NOT NULL, `verified` bool NOT NULL);
ALTER TABLE `social_auth_code` ADD CONSTRAINT `social_auth_code_email_75f27066d057e3b6_uniq` UNIQUE (`email`, `code`);
CREATE INDEX `social_auth_code_c1336794` ON `social_auth_code` (`code`);

ALTER TABLE `social_auth_nonce` MODIFY `salt` varchar(65) NOT NULL;
DROP INDEX `social_auth_nonce1` ON `social_auth_nonce`;
DROP INDEX `social_auth_nonce2` ON `social_auth_nonce`;

DROP INDEX `social_auth_association1` ON `social_auth_association`;
DROP INDEX `social_auth_association2` ON `social_auth_association`;
UPDATE `social_auth_usersocialauth` SET provider="yandex-openid" WHERE provider="yandex";

DELETE FROM `django_content_type` WHERE `app_label`="adzone";
DELETE FROM `django_content_type` WHERE `app_label`="auth" AND `model`="message";
DELETE FROM `django_content_type` WHERE `app_label`="claims" AND `model`="claimstatus";
DELETE FROM `django_content_type` WHERE `app_label`="claims" AND `model`="text";
DELETE FROM `django_content_type` WHERE `app_label`="dashboard" AND `model`="dashboardpreferences";
DELETE FROM `django_content_type` WHERE `app_label`="dinette";
DELETE FROM `django_content_type` WHERE `app_label`="djangobb_forum";
DELETE FROM `django_content_type` WHERE `app_label`="google_analytics";
DELETE FROM `django_content_type` WHERE `app_label`="indexer" AND `model`="index";
DELETE FROM `django_content_type` WHERE `app_label`="menu" AND `model`="bookmark";
DELETE FROM `django_content_type` WHERE `app_label`="nezabudka";
DELETE FROM `django_content_type` WHERE `app_label`="openid_consumer";
DELETE FROM `django_content_type` WHERE `app_label`="poll";
DELETE FROM `django_content_type` WHERE `app_label`="robots";
DELETE FROM `django_content_type` WHERE `app_label`="sentry";
DELETE FROM `django_content_type` WHERE `app_label`="socialauth";
DELETE FROM `django_content_type` WHERE `app_label`="south";
DELETE FROM `django_content_type` WHERE `app_label`="code_review";

DELETE ap FROM `auth_permission` ap LEFT JOIN `django_content_type` ct ON (ap.`content_type_id`=ct.id) WHERE ct.`name` IS NULL;

COMMIT;

"""
pip install colorclass
pip install terminaltables
"""
import difflib
import hashlib
import os
import sqlparse
import subprocess
import warnings

from colorclass import Color
from optparse import make_option
from pprint import pprint
from terminaltables import SingleTable

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import DatabaseError

from src.settings import rel_project


DJANGO_DB_ALIAS = 'django'
BEFORE_DUMP_PATH = '/tmp/dump/before'
AFTER_DUMP_PATH = '/tmp/dump/after'
PATCH_PATH = 'db_fix_patch.sql'
REMOVE_TABLES = (
    'admin_tools_dashboard_preferences',
    'admin_tools_menu_bookmark',
    'adzone_adbase',
    'adzone_adcategory',
    'adzone_adclick',
    'adzone_adimpression',
    'adzone_advertiser',
    'adzone_adzone',
    'adzone_bannerad',
    'adzone_textad',
    'auth_message',
    'google_analytics_analytics',
    'indexer_index',
    'poll_choice',
    'poll_item',
    'poll_poll',
    'poll_poll_votes',
    'poll_queue',
    'poll_vote',
    'robots_rule',
    'robots_rule_allowed',
    'robots_rule_disallowed',
    'robots_rule_sites',
    'robots_url',
    'sentry_filtervalue',
    'sentry_groupedmessage',
    'sentry_message',
    'south_migrationhistory',
)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dump', action='store', dest='dump',
                    default='../20141029.sql', help='Path to DB dump.'),
    )

    requires_system_checks = False

    def handle(self, **options):
        prod = DBSchema(connections[DEFAULT_DB_ALIAS], DEFAULT_DB_ALIAS, self.style)
        django = DBSchema(connections[DJANGO_DB_ALIAS], DJANGO_DB_ALIAS, self.style)

        if options.get('dump'):
            print(self.style.MIGRATE_HEADING(u'Load dump to default database...'))
            prod.load_dump(rel_project(options.get('dump')))

        print(self.style.MIGRATE_HEADING(u'Dump data before final migrations...'))
        prod.make_dump(BEFORE_DUMP_PATH)

        print(self.style.MIGRATE_HEADING(u'Apply patch...'))
        prod.apply_sql(rel_project(PATCH_PATH))

        print(self.style.MIGRATE_HEADING(u'Run final migrations...'))
        call_command('migrate', interactive=False)

        print(self.style.MIGRATE_HEADING(u'Reset django database...'))
        django.reset_db()

        print(self.style.MIGRATE_HEADING(u'Check tables...'))
        tables = self.tables_diff(prod, django)

        print(self.style.MIGRATE_HEADING(u'Check tables\' structure...'))
        for table_name in tables:
            self.table_diff(table_name, prod, django)

        print(self.style.MIGRATE_HEADING(u'Check indexes...'))
        for table_name in tables:
            self.index_diff(table_name, prod, django)

        print(self.style.MIGRATE_HEADING(u'Check constraints...'))
        for table_name in tables:
            self.constraints_diff(table_name, prod, django)

        print(self.style.MIGRATE_HEADING(u'Check triggers...'))
        self.triggers_diff(prod, django)

        print(self.style.MIGRATE_HEADING(u'Check content types...'))
        self.content_types_diff(prod, django)

        print(self.style.MIGRATE_HEADING(u'Check permissions...'))
        self.permissions_diff(prod, django)

        print(self.style.MIGRATE_HEADING(u'Check migrations...'))
        self.migrations_diff(prod, django)

        print(self.style.MIGRATE_HEADING(u'Dump data after patch...'))
        prod.make_dump(AFTER_DUMP_PATH)

        print(self.style.MIGRATE_HEADING(u'Check data...'))
        self.data_diff(BEFORE_DUMP_PATH, AFTER_DUMP_PATH)

    def tables_diff(self, db1, db2):
        db1_tables = set(db1.get_table_list())
        db2_tables = set(db2.get_table_list())

        assert not db1_tables.intersection(set(REMOVE_TABLES))
        assert not db2_tables.intersection(set(REMOVE_TABLES))

        db1_diff = db1_tables.difference(db2_tables)
        db2_diff = db2_tables.difference(db1_tables)

        def print_diff(db_diff, db, style):
            if db_diff:
                print(style.ERROR('These tables exist only in %s:' % db.db_name))
                for table_name in db_diff:
                    print(style.HTTP_INFO('%s rows: %s DROP TABLE `%s`;' % (table_name, db.rows_count(table_name), table_name)))
                print('')

        print_diff(db1_diff, db1, self.style)

        return db1_tables.intersection(db2_tables)

    def table_diff(self, table_name, db1, db2):
        columns1 = db1.get_columns(table_name)
        columns2 = db2.get_columns(table_name)

        diff = list(difflib.unified_diff(columns1, columns2))
        if diff:
            print(self.style.ERROR(table_name))
            print(db1.get_create_table(table_name))
            print('')
            print(db2.get_create_table(table_name))
            table = DiffTable(
                ['', 'Field', 'Type', 'Null', 'Key', 'Default', 'Extra'],
                diff, db1.alias, db2.alias)

            print(table.table)

    def index_diff(self, table_name, db1, db2):
        indexes1 = db1.get_indexes(table_name)
        indexes2 = db2.get_indexes(table_name)

        diff = list(difflib.unified_diff(indexes1, indexes2))

        if diff:
            print(self.style.ERROR(table_name))
            print(db1.get_create_table(table_name))
            print('')
            print(db2.get_create_table(table_name))
            table = DiffTable(
                ['', 'Field', 'Primary', 'Unique'],
                diff, db1.alias, db2.alias)
            print(table.table)

    def constraints_diff(self, table_name, db1, db2):
        constraints1 = db1.get_constraints(table_name)
        constraints2 = db2.get_constraints(table_name)

        diff = list(difflib.unified_diff(constraints1, constraints2))

        if diff:
            print(self.style.ERROR(table_name))
            print(db1.get_create_table(table_name))
            print('')
            print(db2.get_create_table(table_name))
            table = DiffTable(
                ['', 'Columns', 'FK', 'PK', 'Unique'],
                diff, db1.alias, db2.alias)
            print(table.table)

    def data_diff(self, before_path, after_path):
        for file_path in os.listdir(before_path):
            if not file_path.endswith('.txt'):
                continue

            file_before = open(os.path.join(before_path, file_path))
            file_after = open(os.path.join(after_path, file_path))

            hash_before = hashlib.sha256(file_before.read()).hexdigest()
            hash_after = hashlib.sha256(file_after.read()).hexdigest()

            if hash_before != hash_after:
                print(self.style.ERROR('Broken data after patch: %s' % file_path.split('.')[0]))

    def triggers_diff(self, db1, db2):
        triggers1 = db1.get_triggers()
        triggers2 = db2.get_triggers()

        diff = list(difflib.unified_diff(triggers1, triggers2))

        if diff:
            table = DiffTable(
                ['', 'Name', 'Table', 'Event', 'Timing', 'MD5(Statment)'],
                diff, db1.alias, db2.alias)
            print(table.table)

    def content_types_diff(self, db1, db2):
        content_types1 = db1.get_content_types()
        content_types2 = db2.get_content_types()

        diff = list(difflib.unified_diff(content_types1, content_types2))

        if diff:
            table = DiffTable(
                ['', 'Name', 'App label', 'Model'],
                diff, db1.alias, db2.alias)
            print(table.table)

    def permissions_diff(self, db1, db2):
        permissions1 = db1.get_permissions()
        permissions2 = db2.get_permissions()

        diff = list(difflib.unified_diff(permissions1, permissions2))

        if diff:
            table = DiffTable(
                ['', 'Name', 'Code', 'CT name', 'App label', 'Model'],
                diff, db1.alias, db2.alias)
            print(table.table)

    def migrations_diff(self, db1, db2):
        migrations1 = db1.get_migrations()
        migrations2 = db2.get_migrations()

        diff = list(difflib.unified_diff(migrations1, migrations2))

        if diff:
            table = DiffTable(
                ['', 'App', 'Name'],
                diff, db1.alias, db2.alias)
            print(table.table)


def format_output(rows):
    output = []
    for row in rows:
        row = [unicode(item) for item in row]
        output.append(u'|'.join(row))
    output.sort()
    return output


class DBSchema(object):

    def __init__(self, connection, alias, style):
        self.style = style
        self.connection = connection
        self.introspection = connection.introspection
        self.db_name = connection.settings_dict['NAME']
        self.alias = alias
        self.conf = connection.settings_dict

    def get_table_list(self):
        return self.introspection.get_table_list(self.connection.cursor())

    def get_table_description(self, table_name):
        return self.introspection.get_table_description(self.connection.cursor(), table_name)

    def get_create_table(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute('SHOW CREATE TABLE %s' % table_name)
        output = cursor.fetchone()[1]
        cursor.close()
        return output

    def get_columns(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute('SHOW COLUMNS FROM %s' % table_name)
        output = format_output(cursor.fetchall())
        cursor.close()
        return output

    def get_indexes(self, table_name):
        indexes = self.introspection.get_indexes(self.connection.cursor(), table_name)
        output = []
        for key, params in indexes.items():
            row = [key, unicode(params['primary_key']), unicode(params['unique'])]
            output.append(u'|'.join(row))
        output.sort()
        return output

    def get_constraints(self, table_name):
        constraints = self.introspection.get_constraints(self.connection.cursor(), table_name)
        output = []
        for _, params in constraints.items():
            # Skip indexes
            if params['index'] and params['foreign_key'] is None and \
                    not params['primary_key'] and not params['unique']:
                continue

            row = [
                params['columns'],
                params['foreign_key'],
                params['primary_key'],
                params['unique']
            ]
            row = [unicode(item) for item in row]
            output.append(u'|'.join(row))
        output.sort()
        return output

    def get_triggers(self):
        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT TRIGGER_NAME, EVENT_OBJECT_TABLE, EVENT_MANIPULATION, '
            'ACTION_TIMING, MD5(LOWER(REPLACE(REPLACE(ACTION_STATEMENT, "\n", ""), " ", ""))) '
            'FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA=%s', [self.db_name])
        output = format_output(cursor.fetchall())
        cursor.close()
        return output

    def reset_db(self):
        assert self.alias != DEFAULT_DB_ALIAS

        cursor = self.connection.cursor()

        cursor.execute('DROP DATABASE %s' % self.db_name)
        cursor.execute('CREATE DATABASE %s' % self.db_name)
        cursor.execute('USE %s' % self.db_name)
        cursor.close()

        call_command('migrate', database=self.alias)

    def load_dump(self, dump_path):
        cursor = self.connection.cursor()

        cursor.execute('DROP DATABASE %s' % self.db_name)
        cursor.execute('CREATE DATABASE %s' % self.db_name)
        cursor.execute('USE %s' % self.db_name)
        cursor.close()

        cmd = 'mysql -h%s -u%s -p%s %s < %s' % (
            self.conf['HOST'], self.conf['USER'],
            self.conf['PASSWORD'], self.conf['NAME'], dump_path)

        subprocess.call(cmd, shell=True)

    def apply_sql(self, path):
        cursor = self.connection.cursor()

        with open(path) as f:
            for statement in sqlparse.split(f.read()):
                statement = statement.strip()

                if not statement:
                    continue

                with warnings.catch_warnings(record=True) as query_warnings:
                    try:
                        cursor.execute(statement.replace('%', '%%'))
                    except DatabaseError:
                        print(self.style.ERROR('Error during query execution:'))
                        print(statement)
                        raise
                    if query_warnings:
                        print(self.style.ERROR('Warnings during query execution:'))
                        print(self.style.WARNING(query_warnings[0].message))
                        print(statement)
                        print('')

    def rows_count(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM %s' % table_name)
        output = cursor.fetchone()[0]
        cursor.close()
        return output

    def make_dump(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            # markdirs may ignore mask on some OS
            subprocess.call('chmod -R 0777 %s' % dir_path, shell=True)

        cmd = 'mysqldump --no-create-info --tab=/%s --fields-terminated-by=";" -h%s -u%s -p%s %s'
        cmd = cmd % (
            dir_path, self.conf['HOST'], self.conf['USER'],
            self.conf['PASSWORD'], self.conf['NAME'])

        subprocess.call(cmd, shell=True)

    def get_content_types(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT name, app_label, model FROM django_content_type')
        output = format_output(cursor.fetchall())
        cursor.close()
        return output

    def get_permissions(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT ap.name, ap.codename, ct.name, ct.app_label, ct.model FROM '
                       'auth_permission ap JOIN django_content_type ct ON '
                       '(ap.content_type_id=ct.id)')
        output = format_output(cursor.fetchall())
        cursor.close()
        return output

    def get_migrations(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT app, name FROM django_migrations')
        output = format_output(cursor.fetchall())
        cursor.close()
        return output


class DiffTable(SingleTable):

    def __init__(self, headline, diff, alias1, alias2):
        table_data = [headline]
        diff = diff[3:]
        for row in diff:
            if row[0] == '-':
                # terminaltables does not like Django's color
                delta = Color('{autogreen}%s{/autogreen}' % alias1)
            elif row[0] == '+':
                delta = Color('{autoyellow}%s{/autoyellow}' % alias2)
            else:
                delta = ''
            row = row[1:]
            table_data.append([delta] + row.split('|'))

        super(DiffTable, self).__init__(table_data)

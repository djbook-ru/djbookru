"""
pip install colorclass
pip install terminaltables
"""
import difflib
import hashlib
import os
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


DJANGO_DB_ALIAS = 'django'
BEFORE_DUMP_PATH = '/tmp/dump/before'
AFTER_DUMP_PATH = '/tmp/dump/after'


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dump', action='store', dest='../dump',
                    default='dump.sql', help='Path to DB dump.'),
    )

    requires_system_checks = False

    def handle(self, **options):
        prod = DBSchema(connections[DEFAULT_DB_ALIAS], DEFAULT_DB_ALIAS, self.style)
        django = DBSchema(connections[DJANGO_DB_ALIAS], DJANGO_DB_ALIAS, self.style)

        if options.get('dump'):
            print(self.style.MIGRATE_HEADING(u'Load dump to default database...'))
            prod.load_dump(settings.rel_project(options.get('dump')))

        print(self.style.MIGRATE_HEADING(u'Dump data before final migrations...'))
        prod.make_dump(BEFORE_DUMP_PATH)

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
            statements = parse_mysql_script(f.read())

            for statement in statements:
                statement = statement.strip()
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

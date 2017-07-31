from orator.migrations import Migration


class RemoveSizeClomunFromApp(Migration):

    def up(self):
        with self.schema.table('apps') as table:
            table.drop_column('size')

    def down(self):
        with self.schema.table('apps') as table:
            table.string('size')

from orator.migrations import Migration


class AddPlayStoreHtmlColumnToApps(Migration):

    def up(self):
        with self.schema.table('apps') as table:
            table.long_text('play_store_html')

    def down(self):
        with self.schema.table('apps') as table:
            table.drop_column('play_store_html')

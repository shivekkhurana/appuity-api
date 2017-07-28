from orator.migrations import Migration


class CreateAppsTable(Migration):

    def up(self):
        with self.schema.create('apps') as table:
            table.increments('id')
            table.string('name')
            table.string('category')
            table.string('total_reviews')
            table.long_text('icon_url')
            table.string('avg_rating')
            table.string('last_updated')
            table.string('current_version')
            table.string('size')
            table.string('no_of_downloads')
            table.string('offered_by')
            table.json('developer').default({})
            table.string('play_store_id').unique()
            table.timestamps()


    def down(self):
        self.schema.drop('apps')
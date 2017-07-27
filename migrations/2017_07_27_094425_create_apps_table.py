from orator.migrations import Migration


class CreateAppsTable(Migration):

    def up(self):
        with self.schema.create('apps') as table:
            table.increments('id')
            table.string('app_id').unique()
            table.string('name')
            table.string('category')
            table.integer('total_reviews')
            table.float('avg_rating')
            table.string('last_updated')
            table.string('current_version')
            table.string('size')
            table.string('no_of_downloads')
            table.string('offered_by')
            table.string('developer')


    def down(self):
        self.schema.drop('apps')
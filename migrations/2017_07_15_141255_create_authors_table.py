from orator.migrations import Migration

class CreateAuthorsTable(Migration):
    def up(self):
        with self.schema.create('authors') as table:
            table.increments('id')
            table.string('name')
            table.long_text('avatar_url')
            table.timestamps()

    def down(self):
        self.schema.drop('authors')

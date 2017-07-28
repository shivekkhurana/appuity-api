from orator.migrations import Migration


class CreateReviewsTable(Migration):

    def up(self):
        with self.schema.create('reviews') as table:
            table.increments('id')
            table.integer('app_id')
            table.integer('author_id')
            table.integer('rating') #option pool (1-5 stars)
            table.long_text('review_text')
            table.timestamps()

    def down(self):
        self.schema.drop('reviews')


from orator.migrations import Migration


class CreateReviewsTable(Migration):

    def up(self):
        with self.schema.create('reviews') as table:
            table.increments('id')
            table.string('app_id')
            table.long_text('author_url')
            table.integer('rating') #option pool (1-5 stars)
            table.long_text('review_text')
            
            table.foreign('app_id').references('app_id').on('apps')
            table.foreign('author_url').references('avatar_url').on('authors')

    def down(self):
        self.schema.drop('reviews')


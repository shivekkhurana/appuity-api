from orator.migrations import Migration


class ChangeReviewCloumn(Migration):

    def up(self):
        with self.schema.table('apps') as table:
            table.rename_column('total_reviews','total_ratings')

    def down(self):
        with self.schema.table('apps') as table:
            table.rename_column('total_ratings','total_reviews')

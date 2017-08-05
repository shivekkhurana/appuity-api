from orator.migrations import Migration


class AddColumnsToReview(Migration):

    def up(self):
        with self.schema.table('reviews') as table:
            table.string('date')
            table.float('score')
            table.float('magnitude')

    def down(self):
        with self.schema.table('reviews') as table:
            table.drop_cloumn('date','score','magnitude')

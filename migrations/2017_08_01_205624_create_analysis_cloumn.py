from orator.migrations import Migration


class CreateAnalysisCloumn(Migration):

    def up(self):
        with self.schema.table('reviews') as table:
            table.drop_column('score')
            table.drop_column('magnitude')
            table.json('analysis')

    def down(self):
        with self.schema.table('reviews') as table:
            table.drop_column('analysis')
            table.float('magnitude')
            table.float('score')

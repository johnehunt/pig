class Pipeline:

    def __init__(self, start, steps, end):
        self.start = start
        self.steps = steps
        self.end = end

    def __repr__(self):
        return f'Pipeline(start: {self.start}, steps {self.steps}, end: {self.end})'

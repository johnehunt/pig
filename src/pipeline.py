
class Operation:
    def __init__(self, action, args=None):
        self.action = action
        self.args = args

    def __repr__(self):
        return f'Operation(action = {self.action}, args={self.args})'




class Pipeline:

    def __init__(self, start, operations, end):
        self.start = start
        self.operations = operations
        self.end = end

    def __repr__(self):
        return f'Pipeline(start: {self.start}, steps {self.operations}, end: {self.end})'

    def run_pipeline(self):
        print(f'Running {self.start}')
        for operation in self.operations:
            print(f'Running {operation}')
        print(f'Running {self.end}')


def load_json_pipeline(filename):
    """Python function to read json file """

    import json

    pipeline_obj = None

    # Opening JSON file
    with open(filename, 'r') as file:

        # returns JSON object as
        # a dictionary
        data = json.load(file)

        # Iterating through the json
        # list
        pipeline_data= data['pipeline']

        pipeline_obj = Pipeline(pipeline_data['start'], pipeline_data['operations'], pipeline_data['end'])

        print(pipeline_obj)

    return pipeline_obj
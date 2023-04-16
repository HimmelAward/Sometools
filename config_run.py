from lib import *
from functools import partial
import argparse
class Engine:
    def __init__(self,script,args):
        self.script = script
        self.args = args

    def _prepare(self):
        self.script_to_run = partial(self.script,self.args)

    def run(self):
        self._prepare()
        self.script_to_run()

class Config:
    def __init__(self,**kwargs):
        try:
            kwargs.keys()
        except:
            assert True,"必须给带有关键字的参数"

        self.kwargs = kwargs

    def __getattr__(self, attr):
        return self.kwargs[attr] if attr in self.kwargs.keys() else None



if __name__ == "__main__":
    arg = argparse.ArgumentParser(description="this is a simple scanner of web")
    arg.add_argument('--url',type=str,)
    args = arg.parse_args()
    
    web_scanner_config = Config(
        url = args.url,
        type = 'php',
        threads = 5,
        headers = ''
    )
    engine = Engine(web_scaner.main,web_scanner_config)

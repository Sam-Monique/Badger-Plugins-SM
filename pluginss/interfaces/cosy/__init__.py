from badger import interface
from .cosy_run import change_line,replace_line, get_var,get_obs, set_vals,set_rays, run



class Interface(interface.Interface):

    name = 'cosy'

    def __init__(self, params=None):
        super().__init__(params)

        self.settings = {}
        self.path = 0
        self.file = 0

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str):
        path = self.path
        file = self.file
        settings = self.settings
        
        if channel in settings:
            val = get_var(channel,settings,path,file)

        else:
            val = get_obs(channel)
            
        return val
    
        
    
    def set_value(self, channel: str, value):

        
        path = self.path
        file = self.file
        
        cosyfile = path + file + '.fox'

        temp =  file + 'TEMP' +  '.fox'
        cosyfileTemp = path + temp
        settings = self.settings

        line_num = settings[channel][0]
        types = settings[channel][1]
        line = change_line(cosyfile,line_num,value,types)
        replace_line(cosyfileTemp,cosyfileTemp,line_num,line)

    def set_temp_file(self):


        path = self.path
        file = self.file
        settings = self.settings
        set_vals(settings,path,file)
        set_rays(path, file)

    def set_beam_offset(self,dx,dy, pencils = False):
        path = self.path
        file = self.file
        settings = self.settings
        set_vals(settings,path,file)
        set_rays(path, file, dx=dx,dy=dy, pencil= pencils)

    def run(self):
        path = self.path
        file = self.file
        run(path,file)
        

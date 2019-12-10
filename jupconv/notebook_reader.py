import os
import json
import uuid
import shutil
import base64


class NotebookParser():
    def __init__(self, filepath):
        self.notebook = self._read(filepath)
        self.layout = []

    def _read(self, filepath):

        with open(filepath, "r", encoding='utf-8') as f:
            contents = f.read()

        return json.loads(contents)

    def _save_image(self, img_source):
        
        filepath = os.path.join(self.temp_dir, self.random_filename())
        img_data = base64.b64decode(img_source)
        
        with open(filepath, "wb") as f:
            f.write(img_data)
        
        self.layout.append({'content_type': 'image',
                            'content': filepath})

    def _make_temp_folder(self):
        self.temp_dir = str(uuid.uuid4())
        os.mkdir(self.temp_dir)

    def create_layout(self):
        self._make_temp_folder()
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'markdown':
                self.layout.append({'content_type': 'text',
                                    'content': cell['source']})

            if cell['cell_type'] == 'code':
                if cell['outputs']:
                    outputs = [output for output in cell['outputs']
                               if 'data' in output]
                    img_sources = [output['data']['image/png'] for output in outputs
                                   if 'image/png' in output['data']]
                    for img_source in img_sources:
                        self._save_image(img_source)
        return self.layout

    def delete_temp_folder(self):
        shutil.rmtree(self.temp_dir)

    def random_filename(self):
        return str(uuid.uuid4()) + '.png'

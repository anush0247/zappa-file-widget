import base64

from django import forms
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe


class FileWidget(forms.widgets.ClearableFileInput):
    def render(self, name, value, attrs=None):
        attrs["onchange"] = name + "_previewFile()"
        attrs["id"] = "id_" + name + "_tmp"
        file_html = super(FileWidget, self).render(name + "_tmp", value, attrs=attrs)
        html = """
        <script type="text/javascript">
            function """ + name + """_previewFile() {
              var """ + name + """file_input = document.getElementById('id_""" + name + """');
              var file    = document.getElementById('id_""" + name + """_tmp').files[0];
              var reader  = new FileReader();
              reader.addEventListener("load", function () {
                var value = file.name + ":::" +reader.result;
                console.log(value);
                """ + name + """file_input.value = value
              }, false);

              if (file) {
                reader.readAsDataURL(file);
              }
            }
        </script>
        <input type="hidden" value="" name="id_""" + name + """" id="id_""" + name + """" /> """ + file_html + """
        """
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        file_data = data["id_" + name]

        """
        file_data: <file_name>:::data:<file content type>;base64,<base64 encoded file data>
        Example : PG Deletion.txt:::data:text/plain;base64,UEcgRGVsZXRpb2tpIjsKCg==
        """

        _data_list = file_data.split(":::")

        if len(_data_list) == 1:
            return None

        file_name = _data_list[0]
        _data_list = _data_list[1].split(";base64,")

        file_extension = _data_list[0].split("data:")[1]
        file_content = _data_list[1]

        return ContentFile(base64.b64decode(file_content), name=file_name)

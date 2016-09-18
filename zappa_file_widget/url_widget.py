from django import forms
from django.template import Template, Context
from django.utils.safestring import mark_safe


class URLWidget(forms.widgets.URLInput):
    def render(self, name, value, attrs=None):
        html_template = """
        <script type="text/javascript">
            function {{field_name}}_previewFile() {
              var {{field_name}}file_input = document.getElementById('id_{{field_name}}');
              var {{field_name}}file_url = document.getElementById('id_{{field_name}}_url');
              var file    = document.getElementById('id_{{field_name}}_tmp').files[0];
              var reader  = new FileReader();
              reader.addEventListener("load", function () {
                var value = file.name + ":::" +reader.result;
                {{field_name}}file_url.href = file.name;
                {{field_name}}file_url.innerHTML = file.name;
                {{field_name}}file_url.style = 'display:block';
                {{field_name}}file_input.value = 'https://www.gogole.com/' + encodeURI(file.name);
              }, false);

              if (file) {
                reader.readAsDataURL(file);
              }
              //else {
                //{{field_name}}file_url.style = 'display:none';
              //}
            }
        </script>
        <input type="file" id="id_{{field_name}}_tmp"
        onchange="{{field_name}}_previewFile()" />
        <a href="#" id="id_{{field_name}}_url" style="display:none" ></a>
        {{parent_html}}
        """
        attrs['type'] = 'hidden'
        parent_html =  super(URLWidget, self).render(name, value, attrs=attrs)
        template = Template(html_template)
        context = Context({'field_name': name, 'parent_html': parent_html})
        html = template.render(context)

        return mark_safe(html)

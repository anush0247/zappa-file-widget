from django import forms
from django.conf import settings
from django.template import Template, Context
from django.utils.safestring import mark_safe


class URLWidget(forms.widgets.URLInput):
    upload_to = ''

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', self.upload_to)
        super(URLWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        html_template = """
<script src="https://sdk.amazonaws.com/js/aws-sdk-2.1.24.min.js"></script>
<script type="text/javascript">
function {{field_name}}_previewFile() {

    AWS.config.update({
        accessKeyId : '{{AWS_ACCESS_KEY_ID}}',
        secretAccessKey : '{{AWS_SECRET_ACCESS_KEY}}'
    });
    AWS.config.region = '{{AWS_DEFAULT_REGION}}';
    AWS.config.sslEnabled = true;
    AWS.config.logger = true;

    var bucket = new AWS.S3();

    var {{field_name}}file_input = document.getElementById('id_{{field_name}}');
    var {{field_name}}file_url = document.getElementById('id_{{field_name}}_url');
    var {{field_name}}file_loading = document.getElementById('id_{{field_name}}_loading');
    var file    = document.getElementById('id_{{field_name}}_tmp').files[0];
    var reader  = new FileReader();
    reader.addEventListener("load", function () {
        var params = {
            Bucket: '{{AWS_STORAGE_BUCKET_NAME}}',
            Key: '{{prefix}}' + file.name,
            ContentType: file.type,
            Body: file,
            Prefix: '{{prefix}}',
            ACL: 'public-read'
        };
        bucket.upload(params, function (err, data) {
            // results.innerHTML = err ? 'ERROR!' : 'UPLOADED.';
            if (err) {
                alert('Failed to Upload file to s3 ' + err);
            }
            else{
                var s3_key_url = "{{ prefix_url }}" + encodeURI(file.name);
                {{field_name}}file_url.href = s3_key_url;
                {{field_name}}file_url.innerHTML = s3_key_url;
                {{field_name}}file_url.style = 'display:block';
                {{field_name}}file_loading.style = 'display:none';
                {{field_name}}file_input.value = s3_key_url;
            }
        }).on('httpUploadProgress',function(progress) {
          // Log Progress Information
          {{field_name}}file_loading.style = 'display:block';
          var msg = 'Please Wait, Uploading  ' + file.name + ' ('
          {{field_name}}file_loading.innerHTML = msg + Math.round(progress.loaded / progress.total * 100) +'% done)';
        });
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}
</script>
<input type="file" id="id_{{field_name}}_tmp"
onchange="{{field_name}}_previewFile()"/>
<a href="{{field_value}}" id="id_{{field_name}}_url" target="_blank"
style="display:{% if field_value %}block{% else %}none{% endif%}" >{{field_value}}</a><br>
<p id="id_{{field_name}}_loading" style="display:none" ></p>
{{parent_html}}
"""
        attrs['type'] = 'hidden'
        parent_html = super(URLWidget, self).render(name, value, attrs=attrs)
        template = Template(html_template)
        s3_host = 's3-ap-southeast-1.amazonaws.com'
        default_region = getattr(settings, 'AWS_S3_HOST', s3_host).split(".amazonaws.com")[0].split("s3-")[1]
        prefix = settings.MEDIAFILES_LOCATION + "/" + self.upload_to
        context = Context({
            'field_name': name,
            "field_value": value,
            'parent_html': parent_html,
            'prefix': prefix,
            "prefix_url": settings.MEDIA_URL + self.upload_to,
            'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
            'AWS_SECRET_ACCESS_KEY': settings.AWS_SECRET_ACCESS_KEY,
            'AWS_DEFAULT_REGION': default_region,
            'AWS_STORAGE_BUCKET_NAME': settings.AWS_STORAGE_BUCKET_NAME
        })
        html = template.render(context)

        return mark_safe(html)

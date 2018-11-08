from django import template
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()

def disqus_dev():
    """
    Return the HTML/js code to enable DISQUS comments on a local
    development server if settings.DEBUG is True.
    """
    if settings.DEBUG:
        return """<script type="text/javascript">
    var disqus_developer = 1;
</script>"""
    return ""

class DisqusNumRepliesTag(template.Node):
    def __init__(self, identifier):
        self.identifier = template.Variable(identifier) if identifier else None

    def render(self, context):
        shortname = settings.DISQUS_WEBSITE_SHORTNAME
        url = context['request'].build_absolute_uri()
        identifier = self.identifier.resolve(context) if self.identifier else None
        code = ["""<script type="text/javascript">"""]
        if identifier:
            code.append("    var disqus_identifier = '%s';" % identifier)
        code.append("""
    var disqus_url = '%(url)s';
    var disqus_shortname = '%(shortname)s';
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.src = 'http://disqus.com/forums/%(shortname)s/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
</script>""" % dict(shortname=shortname, url=url))
        return "\n".join(code)

class DisqusShowCommentsTag(template.Node):
    def __init__(self, identifier):
        self.identifier = template.Variable(identifier) if identifier else None

    def render(self, context):
        shortname = settings.DISQUS_WEBSITE_SHORTNAME
        url = context['request'].build_absolute_uri()
        identifier = self.identifier.resolve(context) if self.identifier else None
        code = ["""<div id="disqus_thread"></div>
<script type="text/javascript">
    /* <![CDATA[ */"""]
        if identifier:
            code.append("    var disqus_identifier = '%s';" % identifier)
        code.append("""
    var disqus_url = '%(url)s';
    var disqus_shortname = '%(shortname)s';
    var disqus_domain = 'disqus.com';
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript';
        dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.' + disqus_domain + '/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
    /* ]]> */
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript=">comments powered by Disqus.</a></noscript>
<p><a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a></p>""" % dict(shortname=shortname, url=url))
        return "\n".join(code)

def disqus_num_replies(parser, token):
    bits = token.split_contents()
    if len(bits) == 1:
        tag_name = bits[0]
        identifier = ''
    elif len(bits) == 2:
        tag_name, identifier = bits
    else:
        raise template.TemplateSyntaxError(
                u"%r tag accepts only one argument: disqus_identifier" % tag_name)
    return DisqusNumRepliesTag(identifier)

def disqus_show_comments(parser, token):
    bits = token.split_contents()
    if len(bits) == 1:
        tag_name = bits[0]
        identifier = ''
    elif len(bits) == 2:
        tag_name, identifier = bits
    else:
        raise template.TemplateSyntaxError(
                u"%r tag accepts only one argument: disqus_identifier" % tag_name)
    return DisqusShowCommentsTag(identifier)

register.simple_tag(disqus_dev)
register.tag(disqus_num_replies)
register.tag(disqus_show_comments)

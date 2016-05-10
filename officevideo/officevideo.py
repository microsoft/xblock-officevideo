import textwrap

import pkg_resources
import urllib2
import mimetypes
import urlparse, requests, json
import xml.etree.ElementTree as ET
from xblock.core import XBlock
from xblock.fragment import Fragment
from xblock.fields import Scope, String
from django.conf import settings
from django.contrib.auth.models import User
from social.apps.django_app.utils import load_strategy
import logging
LOG = logging.getLogger(__name__)
import time
import re
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode

"""test url: https://wwedudemo17.sharepoint.com/portals/hub/_layouts/15/PointPublishing.aspx?app=video&p=p&chid=4fe89746-6fd9-4a2b-9a42-ea41c5853a53&vid=70113d75-9a34-494a-972d-dc498c12168f """

"""
    <iframe width=640 height=360 
    src='https://wwedudemo17.sharepoint.com/portals/hub/_layouts/15/VideoEmbedHost.aspx?chId=4fe89746%2D6fd9%2D4a2b%2D9a42%2Dea41c5853a53&amp;vId=70113d75%2D9a34%2D494a%2D972d%2Ddc498c12168f&amp;width=640&amp;height=360&amp;autoPlay=false&amp;showInfo=true' allowfullscreen></iframe> 
"""

DEFAULT_VIDEO_URL = ('https://wwedudemo17.sharepoint.com/portals/hub/_layouts/15/VideoEmbedHost.aspx?chId=4fe89746%2D6fd9%2D4a2b%2D9a42%2Dea41c5853a53&amp;vId=70113d75%2D9a34%2D494a%2D972d%2Ddc498c12168f&amp;width=640&amp;height=360&amp;autoPlay=false&amp;showInfo=true')

class OfficeVideoXBlock(XBlock):

    EMBED_CODE_TEMPLATE = textwrap.dedent("""
        <iframe
            src="{}"
            width="640"
            height="360"
            allowfullscreen>
        </iframe>
    """)

    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="OfficeVideo",
    )

    video_url = String(
        display_name="Video URL",
        help="Navigate to the video in your browser and ensure that it is accessible to your intended audience. Copy its URL or embed code and paste it into this field.",
        scope=Scope.settings,
        default=EMBED_CODE_TEMPLATE.format(DEFAULT_VIDEO_URL)
    )

    output_code = String(
        display_name="Output Iframe Embed Code",
        help="Copy the embed code into this field.",
        scope=Scope.settings,
        default=EMBED_CODE_TEMPLATE.format(DEFAULT_VIDEO_URL)
    )

    message = String(
        display_name="video display status message",
        help="Message to help students in case of errors.",
        scope=Scope.settings,
        default="Note: Office Video message."
    )

    message_display_state = String(
        display_name="Whether to display the status message",
        help="Determines whether to display the message to help students in case of errors.",
        scope=Scope.settings,
        default="block"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the OfficeVideoXBlock, shown to students
        when viewing courses.
        """
        embed_code = self.output_code
        if embed_code == '':
            embed_code = self.get_officevideo_embed_code(officevideo_url=self.video_url)

        html = self.resource_string("static/html/officevideo.html")
        frag = Fragment(html.format(embed_code=embed_code, message=self.message, message_display_state=self.message_display_state))
        frag.add_css(self.resource_string("static/css/officevideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/officevideo.js"))
        frag.initialize_js('OfficeVideoXBlock')
        return frag

    def studio_view(self, context=None):
        """
        he primary view of the OfficeVideoXBlock, shown to teachers
        when viewing courses.
        """

        html = self.resource_string("static/html/officevideo_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/officevideo.css"))
        frag.add_javascript(self.resource_string("static/js/src/officevideo_edit.js"))
        frag.initialize_js('OfficeVideoXBlock')
        return frag

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):  # pylint: disable=unused-argument
        """
        Change the settings for this XBlock given by the Studio user
        """
        if not isinstance(submissions, dict):
            LOG.error("submissions object from Studio is not a dict - %r", submissions)
            return {
                'result': 'error'
            }

        self.display_name = submissions['display_name']
        self.video_url = submissions['video_url']

        # Check if user have entered embed code
        embed_code_regex = '<iframe '
        matched = re.match(embed_code_regex, self.video_url, re.IGNORECASE)

        if matched is not None:
            self.output_code = self.video_url
        else:
            self.output_code = ''
        self.message = "Note: Office Video message."
        self.message_display_state = "block"

        return {'result': 'success'}

    def get_officevideo_embed_code(self, officevideo_url):

        embed_code = ''
        try:
            django_user_social = User.objects.get(id=self.xmodule_runtime.user_id).social_auth.get(provider='azuread-oauth2')
            if int(django_user_social.extra_data['expires_on']) < int(time.time()):
                django_user_social.refresh_token(load_strategy())
                django_user_social = User.objects.get(id=self.xmodule_runtime.user_id).social_auth.get(provider='azuread-oauth2')
            url = self.video_url
            parsed = urlparse.urlparse(url)
            query_params = urlparse.parse_qs(parsed.query)
            resp = requests.get("https://" + parsed.netloc + "/portals/hub/_api/VideoService/Channels('" + query_params['chid'][0] + "')/Videos('" + query_params['vid'][0] + "')/GetVideoEmbedCode",
                             headers={'Authorization': 'Bearer ' + django_user_social.tokens,
                                      'Content-Type': 'application/json;odata=verbose'})
            root = ET.fromstring(resp._content)
            embed_code = unicode(root.text, "utf-8")
        except:
            embed_code = '<a target="_blank" href="'+ officevideo_url +'">Office 365 Video</a>'

        return embed_code


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("OfficeVideoXBlock",
             """<vertical_demo>
                <officevideo/>
                <officevideo/>
                </vertical_demo>
             """),
        ]

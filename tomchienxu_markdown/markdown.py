from urllib.parse import quote
from settings import VERDICT_COLORS
import markdown2
import re
import database_models

class TomChienXuOJMarkdown(markdown2.Markdown):
  def __init__(self, *args, **kwargs):
    extensions = ["break-on-newline", "code-friendly", "fenced-code-blocks", "footnotes", "spoiler", "strike", "markdown-in-html"]
    super().__init__(extras=extensions, *args, **kwargs)

  @staticmethod
  def _convert_submission_verdict_element(text: str) -> str:
    regex_verdict_element = r"(\[verdict:(AC|WA|TLE|RTE|IR|MLE|OLE|IE)\])"
    for verdict_element in re.findall(regex_verdict_element, text):
      text = text.replace(verdict_element[0], f'<b class="text-{VERDICT_COLORS.get(verdict_element[1])}">{verdict_element[1]}</b>')

    return text

  @staticmethod
  def _convert_user_element(text: str) -> str:
    regex_user_element = r"(\[user:(\w*)\])"
    for user_element in re.findall(regex_user_element, text):
      user = database_models.User.query.filter_by(username=user_element[1]).first()
      text = text.replace(user_element[0], f'<strike class="text-secondary">{user_element[1]} <b class="text-dark">(404: User Not Found)</b></strike>' if not user else user.render_display)

    return text

  @staticmethod
  def _sanitize_markdown(tag: str) -> str:
    # (tags which can be opened/closed) | (tags which stand alone)
    basic_tag_whitelist = r'^(<\/?(b|blockquote|code|del|dd|dl|dt|em|h1|h2|h3|i|kbd|li|ol(?: start="\d+")?|p|pre|s|sup|sub|strong|strike|ul)>|<(br|hr)\s?\/?>)$'

    # <a href="https://youtu.be/dQw4w9WgXcQ" [optional]:title="69">|[content]</a>
    a_href_link_tag_white = r'^(<a\shref="((https?|ftp):\/\/|\/)[-A-Za-z0-9+&@#\/%?=~_|!:,.;\(\)*[\]$]+"(\stitle="[^"<>]+")?\s?>|<\/a>)$'

    # <img src="url..." [optional]:width="69" [optional]:height="69" [optional]:alt="69" [optional]:title="69">
    img_src_tag_white = r'^(<img\ssrc="(https?:\/\/|\/)[-A-Za-z0-9+&@#\/%?=~_|!:,.;\(\)*[\]$]+"(\swidth="\d{1,3}")?(\sheight="\d{1,3}")?(\salt="[^"<>]*")?(\stitle="[^"<>]*")?\s?\/?>)$'

    if any(map(lambda regex_string: re.search(regex_string, tag), [basic_tag_whitelist, a_href_link_tag_white, img_src_tag_white])):
      return tag
    else:
      any_change_needed = False
      def encode_string(prefix, url):
        nonlocal any_change_needed
        def deep_encode_string(character):
          nonlocal any_change_needed
          any_change_needed = True
          return "%27" if character == "'" else quote(character)
        return prefix + re.sub(r'[^-A-Za-z0-9+&@#\/%?=~_|!:,.;\(\)*[\]$]', deep_encode_string, url)

      encoded_tag = re.sub(r'^(<a href="|<img src=")([^"]*)', encode_string, tag)
      if (any_change_needed and (re.search(a_href_link_tag_white, encoded_tag) or re.search(img_src_tag_white, encoded_tag))):
        return encoded_tag

    return ""

  @staticmethod
  def _balance_markdown_tags(html: str) -> str:
    if not html:
      return ""

    regex_pattern = r'<\/?\w+[^>]*(\s|$|>)'
    tags = re.findall(regex_pattern, html)
    number_of_tags = len(tags)
    if not number_of_tags:
      return html

    ignored_tags = "<p><img><br><li><hr>"
    tag_paired = [False] * number_of_tags
    tag_remove = [False] * number_of_tags
    any_removal_needed = False

    for tag_index in range(number_of_tags):
      tag_name = re.sub(r'<\/?(\w+).*', "$1", tags[tag_index])
      if tag_paired[tag_index] or re.search(f"<{tag_name}>", ignored_tags) > -1:
        continue

      tag = tags[tag_index]
      match = -1
      if re.search(r'/^<\/', tag):
        for tag_sub_index in range(tag_index + 1, number_of_tags):
          if not tag_paired[tag_sub_index] and tags[tag_sub_index] == f"</{tag_name}>":
            match = tag_sub_index
            break

      if match == -1:
        any_removal_needed = tag_remove[tag_index] = True
      else:
        tag_paired[tag_index] = True

    if not any_removal_needed:
      return html

    counter = 0
    def replace_need_to_be_removed_tag(match):
      counter += 1
      return "" if tag_remove[counter] else match
    return re.sub(regex_pattern, replace_need_to_be_removed_tag, html)

  def convert(self, text):
    converted_text = super().convert(text)
    converted_text = self._convert_user_element(converted_text)
    converted_text = self._convert_submission_verdict_element(converted_text)
    # converted_text = self._sanitize_markdown(converted_text)
    # converted_text = self._balance_markdown_tags(converted_text)

    return converted_text
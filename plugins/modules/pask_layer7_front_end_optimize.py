#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


front_end_optimize_html_rewrite_inner_args = dict(
    add_head=dict(type='str'),
    convert_meta_tags=dict(type='str'),
    lazyload_images=dict(type='str'),
    defer_javascript=dict(type='str'),
    move_css_to_head=dict(type='str'),
    move_css_above_scripts=dict(type='str'),
    insert_dns_prefetch=dict(type='str'),
)
front_end_optimize_resource_minify_inner_args = dict(
    elide_attributes=dict(type='str'),
    remove_comments=dict(type='str'),
    retain_comment=dict(type='str'),
    sprite_images=dict(type='str'),
    rewrite_css=dict(type='str'),
    combine_css=dict(type='str'),
    rewrite_javascript=dict(type='str'),
    combine_javascript=dict(type='str'),
    collapse_whitespace=dict(type='str'),
    flatten_css_imports=dict(type='str'),
    inline_import_to_link=dict(type='str'),
    fallback_rewrite_css_urls=dict(type='str'),
    rewrite_style_attributes=dict(type='str'),
)
front_end_optimize_resource_inline_inner_args = dict(
    status=dict(type='str'),
    javascript=dict(type='str'),
    css=dict(type='str'),
)
front_end_optimize_cache_lifetime_inner_args = dict(
    status=dict(type='str')
)
front_end_optimize_rewrite_images_inner_args = dict(
    inline_images=dict(type='str'),
    resize_images=dict(type='str'),
    recompress_images=dict(type='str'),
    resize_rendered_image_dimensions=dict(type='str'),
    recompress_png=dict(type='str'),
    recompress_jpeg=dict(type='str'),
    recompress_webp=dict(type='str'),
    strip_image_meta_data=dict(type='str'),
    strip_image_color_profile=dict(type='str'),
    convert_gif_to_png=dict(type='str'),
    convert_png_to_jpeg=dict(type='str'),
    convert_jpeg_to_webp=dict(type='str'),
    convert_jpeg_to_progressive=dict(type='str')
)

module_args = dict(
    name=dict(type='str', required=True),
    filter=dict(type='str'),
    description=dict(type='str'),
    html_rewrite=dict(
        type='dict', options=front_end_optimize_html_rewrite_inner_args),
    resource_minify=dict(
        type='dict', options=front_end_optimize_resource_minify_inner_args),
    resource_inline=dict(
        type='dict', options=front_end_optimize_resource_inline_inner_args),
    cache_lifetime=dict(
        type='dict', options=front_end_optimize_cache_lifetime_inner_args),
    rewrite_images=dict(
        type='dict', options=front_end_optimize_rewrite_images_inner_args)
)

name = 'layer7'
subname = 'front-end-optimize'

exclude_underscore_list = [
    'add_head', 'convert_meta_tags', 'lazyload_images', 'defer_javascript',
    'move_css_to_head', 'move_css_above_scripts',
    'insert_dns_prefetch', 'elide_attributes', 'remove_comments',
    'retain_comment', 'sprite_images', 'rewrite_css',
    'combine_css', 'rewrite_javascript', 'combine_javascript',
    'collapse_whitespace', 'flatten_css_imports', 'inline_import_to_link',
    'fallback_rewrite_css_urls', 'rewrite_style_attributes', 'inline_images',
    'resize_images', 'recompress_images', 'resize_rendered_image_dimensions',
    'recompress_png', 'recompress_jpeg', 'recompress_webp',
    'strip_image_meta_data', 'strip_image_color_profile',
    'convert_gif_to_png', 'convert_png_to_jpeg', 'convert_jpeg_to_webp',
    'convert_jpeg_to_progressive'
]

class PaskLayer7FrontEndOptimize(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLayer7FrontEndOptimize, self).__init__(name, module_args)
        for exclude_underscore_param in exclude_underscore_list:
            self.exclude_underscore_params.add(exclude_underscore_param)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        if self.module.params['state'] == "absent":
            data = dict()
            data[subname] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(url, self.module.params['name'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    layer7_front_end_optimize = PaskLayer7FrontEndOptimize(name, module_args)
    layer7_front_end_optimize.set_param()
    layer7_front_end_optimize.run()
    layer7_front_end_optimize.set_result()


if __name__ == '__main__':
    main()